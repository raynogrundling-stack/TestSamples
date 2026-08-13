from alembic import op
import sqlalchemy as sa

revision = "extend_submission_model"
down_revision = "add_sandbox_support"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "submissions",
        sa.Column(
            "customer_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.add_column(
        "submissions",
        sa.Column(
            "sample_description",
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        "submissions",
        sa.Column(
            "sample_type",
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        "submissions",
        sa.Column(
            "test_required",
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        "submissions",
        sa.Column(
            "results_email",
            sa.String(length=255),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_submissions_customer",
        "submissions",
        "customers",
        ["customer_id"],
        ["id"]
    )


def downgrade():

    op.drop_constraint(
        "fk_submissions_customer",
        "submissions",
        type_="foreignkey"
    )

    op.drop_column(
        "submissions",
        "results_email"
    )

    op.drop_column(
        "submissions",
        "test_required"
    )

    op.drop_column(
        "submissions",
        "sample_type"
    )

    op.drop_column(
        "submissions",
        "sample_description"
    )

    op.drop_column(
        "submissions",
        "customer_id"
    )