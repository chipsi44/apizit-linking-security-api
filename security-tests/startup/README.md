# Import et cache initial

## Objectif et abus représenté

Exécuter du travail avant tout endpoint et retenir de la mémoire au démarrage. Ce scénario permet d'isoler ce comportement pendant une future
qualification, avec des données synthétiques.

## Comportement et endpoints

`GET /startup` — Import : 2 000 hashes et 50 ms maximum ; cache 2 MiB ; mode fail optionnel.

```text
curl -X GET http://127.0.0.1:8080/startup
```

## Observation attendue sur APIZIT

Comparer scan safe, probe d'import, cold start et warm start ; fail doit empêcher le lancement.

## Protection à vérifier et réaction idéale

Isolation du build, limite d'import et safe release. Le résultat doit rester borné et correctement attribué au
client, sans effet sur un autre workspace. Une observation locale ne démontre
pas cette propriété dans AWS.

## Risque et précautions

Niveau : **MEDIUM**, dans les bornes de la fixture. Lire le README racine,
utiliser un environnement jetable, commencer par un appel et ne pas utiliser
de load generator. Pas de production, de paiement, de données réelles, de
lecture de secrets ou de cible tierce. Le plafond par processus ne remplace
pas un budget global lors d'une campagne multi-instance.

Le travail s'exécute à l'import de `service.py` ; GET /startup ne le redéclenche
pas. `ADVERSARIAL_STARTUP_MODE=fail` provoque une erreur synthétique à l'import.
La validation statique Linking doit rester possible, mais le démarrage doit échouer.
Il s'agit d'une simulation de dépendance coûteuse ; aucun hook d'installation,
poids ML ou gros package n'est téléchargé. Le cache alloue exactement 2 MiB.

