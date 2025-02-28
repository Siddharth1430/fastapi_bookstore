"""Add edition

Revision ID: e4dd3e14bd71
Revises: b6c7f45974e4
Create Date: 2025-02-17 21:13:32.572837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4dd3e14bd71'
down_revision: Union[str, None] = 'b6c7f45974e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('edition', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'edition')
    # ### end Alembic commands ###
