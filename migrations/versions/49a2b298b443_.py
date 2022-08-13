"""empty message

Revision ID: 49a2b298b443
Revises: 533d622d7ad0
Create Date: 2022-08-07 16:52:56.683232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49a2b298b443'
down_revision = '533d622d7ad0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('shows', 'start_time')
    op.drop_column('shows', 'id')
    # ### end Alembic commands ###