"""Ajout annee et nombre_exemplaires

Revision ID: 8bb71584624d
Revises: 031bfbf3c367
Create Date: 2025-07-05 22:35:35.917065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bb71584624d'
down_revision = '031bfbf3c367'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('livres', schema=None) as batch_op:
        batch_op.add_column(sa.Column('annee', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('nombre_exemplaires', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('livres', schema=None) as batch_op:
        batch_op.drop_column('nombre_exemplaires')
        batch_op.drop_column('annee')

    # ### end Alembic commands ###
