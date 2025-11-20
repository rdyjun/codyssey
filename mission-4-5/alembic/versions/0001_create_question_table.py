"""question 테이블 생성

Revision ID: 0001_create_question_table
Revises: 
Create Date: 2025-11-20 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# 리비전 식별자 — Alembic에서 사용됨
revision = '0001_create_question_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'question',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('create_date', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('question')
