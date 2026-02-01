import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# 1. On force Python à trouver ton dossier 'app'
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Imports de tes modèles
from app.database.database import Base
from app.models.user import UserModel
from app.models.product import ProductModel
from app.models.menu import MenuModel
from app.models.order import OrderModel

# 3. Cible pour l'autogénération
target_metadata = Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Mode offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Mode online."""
    # On récupère l'URL du fichier alembic.ini
    url = config.get_main_option("sqlalchemy.url")
    
    # On crée le moteur de connexion
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True # Pour détecter les changements de types de colonnes
        )

        with context.begin_transaction():
            context.run_migrations()

# 4. Lancement des migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()