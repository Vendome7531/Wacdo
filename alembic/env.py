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
    url = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    if url and url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)
        
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
    # Priorité à la variable d'environnement (indispensable pour Render/Aiven)
    url = os.getenv("DATABASE_URL")
    
    # Si pas de variable d'env, on se rabat sur le fichier alembic.ini
    if not url:
        url = config.get_main_option("sqlalchemy.url")
    
    # Correction du driver pour SQLAlchemy
    if url and url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)

    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

# 4. Lancement des migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()