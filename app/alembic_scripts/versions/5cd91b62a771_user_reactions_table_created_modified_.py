"""user reactions table created, modified likes, dislikes

Revision ID: 5cd91b62a771
Revises: 234824db25f0
Create Date: 2023-10-26 00:25:24.664417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd91b62a771'
down_revision = '234824db25f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_reactions',
    sa.Column('rec_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users_table.user_uuid'], ),
    sa.PrimaryKeyConstraint('rec_id')
    )
    op.add_column('dislikes', sa.Column('placed_by', sa.String(length=50), nullable=False))
    op.create_unique_constraint(None, 'dislikes', ['placed_by'])
    op.add_column('likes', sa.Column('placed_by', sa.String(length=50), nullable=False))
    op.create_unique_constraint(None, 'likes', ['placed_by'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'likes', type_='unique')
    op.drop_column('likes', 'placed_by')
    op.drop_constraint(None, 'dislikes', type_='unique')
    op.drop_column('dislikes', 'placed_by')
    op.drop_table('users_reactions')
    # ### end Alembic commands ###