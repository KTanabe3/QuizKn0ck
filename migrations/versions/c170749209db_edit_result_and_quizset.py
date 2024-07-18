"""edit Result and QuizSet

Revision ID: c170749209db
Revises: 0c6583a01b77
Create Date: 2024-07-15 05:24:05.072067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c170749209db'
down_revision = '0c6583a01b77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quizset', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'QuizSets', ['quizset'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Result', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('quizset')

    # ### end Alembic commands ###
