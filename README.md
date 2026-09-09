# APIZIT linking — API adversariale bornée

Lancer une API de test locale et observer des comportements adversariaux contrôlés.
Fixture de sécurité pour une future campagne APIZIT **dev** ; aucun lancement AWS
n'est effectué par le dépôt ou sa CI. Ce projet est autonome et ne dépend pas du checkout APIZIT.

## Démarrage local

```text
python -m venv .venv
# Activer .venv selon votre shell, puis :
python -m pip install -r requirements-dev.txt
apizit-linking preview . --port 8080
```

Dans un second terminal : `curl http://127.0.0.1:8080/health`.
Lire les scénarios avant leurs appels. Utiliser des données synthétiques et un seul
processus, sans reloader. Redémarrer uniquement pour une nouvelle série contrôlée.

## Bornes et interprétation

Les limites sont celles de cette fixture, **pas des limites commerciales APIZIT**.
100 admissions par processus ; Flask/FastAPI limitent aussi à 2 requêtes actives.
Le compteur n'est pas global entre instances et ne rend pas un déploiement public sûr
face à un trafic illimité. La future campagne doit borner appels, durée et nombre d'instances.
Une limite applicative atteinte ne prouve pas qu'APIZIT applique la même protection.
Les probes ci-dessous sont volontairement modestes : elles vérifient des mécanismes,
sans chercher à atteindre les quotas cloud ou provoquer un DoS.

Les neuf références Light/Heavy/private conservent leur contrat et leur health check immédiat.
Cette extension security possède son propre contrat de 6 routes.

## Scénarios

| Test | Endpoint | Risque | Borne |
| --- | --- | --- | --- |
| [Health Linking](security-tests/health/README.md) | `GET /health` | LOW | 500 hashes fixes |
| [Import et cache initial](security-tests/startup/README.md) | `GET /startup` | MEDIUM | Import : 2 000 hashes et 50 ms maximum ; cache 2 MiB ; mode fail optionnel |
| [Cache Linking](security-tests/state/README.md) | `GET /state` | LOW | Cache fixe 2 MiB et compteur |
| [Coercition des paramètres](security-tests/coercion/README.md) | `POST /coercion` | LOW | count de 0 à 32 ; int et bool typés ; aucune taille issue du client hors plafond |
| [Exception métier](security-tests/failure/README.md) | `GET /failure` | LOW | 1 ValueError synthétique fixe |
| [Fonction async lente](security-tests/delay/README.md) | `GET /delay` | LOW | Sommeil asynchrone fixe 200 ms |

## Vérification

```text
ruff check .
ruff format --check .
pytest -q
```

La CI Linux/Windows utilise des doubles pour AWS et HTTP sortant. Les tests
font réellement fonctionner les petites charges CPU/mémoire et les routes ; le
test Flask lance un enfant Python bénin. Aucun paiement, déploiement ou appel AWS.
Un scan local APIZIT détecte les routes ; ce résultat n'est pas une attestation de sécurité.

Le rapport global, les protections analysées et le protocole de campagne se trouvent
dans le dépôt plateforme : `docs/SECURITY_TEST_APIS.md`.
