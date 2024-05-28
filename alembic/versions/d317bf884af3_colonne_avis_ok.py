"""colonne avis.ok

Revision ID: d317bf884af3
Revises: f8d00e9b7017
Create Date: 2024-05-28 10:18:25.170221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd317bf884af3'
down_revision: Union[str, None] = 'f8d00e9b7017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('avis', sa.Column('ok', sa.Boolean(), nullable=False, server_default=str(1)))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("avis") as batch_op:
        batch_op.drop_column('ok')
    # ### end Alembic commands ###
