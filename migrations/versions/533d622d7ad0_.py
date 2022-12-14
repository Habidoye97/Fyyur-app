"""empty message

Revision ID: 533d622d7ad0
Revises: 2effcb42aa0c
Create Date: 2022-08-07 16:04:31.071245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '533d622d7ad0'
down_revision = '2effcb42aa0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id')
    )
    op.drop_table('venue_artist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue_artist',
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='venue_artist_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='venue_artist_venue_id_fkey'),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id', name='venue_artist_pkey')
    )
    op.drop_table('shows')
    # ### end Alembic commands ###
