📂 DOSSIER TECHNIQUE : PROJET WACDO


1. Démarche de sécurité et d'initialisation

Pour ce projet, j'ai mis en place une gestion des droits d'accès stricte : seul un administrateur possède les permissions nécessaires pour créer des comptes utilisateurs.

Cette configuration crée cependant un blocage lors de la première installation puisque la base de données est vide. Pour résoudre ce problème de manière professionnelle, j'ai développé un script d'amorçage du système (init_admin.py). Ce script permet d'injecter directement le premier compte administrateur en base de données, ce qui permet ensuite de se connecter à l'API et de gérer le reste du personnel.



2. Guide d'installation et d'utilisation (README)

Voici les étapes définies pour mettre en place et tester l'API :

- Installation des dépendances : pip install -r requirements.txt
- Amorçage du compte admin : python init_admin.py
- Démarrage du serveur : uvicorn main:app --reload
- Exécution de la suite de tests : pytest -v -W ignore



3. Validation de mon travail

J'ai validé l'intégralité de la logique métier et de la sécurité via une suite de tests automatisés. Mon projet affiche actuellement un résultat de 3/3 PASSED.
À travers ces tests, j'ai prouvé que :

- L'administrateur accède correctement à la gestion des utilisateurs.
- L'agent d'accueil peut créer des commandes de manière fluide via le formulaire dédié.
- Le préparateur (cuisine) est restreint aux fonctions de consultation et ne peut pas créer de commandes, respectant ainsi la hiérarchie des rôles que j'ai établie.