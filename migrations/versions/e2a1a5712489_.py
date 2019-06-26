"""empty message

Revision ID: e2a1a5712489
Revises: 
Create Date: 2019-06-26 04:22:47.492087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2a1a5712489'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('transaction_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('insider_ticker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insider_id', sa.Integer(), nullable=False),
    sa.Column('ticker_id', sa.Integer(), nullable=False),
    sa.Column('relation', sa.String(), nullable=True),
    sa.Column('owner_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['insider_id'], ['insider.id'], ),
    sa.ForeignKeyConstraint(['ticker_id'], ['ticker.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker_id', sa.Integer(), nullable=False),
    sa.Column('price_date', sa.Date(), nullable=False),
    sa.Column('start', sa.DECIMAL(), nullable=True),
    sa.Column('high', sa.DECIMAL(), nullable=True),
    sa.Column('low', sa.DECIMAL(), nullable=True),
    sa.Column('last', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['ticker_id'], ['ticker.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insider_ticker_id', sa.Integer(), nullable=False),
    sa.Column('transaction_type_id', sa.Integer(), nullable=False),
    sa.Column('shares_traded', sa.Integer(), nullable=True),
    sa.Column('last_price', sa.DECIMAL(), nullable=True),
    sa.Column('shares_held', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['insider_ticker_id'], ['insider_ticker.id'], ),
    sa.ForeignKeyConstraint(['transaction_type_id'], ['transaction_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trade')
    op.drop_table('price')
    op.drop_table('insider_ticker')
    op.drop_table('transaction_type')
    op.drop_table('ticker')
    op.drop_table('insider')
    # ### end Alembic commands ###