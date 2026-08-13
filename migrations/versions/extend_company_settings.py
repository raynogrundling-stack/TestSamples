from alembic import op
import sqlalchemy as sa

revision = "extend_companysettings"
down_revision = "extend_submission_model"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "system_settings",
        sa.Column(
            "company_logo",
            sa.String(length=500),
            nullable=True
        )
    )


def downgrade():

    op.drop_column(
        "system_settings",
        "company_logo"
    )