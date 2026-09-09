# Exception métier

## Objectif et abus représenté

Provoquer des erreurs répétées ou des traces exposant des détails internes. Ce scénario permet d'isoler ce comportement pendant une future
qualification, avec des données synthétiques.

## Comportement et endpoints

`GET /failure` — 1 ValueError synthétique fixe.

```text
curl -X GET http://127.0.0.1:8080/failure
```

## Observation attendue sur APIZIT

Observer réponse publique et logs ; aucun message ni secret fourni par l'utilisateur.

## Protection à vérifier et réaction idéale

Sérialisation sûre des erreurs et état de release fidèle. Le résultat doit rester borné et correctement attribué au
client, sans effet sur un autre workspace. Une observation locale ne démontre
pas cette propriété dans AWS.

## Risque et précautions

Niveau : **LOW**, dans les bornes de la fixture. Lire le README racine,
utiliser un environnement jetable, commencer par un appel et ne pas utiliser
de load generator. Pas de production, de paiement, de données réelles, de
lecture de secrets ou de cible tierce. Le plafond par processus ne remplace
pas un budget global lors d'une campagne multi-instance.

