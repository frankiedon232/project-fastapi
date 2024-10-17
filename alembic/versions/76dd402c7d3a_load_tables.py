"""load-tables

Revision ID: 76dd402c7d3a
Revises: 
Create Date: 2024-10-17 13:30:28.433677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76dd402c7d3a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_categories',
    sa.Column('catagory_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_name', sa.String(length=400), nullable=False),
    sa.Column('category_content', sa.Text(), nullable=True),
    sa.Column('category_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('contact_email', sa.String(length=500), nullable=False),
    sa.Column('category_state', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('category_price > 0', name='check_price_ck'),
    sa.PrimaryKeyConstraint('catagory_id'),
    sa.UniqueConstraint('category_state', name='category_state_uq'),
    sa.UniqueConstraint('contact_email', name='contact_email_uq')
    )
    op.create_index('category_email_idx', 'post_categories', ['contact_email'], unique=False)
    op.create_index('category_name_idx', 'post_categories', ['category_name'], unique=False)
    op.create_index('category_price_idx', 'post_categories', ['category_price'], unique=False)
    op.create_index('category_state_idx', 'post_categories', ['category_state'], unique=False)
    op.create_index('created_at_idx', 'post_categories', ['created_at'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_index('created_at_idx', table_name='post_categories')
    op.drop_index('category_state_idx', table_name='post_categories')
    op.drop_index('category_price_idx', table_name='post_categories')
    op.drop_index('category_name_idx', table_name='post_categories')
    op.drop_index('category_email_idx', table_name='post_categories')
    op.drop_table('post_categories')
    # ### end Alembic commands ###
