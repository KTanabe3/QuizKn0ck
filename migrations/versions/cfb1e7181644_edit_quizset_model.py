"""edit quizset model

Revision ID: cfb1e7181644
Revises: 126e51b1a146
Create Date: 2024-07-08 04:58:28.496992

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cfb1e7181644'
down_revision = '126e51b1a146'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Relations')
    op.drop_table('Quizes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Quizes',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('text', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('ans', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('cand1', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('cand2', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('cand3', mysql.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('Relations',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('set', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('quiz', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###