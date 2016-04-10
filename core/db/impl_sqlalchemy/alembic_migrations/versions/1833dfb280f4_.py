"""empty message

Revision ID: 1833dfb280f4
Revises: d3e764a1db46
Create Date: 2016-04-10 00:56:14.653206

"""

# revision identifiers, used by Alembic.
revision = '1833dfb280f4'
down_revision = 'd3e764a1db46'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('event_type', sa.String(length=255), nullable=False),
    sa.Column('host', sa.String(length=255), nullable=False),
    sa.Column('fabscript', sa.String(length=255), nullable=False),
    sa.Column('msg', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.drop_table('alarm')
    op.add_column('agent', sa.Column('fabscript_map', sa.String(length=1000), nullable=False))
    op.drop_column('agent', 'setup_result')
    op.drop_column('agent', 'crit_errs')
    op.drop_column('agent', 'warn_errs')
    op.drop_column('agent', 'warn_errs_len')
    op.drop_column('agent', 'crit_errs_len')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agent', sa.Column('crit_errs_len', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('agent', sa.Column('warn_errs_len', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('agent', sa.Column('warn_errs', mysql.VARCHAR(length=1000), nullable=False))
    op.add_column('agent', sa.Column('crit_errs', mysql.VARCHAR(length=1000), nullable=False))
    op.add_column('agent', sa.Column('setup_result', mysql.VARCHAR(length=255), nullable=False))
    op.drop_column('agent', 'fabscript_map')
    op.create_table('alarm',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.Column('host', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=55), nullable=False),
    sa.Column('msg', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('status', mysql.VARCHAR(length=55), nullable=False),
    sa.Column('task', mysql.VARCHAR(length=55), nullable=False),
    sa.Column('scheduled_time', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('event')
    ### end Alembic commands ###
