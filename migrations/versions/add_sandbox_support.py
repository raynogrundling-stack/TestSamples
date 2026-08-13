from alembic import op
import sqlalchemy as sa
revision = "add_sandbox_support"
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.add_column(
        "system_settings",
        sa.Column(
            "sandbox_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        )
    )
    op.add_column(
        "system_settings",
        sa.Column(
            "sandbox_pending_disable",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )
    op.add_column(
        "system_settings",
        sa.Column(
            "sandbox_initialized_at",
            sa.DateTime(),
            nullable=True
        )
    )
def downgrade():
    op.drop_column(
        "system_settings",
        "sandbox_initialized_at"
    )
    op.drop_column(
        "system_settings",
        "sandbox_pending_disable"
    )
    op.drop_column(
        "system_settings",
        "sandbox_enabled"
    )