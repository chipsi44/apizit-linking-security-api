"""Plain Python business probes; imports are intentionally bounded but observable."""

import hashlib
import os
import threading
import time
import uuid


def startup_probe():
    if os.getenv("ADVERSARIAL_STARTUP_MODE") == "fail":
        raise RuntimeError("SYNTHETIC startup failure")
    started = time.monotonic()
    # A finite import workload, no files, network, threads or SDK at import time.
    for _ in range(2000):
        hashlib.sha256(b"synthetic-startup" * 64).digest()
        if time.monotonic() - started >= 0.05:
            break
    return {"phase": "module_import", "elapsed_seconds": time.monotonic() - started}


STARTUP = startup_probe()
CACHE = bytearray(2 * 1024 * 1024)
INSTANCE = uuid.uuid4().hex
LOCK = threading.Lock()
REQUESTS = 0
COUNTER = 0


def admit():
    global REQUESTS
    with LOCK:
        if REQUESTS >= 100:
            return False
        REQUESTS += 1
        return True


def health() -> dict:
    """Health Linking. 500 hashes fixes."""
    if not admit():
        return {"status": "fixture_budget_exhausted"}
    # Deliberately compute inside a business function bound to /health.
    for _ in range(500):
        hashlib.sha256(b"synthetic-health").digest()
    return {"status": "ok", "iterations": 500}


def startup() -> dict:
    """Import et cache initial. Import : 2 000 hashes et 50 ms maximum ; cache 2 MiB ; mode
    fail optionnel.
    """
    return {"instance": INSTANCE, "startup": STARTUP, "retained_bytes": len(CACHE)}


def state() -> dict:
    """Cache Linking. Cache fixe 2 MiB et compteur."""
    global COUNTER
    if not admit():
        return {"status": "fixture_budget_exhausted"}
    with LOCK:
        COUNTER += 1
        return {"instance": INSTANCE, "counter": COUNTER, "retained_bytes": len(CACHE)}


def coercion(count: int = 1, enabled: bool = False) -> dict:
    """Coercition des paramètres. count de 0 à 32 ; int et bool typés ; aucune taille issue du
    client hors plafond.
    """
    if not admit():
        return {"status": "fixture_budget_exhausted"}
    if not 0 <= count <= 32:
        return {"status": "fixture_cap", "maximum": 32}
    return {"count": count, "enabled": enabled, "values": list(range(count))}


def failure() -> dict:
    """Exception métier. 1 ValueError synthétique fixe."""
    if not admit():
        return {"status": "fixture_budget_exhausted"}
    raise ValueError("SYNTHETIC controlled business failure; no customer data")


async def delay() -> dict:
    """Fonction async lente. Sommeil asynchrone fixe 200 ms."""
    import asyncio

    if not admit():
        return {"status": "fixture_budget_exhausted"}
    await asyncio.sleep(0.2)
    return {"delay_seconds": 0.2, "phase": "request"}
