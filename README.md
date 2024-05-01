# Autoflex README
## Présentation d'Autoflex
Autoflex est un système de gestion de location de voitures conçu pour offrir une interface utilisateur simple pour enregistrer des utilisateurs, louer des voitures, et visualiser des statistiques liées aux locations de voitures, aux utilisateurs, aux marques de voitures, et aux entreprises. Ce système gère une base de données relationnelle pour stocker et manipuler les données concernant les utilisateurs, les voitures, les marques, les entreprises et les contrats de location.

## Description des tables et des relations
### Tables Principales
- User : Contient les informations des utilisateurs comme le nom, le prénom, l'email, le mot de passe, et le numéro de téléphone.
- PrivateIndividual : Extension de la table User pour les individus privés, incluant des informations supplémentaires comme l'adresse et le numéro de permis de conduire.
- Company : Contient des informations sur les entreprises comme le nom, le secteur d'activité, et l'adresse.
- Employee : Extension de la table User pour les employés, incluant l'identifiant de l'entreprise et le département.
- Brand : Stocke les informations sur les marques de voitures.
- Car : Détails des voitures disponibles pour la location, incluant la marque, le modèle, l'année, la couleur, et le prix par kilomètre.
- RentalContract : Enregistre les détails des contrats de location, y compris les informations sur la voiture louée, l'utilisateur, la date de début et de fin de location, et les kilomètres parcourus.
### Relations
- PrivateIndividual et Employee sont liées à User via une clé étrangère indiquant que chaque entrée dans ces tables est également un utilisateur.
- Car est liée à Brand via une clé étrangère indiquant la marque de la voiture.
- RentalContract est connectée à Car et User, indiquant quel utilisateur a loué quelle voiture et quand.
## Vues et Déclencheurs (Triggers)
### Vues
- carStats : Donne une vue d'ensemble des voitures, y compris la disponibilité, le nombre total de locations, les kilomètres totaux parcourus, et les revenus générés.
- brandStats : Fournit des statistiques sur les marques de voitures, incluant le nombre total de voitures par marque, le total des locations, les kilomètres parcourus et les revenus.
- rentalStats : Offre des statistiques sur les locations par mois et par année, incluant le total des locations, les kilomètres parcourus et les revenus.
- companyStats : Présente des informations sur les entreprises, notamment le nombre total d'employés, les locations effectuées par ces employés, et les revenus associés.
### Déclencheurs
- before_delete_user_who_has_rental_contract : Assure qu'avant de supprimer un utilisateur, son identifiant dans les contrats de location existants soit remplacé par celui de l'utilisateur inconnu.
- delete_all_employee_from_company : Supprime tous les employés d'une entreprise lorsque cette dernière est supprimée.
- cannot_delete_the_unknown_user : Empêche la suppression de l'utilisateur inconnu.
- before_insert_rental_contract_for_car_with_max_kilometers : Vérifie que la voiture n'a pas dépassé son kilométrage maximal avant d'insérer un nouveau contrat de location.
- before_insert_rental_contract_for_rented_car : Empêche l'insertion d'un contrat de location pour une voiture déjà louée durant les dates spécifiées.


## Python application

Voici un aperçu des fonctions principales du système Autoflex, avec une explication de leur rôle et de leur enchaînement.

### `get_db_connection()`
- Description : Établit la connexion à la base de données MySQL. Gère les exceptions liées à la connexion et interrompt le programme si la connexion échoue.
- Utilisation : Appelée au démarrage de l'application pour établir la connexion initiale.

### `register_user(db)`
- Description : Permet à un nouvel utilisateur de s'inscrire. Demande à l'utilisateur de saisir ses informations personnelles, vérifie la validité des données, et insère les informations dans la base de données.
- Utilisation : Appelée lorsque l'utilisateur sélectionne l'option d'enregistrement.
### `login_user(db)`
- Description : Gère le processus de connexion pour les utilisateurs enregistrés. Vérifie les identifiants fournis contre ceux enregistrés dans la base de données.
- Utilisation : Appelée lorsque l'utilisateur sélectionne l'option de connexion.
### `rent_a_car(db, user)`
- Description : Permet à l'utilisateur de louer une voiture disponible. Affiche les voitures disponibles et gère la création d'un nouveau contrat de location.
- Utilisation : Appelée après la connexion de l'utilisateur, lorsqu'il choisit de louer une voiture.
### `rental_stats(db)`
- Description : Affiche les statistiques de location, permettant à l'utilisateur de voir les données par année ou pour toutes les années.
- Utilisation : Accessible après la connexion, pour les utilisateurs souhaitant voir les statistiques de location.
###  `car_stats(db)`
- Description : Fournit des statistiques détaillées sur les voitures, incluant les revenus générés et le nombre de fois que chaque voiture a été louée.
- Utilisation : Appelée pour afficher les statistiques détaillées des voitures.
### `brand_stats(db)`
- Description : Présente des statistiques sur les marques de voitures, telles que le nombre total de voitures, de locations, et les revenus générés par marque.
- Utilisation : Appelée pour consulter les statistiques par marque de voiture.
### `company_stats(db)`
- Description : Affiche des informations sur les entreprises, comme le nombre d'employés et les activités de location liées.
- Utilisation : Accessible aux utilisateurs connectés, surtout utile pour les responsables d'entreprise.
### `user_info(db, user)`
- Description : Affiche les informations de l'utilisateur et permet la mise à jour ou la suppression du compte utilisateur.
- Utilisation : Accessible après la connexion, permettant à l'utilisateur de gérer son compte.
### `update_user_info(db, user)`
- Description : Permet à l'utilisateur de mettre à jour ses informations personnelles.
- Utilisation : Appelée depuis user_info lorsqu'un utilisateur souhaite modifier ses informations.
### `delete_user(db, user)`
- Description : Permet à l'utilisateur de supprimer son compte. Implémente des contrôles pour empêcher la suppression si des contraintes sont en place.
- Utilisation : Appelée depuis user_info pour supprimer un compte utilisateur.
## Flow Map
1) Démarrage de l'Application :
- La connexion à la base de données est établie.
- L'utilisateur arrive sur l'écran d'accueil.
- Écran d'Accueil :
    - Option 1 : Enregistrer un nouvel utilisateur (register_user).
    - Option 2 : Connexion d'un utilisateur existant (login_user).
    - Option 3 : Quitter l'application.
2) Après Connexion :
    - Option 1 : Louer une voiture (rent_a_car).
    - Option 2 : Afficher les statistiques de location (rental_stats).
    - Option 3 : Afficher les statistiques des voitures (car_stats).
    - Option 4 : Afficher les statistiques des marques (brand_stats).
    - Option 5 : Afficher les statistiques des entreprises (company_stats).
    - Option 6 : Afficher et gérer les informations de l'utilisateur (user_info).
    - Option 7 : Déconnexion.
    - Option 8 : Quitter l'application.

## Comment lancez l'application ? 

1. Assurez-vous que Docker desktop est lancé sur votre machine.
2. Ouvrez un terminal et exécutez la commande suivante pour démarrer le Docker Compose :
```bash
docker compose up --build
```
3. Une fois que les conteneurs sont prêts, ouvrez un autre terminal et exécutez la commande suivante pour lancer l'application Python :
```bash
docker compose run pythonapp
```
4. Suivez les instructions à l'écran pour utiliser l'application Autoflex.

5. Pour arrêter l'application, appuyez sur `Ctrl + C` dans le terminal où l'application Python est en cours d'exécution, puis exécutez la commande suivante pour arrêter les conteneurs Docker pour s'assurer qu'ils sont correctement arrêtés :
```bash
docker compose down
```

## Mise à jour de l'application

1. Pour seulement mettre à jour l'application Python, exécutez la commande suivante :
```bash
docker compose up --build pythonapp
```
2. Pour seulement mettre à jour la base de données MySQL, exécutez la commande suivante :
```bash
docker compose up --build mysql
```