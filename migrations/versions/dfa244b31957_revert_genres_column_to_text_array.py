"""Revert genres column to text array

Revision ID: dfa244b31957
Revises: de88e6e2b7af
Create Date: 2024-06-14 19:31:09.034519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dfa244b31957'
down_revision = 'de88e6e2b7af'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('Venue', 'genres',
                   existing_type=postgresql.ARRAY(postgresql.ENUM('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'R_B', 'Reggae', 'RocknRoll', 'Soul', 'Swing', 'Other', name='genreenum')),
                   type_=sa.ARRAY(sa.String()),
                   existing_nullable=False,
                   nullable=False)
    op.alter_column('Artist', 'genres',
                   existing_type=postgresql.ARRAY(postgresql.ENUM('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'R_B', 'Reggae', 'RocknRoll', 'Soul', 'Swing', 'Other', name='genreenum')),
                   type_=sa.ARRAY(sa.String()),
                   existing_nullable=False,
                   nullable=False)

def downgrade():
    op.alter_column('Venue', 'genres',
                   existing_type=sa.ARRAY(sa.String()),
                   type_=postgresql.ARRAY(postgresql.ENUM('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'R_B', 'Reggae', 'RocknRoll', 'Soul', 'Swing', 'Other', name='genreenum')),
                   existing_nullable=False,
                   nullable=False)
    op.alter_column('Artist', 'genres',
                   existing_type=sa.ARRAY(sa.String()),
                   type_=postgresql.ARRAY(postgresql.ENUM('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'R_B', 'Reggae', 'RocknRoll', 'Soul', 'Swing', 'Other', name='genreenum')),
                   existing_nullable=False,
                   nullable=False)