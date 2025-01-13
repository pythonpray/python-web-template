"""message

Revision ID: ae9f84067247
Revises: 1cf54aa004c1
Create Date: 2025-01-07 12:53:49.049126+00:00

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ae9f84067247"
down_revision = "1cf54aa004c1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "enrollment",
        sa.Column("student_id", sa.Integer(), nullable=True),
        sa.Column("course_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False, comment="主键ID"),
        sa.Column("create_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_deleted", sa.BOOLEAN(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_enrollment_id"), "enrollment", ["id"], unique=False)
    op.drop_index("ix_enrollments_id", table_name="enrollments")
    op.drop_table("enrollments")
    op.alter_column("student", "name", existing_type=sa.VARCHAR(length=100), comment="姓名", existing_nullable=False)
    op.alter_column("student", "email", existing_type=sa.VARCHAR(length=100), type_=sa.String(length=255), nullable=False, comment="邮箱")
    op.drop_constraint("student_student_id_key", "student", type_="unique")
    op.create_unique_constraint(None, "student", ["email"])
    op.drop_column("student", "student_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("student", sa.Column("student_id", sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_constraint(None, "student", type_="unique")
    op.create_unique_constraint("student_student_id_key", "student", ["student_id"])
    op.alter_column("student", "email", existing_type=sa.String(length=255), type_=sa.VARCHAR(length=100), nullable=True, comment=None, existing_comment="邮箱")
    op.alter_column("student", "name", existing_type=sa.VARCHAR(length=100), comment=None, existing_comment="姓名", existing_nullable=False)
    op.create_table(
        "enrollments",
        sa.Column("student_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("course_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("status", sa.VARCHAR(length=20), autoincrement=False, nullable=True),
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False, comment="主键ID"),
        sa.Column("create_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("is_deleted", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["course.id"], name="enrollments_course_id_fkey"),
        sa.ForeignKeyConstraint(["student_id"], ["student.id"], name="enrollments_student_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="enrollments_pkey"),
    )
    op.create_index("ix_enrollments_id", "enrollments", ["id"], unique=False)
    op.drop_index(op.f("ix_enrollment_id"), table_name="enrollment")
    op.drop_table("enrollment")
    # ### end Alembic commands ###
