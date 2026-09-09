import ast
import asyncio
from pathlib import Path

import httpx
import pytest
from apizit_linking import compile_linking_file
from apizit_linking.fastapi import create_app

import service

ROOT = Path(__file__).resolve().parents[1]


def test_static_manifest_and_business_boundary():
    result = compile_linking_file(ROOT / "apizit_linking.yaml", ROOT)
    assert result.is_valid, result.diagnostics
    assert len(result.routes) == 6
    tree = ast.parse((ROOT / "service.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(
                name.name.split(".")[0] not in {"flask", "fastapi", "apizit_linking", "backend"}
                for name in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] not in {
                "flask",
                "fastapi",
                "apizit_linking",
                "backend",
            }


def test_all_http_paths_and_validation():
    async def run():
        app = create_app(ROOT)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://synthetic.invalid",
        ) as client:
            assert (await client.get("/health")).json()["iterations"] == 500
            startup = (await client.get("/startup")).json()
            assert startup["startup"]["phase"] == "module_import"
            assert startup["retained_bytes"] == 2 * 1024 * 1024
            first = (await client.get("/state")).json()
            second = (await client.get("/state")).json()
            assert second["counter"] == first["counter"] + 1
            assert second["instance"] == first["instance"]
            assert (await client.get("/delay")).json()["delay_seconds"] == 0.2
            assert (await client.get("/failure")).status_code == 500
            result = await client.post("/coercion", json={"count": 32, "enabled": True})
            assert len(result.json()["values"]) == 32
            assert (await client.post("/coercion", json={"count": 33})).json()[
                "status"
            ] == "fixture_cap"
            assert (await client.post("/coercion", json={"count": "oops"})).status_code == 400

    asyncio.run(run())


@pytest.mark.parametrize("count", [-1, 33, 10**50])
def test_output_allocation_bound(count, monkeypatch):
    monkeypatch.setattr(service, "REQUESTS", 0)
    assert service.coercion(count)["status"] == "fixture_cap"


def test_lifetime_budget(monkeypatch):
    monkeypatch.setattr(service, "REQUESTS", 99)
    assert service.health()["status"] == "ok"
    assert service.health()["status"] == "fixture_budget_exhausted"
    assert service.failure()["status"] == "fixture_budget_exhausted"
    assert asyncio.run(service.delay())["status"] == "fixture_budget_exhausted"


def test_opt_in_startup_failure(monkeypatch):
    monkeypatch.setenv("ADVERSARIAL_STARTUP_MODE", "fail")
    with pytest.raises(RuntimeError, match="SYNTHETIC startup failure"):
        service.startup_probe()
    # Static validation must still succeed without importing the customer module.
    result = compile_linking_file(ROOT / "apizit_linking.yaml", ROOT)
    assert result.is_valid
