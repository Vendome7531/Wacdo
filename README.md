DOSSIER TECHNIQUE : PROJET WACDO


1. Démarche de sécurité et d'initialisation

Pour ce projet, j'ai mis en place une gestion des droits d'accès stricte : seul un administrateur possède les permissions nécessaires pour créer des comptes utilisateurs.
Cette configuration crée cependant un blocage lors de la première installation puisque la base de données est vide. Pour résoudre ce problème de manière professionnelle, j'ai développé un script d'amorçage du système (init_admin.py). Ce script permet d'injecter directement le premier compte administrateur en base de données, ce qui permet ensuite de se connecter à l'API et de gérer le reste du personnel.



2. Guide d'installation et d'utilisation (README)

Voici les étapes définies pour mettre en place et tester l'API :

- Cloner le projet et créer l'environnement virtuel : python -m venv venv PUIS source venv/bin/activate (pour windows : venv\Scripts\activate)
- Installation des dépendances : pip install -r requirements.txt
- Amorçage du compte admin : python init_admin.py
- Démarrage du serveur : uvicorn main:app --reload
(La documentation Swagger est accessible sur : http://127.0.0.1:8000/docs)
- Exécution de la suite de tests : pytest --durations=3 -v



3. Tests

Le projet inclut une suite de tests automatisés avec Pytest pour garantir la sécurité et la fiabilité des calculs métier.
Lancement des tests:
Pour exécuter l'ensemble de la suite de tests avec le détail des performances : pytest --durations=3 -v

    Point Technique : Le fichier pytest.ini

Pour professionnaliser la suite de tests, j'ai configuré un fichier pytest.ini à la racine du projet. Ce fichier sert de "tour de contrôle" pour l'environnement de test :

    Automatisation des options (addopts) : Il force l'affichage détaillé (-v) et l'analyse de performance (--durations=3) à chaque lancement.

    Résolution des imports (pythonpath) : Il définit la racine du projet comme source, ce qui permet aux tests d'importer les modules de l'application (ex: from app.main...) sans erreur de chemin.

    Stabilité Asynchrone : Il configure le mode strict pour asyncio, indispensable pour tester les routes de FastAPI.


4. Mise en Production et Déploiement

Pour préparer l'application à un environnement réel, les étapes suivantes ont été réalisées :

Gestion des variables d'environnement : Utilisation d'un fichier .env pour isoler les données sensibles (URL de la base de données, clés secrètes JWT) du code source.

Configuration CORS (Cross-Origin Resource Sharing) : Mise en place d'un middleware de sécurité pour restreindre les appels API aux seuls domaines autorisés (ex: le futur Front-end), limitant ainsi les risques d'attaques externes.

Plateforme de déploiement : L'application est prête à être déployée sur une plateforme de type Railway ou Render, avec une base de données MySQL managée.