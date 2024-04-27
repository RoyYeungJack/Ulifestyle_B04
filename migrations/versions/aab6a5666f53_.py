"""empty message

Revision ID: aab6a5666f53
Revises: 8a41f22114bd
Create Date: 2024-04-22 03:31:28.881461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aab6a5666f53'
down_revision = '8a41f22114bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imagepath', sa.String(length=140), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post_tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_tag',
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name='post_tag_post_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name='post_tag_tag_id_fkey'),
    sa.PrimaryKeyConstraint('post_id', 'tag_id', name='post_tag_pkey')
    )
    op.drop_table('post_image')
    # ### end Alembic commands ###
