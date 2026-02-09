import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    res = conn.execute(text("SELECT COUNT(*) FROM products"))
    count = res.scalar()
    print(f"📊 Nombre de produits trouvés sur Aiven : {count}")

    res_user = conn.execute(text("SELECT username FROM users WHERE username='vendome'"))
    user = res_user.fetchone()
    print(f"👤 Utilisateur 'vendome' trouvé : {'OUI' if user else 'NON'}")