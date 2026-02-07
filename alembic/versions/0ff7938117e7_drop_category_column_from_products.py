"""drop_category_column_from_products

Revision ID: 0ff7938117e7
Revises: 25454533f107
Create Date: 2026-02-07 19:36:31.892375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ff7938117e7'
down_revision: Union[str, Sequence[str], None] = '25454533f107'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop category column from products table
    op.drop_column('products', 'category')


def downgrade() -> None:
    """Downgrade schema."""
    # Add category column back (assuming it was a String type)
    op.add_column('products', sa.Column('category', sa.String(), nullable=True))
