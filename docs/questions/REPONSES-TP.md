# Réponses aux questions du TP

1. Qu'est-ce qu'un acteur dans un diagramme de cas d'utilisation ?
   Un acteur représente un rôle joué par un utilisateur externe ou un système externe qui interagit avec le système étudié.

2. Qu'est-ce qu'un cas d'utilisation ?
   Un cas d'utilisation décrit une séquence d'actions que le système doit effectuer pour fournir une valeur observable à un acteur.

3. Pourquoi utiliser un acteur générique `Utilisateur` dans ce sujet ?
   Pour représenter tous les types d'utilisateurs qui peuvent se connecter au système, et spécialiser ensuite selon leurs rôles.

4. Quel est l'intérêt de l'héritage entre acteurs en UML ?
   L'héritage permet de factoriser les cas d'utilisation communs et d'ajouter des spécificités pour chaque sous-acteur.

5. Quel lien existe entre diagramme de cas d'utilisation et MCD ?
   Le diagramme de cas d'utilisation identifie les entités métier (acteurs et cas d'utilisation) qui seront modélisées dans le MCD.

6. Qu'est-ce qu'un MCD ?
   Modèle Conceptuel de Données : représentation graphique des entités, attributs et associations du domaine métier.

7. Quelle différence entre MCD et MLD ?
   Le MCD est conceptuel (indépendant du SGBD), le MLD est logique (adapté au relationnel avec tables, clés, etc.).

8. Comment traduit-on une association 1,N en relationnel ?
   La clé primaire de l'entité 1 devient clé étrangère dans l'entité N.

9. Comment traduit-on une association N,N en relationnel ?
   On crée une table d'association contenant les clés primaires des deux entités.

10. Quel est le rôle d'une clé étrangère ?
    Elle établit un lien entre deux tables en référençant la clé primaire d'une autre table.

11. Pourquoi la relation `Commande` / `Facture` peut-elle nécessiter une contrainte `UNIQUE` ?
    Parce qu'une commande ne peut avoir qu'une seule facture.

12. Quelle différence entre Python DB-API et SQLAlchemy ORM ?
    DB-API est une interface bas niveau pour exécuter des requêtes SQL directement, ORM mappe les objets Python aux tables SQL.

13. Qu'est-ce qu'un CRUD ?
    Create, Read, Update, Delete : les opérations de base sur les données.

14. Pourquoi faut-il exécuter `commit()` après certaines requêtes ?
    Pour valider les modifications en base de données (INSERT, UPDATE, DELETE sont dans une transaction).

15. À quoi sert une requête avec jointure dans ce contexte ?
    Pour récupérer des données liées de plusieurs tables, par exemple client et ses commandes.