# Coercition des paramètres

## Objectif et abus représenté

Transformer des paramètres permissifs en allocation disproportionnée. Ce scénario permet d'isoler ce comportement pendant une future
qualification, avec des données synthétiques.

## Comportement et endpoints

`POST /coercion` — count de 0 à 32 ; int et bool typés ; aucune taille issue du client hors plafond.

```text
curl -X POST http://127.0.0.1:8080/coercion -H "Content-Type: application/json" --data-binary @payload.json
```

## Observation attendue sur APIZIT

Comparer valeur valide, entier invalide et entier énorme ; distinguer binding 400 et plafond métier.

## Protection à vérifier et réaction idéale

Validation de liaison et maintien du contrat moteur indépendant. Le résultat doit rester borné et correctement attribué au
client, sans effet sur un autre workspace. Une observation locale ne démontre
pas cette propriété dans AWS.

## Risque et précautions

Niveau : **LOW**, dans les bornes de la fixture. Lire le README racine,
utiliser un environnement jetable, commencer par un appel et ne pas utiliser
de load generator. Pas de production, de paiement, de données réelles, de
lecture de secrets ou de cible tierce. Le plafond par processus ne remplace
pas un budget global lors d'une campagne multi-instance.

Créer payload.json avec `{"count":32,"enabled":true}`. Tester ensuite 33 puis
une chaîne invalide. Les plafonds sont des résultats métier ; le moteur conserve
son contrat de validation 400. Aucun quota APIZIT n’est modifié.
