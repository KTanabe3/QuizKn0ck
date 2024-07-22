"""edit quizset

Revision ID: e5b5198390cd
Revises: cfb1e7181644
Create Date: 2024-07-08 05:04:11.222830

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e5b5198390cd'
down_revision = 'cfb1e7181644'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('QuizSets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'Users', ['author_id'], ['id'])
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('QuizSets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###