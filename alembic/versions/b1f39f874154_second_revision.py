"""second revision

Revision ID: b1f39f874154
Revises: 919ae95f2b19
Create Date: 2023-01-24 16:58:40.020700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1f39f874154'
down_revision = '919ae95f2b19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_player_email', table_name='player')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_player_email', 'player', ['email'], unique=False)
    # ### end Alembic commands ###