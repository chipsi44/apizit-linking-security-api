# Fonction async lente

## Objectif et abus représenté

Occuper une invocation via une fonction métier asynchrone. Ce scénario permet d'isoler ce comportement pendant une future
qualification, avec des données synthétiques.

## Comportement et endpoints

`GET /delay` — Sommeil asynchrone fixe 200 ms.

```text
curl -X GET http://127.0.0.1:8080/delay
```

## Observation attendue sur APIZIT

Comparer durée et métrologie avec Flask /slow et ASGI /background.

## Protection à vérifier et réaction idéale

Attente async, deadline et finalisation du runtime. Le résultat doit rester borné et correctement attribué au
client, sans effet sur un autre workspace. Une observation locale ne démontre
pas cette propriété dans AWS.

## Risque et précautions

Niveau : **LOW**, dans les bornes de la fixture. Lire le README racine,
utiliser un environnement jetable, commencer par un appel et ne pas utiliser
de load generator. Pas de production, de paiement, de données réelles, de
lecture de secrets ou de cible tierce. Le plafond par processus ne remplace
pas un budget global lors d'une campagne multi-instance.
