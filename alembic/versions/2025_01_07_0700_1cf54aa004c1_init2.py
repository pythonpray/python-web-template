"""init2

Revision ID: 1cf54aa004c1
Revises: 
Create Date: 2025-01-07 07:00:13.259948+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cf54aa004c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('teacher', sa.String(length=100), nullable=True),
    sa.Column('max_students', sa.Integer(), nullable=True),
    sa.Column('current_students', sa.Integer(), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_id'), 'course', ['id'], unique=False)
    op.create_table('student',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('student_id', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_index(op.f('ix_student_id'), 'student', ['id'], unique=False)
    op.create_table('enrollments',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enrollments_id'), 'enrollments', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_enrollments_id'), table_name='enrollments')
    op.drop_table('enrollments')
    op.drop_index(op.f('ix_student_id'), table_name='student')
    op.drop_table('student')
    op.drop_index(op.f('ix_course_id'), table_name='course')
    op.drop_table('course')
    # ### end Alembic commands ###
