"""Made swing trade end_date nullable

Revision ID: 077b9cf0bcc0
Revises: d758495e059e
Create Date: 2023-03-10 13:08:43.945887

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '077b9cf0bcc0'
down_revision = 'd758495e059e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('swing_trade', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('swing_trade', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    # ### end Alembic commands ###
