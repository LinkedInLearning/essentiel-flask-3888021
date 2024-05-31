"""Generation initiale

Revision ID: f8d00e9b7017
Revises: 
Create Date: 2024-05-28 08:51:21.491942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.modeles import projets, references, avis, refs_projets


# revision identifiers, used by Alembic.
revision: str = 'f8d00e9b7017'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creation', sa.DateTime(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('sujet', sa.String(length=20), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    table_projets = op.create_table('projets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('titre', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    table_references = op.create_table('references',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('entreprise', sa.String(length=50), nullable=False),
    sa.Column('logo', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    table_avis = op.create_table('avis',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creation', sa.DateTime(), nullable=False),
    sa.Column('contenu', sa.String(), nullable=False),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.Column('auteur', sa.String(length=50), nullable=True),
    sa.Column('id_projet', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_projet'], ['projets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    table_refs_projets = op.create_table('references_projets',
    sa.Column('id_reference', sa.Integer(), nullable=False),
    sa.Column('id_projet', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_projet'], ['projets.id'], ),
    sa.ForeignKeyConstraint(['id_reference'], ['references.id'], ),
    sa.PrimaryKeyConstraint('id_reference', 'id_projet')
    )
    # ### end Alembic commands ###
    op.bulk_insert(table_projets, projets)
    op.bulk_insert(table_references, references)
    op.bulk_insert(table_avis, avis)
    op.bulk_insert(table_refs_projets, refs_projets)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('references_projets')
    op.drop_table('avis')
    op.drop_table('references')
    op.drop_table('projets')
    op.drop_table('contacts')
    # ### end Alembic commands ###