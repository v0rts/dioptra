"""Remove legacy v0 tables

Revision ID: 4b2d781f8bb4
Revises: fd786b5377d6
Create Date: 2024-07-25 15:49:07.329979

"""

import sqlalchemy as sa
from alembic import op

from dioptra.restapi.db.custom_types import GUID

# revision identifiers, used by Alembic.
revision = "4b2d781f8bb4"
down_revision = "fd786b5377d6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("legacy_queues", schema=None) as batch_op:
        batch_op.drop_index("ix_legacy_queues_name")

    with op.batch_alter_table("legacy_jobs", schema=None) as batch_op:
        batch_op.drop_index("ix_legacy_jobs_experiment_id")
        batch_op.drop_index("ix_legacy_jobs_mlflow_run_id")
        batch_op.drop_index("ix_legacy_jobs_queue_id")
        batch_op.drop_index("ix_legacy_jobs_status")

    op.drop_table("legacy_jobs")
    op.drop_table("legacy_users")
    op.drop_table("legacy_queue_locks")
    with op.batch_alter_table("legacy_experiments", schema=None) as batch_op:
        batch_op.drop_index("ix_legacy_experiments_name")

    op.drop_table("legacy_experiments")
    op.drop_table("legacy_queues")
    op.drop_table("legacy_job_statuses")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    legacy_job_statuses = op.create_table(
        "legacy_job_statuses",
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("status", name="pk_legacy_job_statuses"),
    )

    op.bulk_insert(
        legacy_job_statuses,
        [
            {"status": "queued"},
            {"status": "started"},
            {"status": "deferred"},
            {"status": "finished"},
            {"status": "failed"},
        ],
    )

    op.create_table(
        "legacy_queues",
        sa.Column(
            "queue_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("last_modified", sa.DateTime(), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("queue_id", name="pk_legacy_queues"),
    )
    with op.batch_alter_table("legacy_queues", schema=None) as batch_op:
        batch_op.create_index("ix_legacy_queues_name", ["name"], unique=1)

    op.create_table(
        "legacy_experiments",
        sa.Column(
            "experiment_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("last_modified", sa.DateTime(), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("experiment_id", name="pk_legacy_experiments"),
    )
    with op.batch_alter_table("legacy_experiments", schema=None) as batch_op:
        batch_op.create_index("ix_legacy_experiments_name", ["name"], unique=1)

    op.create_table(
        "legacy_queue_locks",
        sa.Column(
            "queue_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["queue_id"],
            ["legacy_queues.queue_id"],
            name="fk_legacy_queue_locks_queue_id_legacy_queues",
        ),
        sa.PrimaryKeyConstraint("queue_id", name="pk_legacy_queue_locks"),
    )
    op.create_table(
        "legacy_users",
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("email_address", sa.Text(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=False),
        sa.Column("last_modified_on", sa.DateTime(), nullable=False),
        sa.Column("last_login_on", sa.DateTime(), nullable=False),
        sa.Column("password_expire_on", sa.DateTime(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("alternative_id", GUID(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name="pk_legacy_users"),
        sa.UniqueConstraint("alternative_id", name="uq_legacy_users_alternative_id"),
    )
    op.create_table(
        "legacy_jobs",
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("mlflow_run_id", sa.String(length=36), nullable=True),
        sa.Column("experiment_id", sa.BigInteger(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("last_modified", sa.DateTime(), nullable=True),
        sa.Column("timeout", sa.Text(), nullable=True),
        sa.Column("workflow_uri", sa.Text(), nullable=True),
        sa.Column("entry_point", sa.Text(), nullable=True),
        sa.Column("entry_point_kwargs", sa.Text(), nullable=True),
        sa.Column("depends_on", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=255), nullable=True),
        sa.Column("queue_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["experiment_id"],
            ["legacy_experiments.experiment_id"],
            name="fk_legacy_jobs_experiment_id_legacy_experiments",
        ),
        sa.ForeignKeyConstraint(
            ["queue_id"],
            ["legacy_queues.queue_id"],
            name="fk_legacy_jobs_queue_id_legacy_queues",
        ),
        sa.ForeignKeyConstraint(
            ["status"],
            ["legacy_job_statuses.status"],
            name="fk_legacy_jobs_status_legacy_job_statuses",
        ),
        sa.PrimaryKeyConstraint("job_id", name="pk_legacy_jobs"),
    )
    with op.batch_alter_table("legacy_jobs", schema=None) as batch_op:
        batch_op.create_index("ix_legacy_jobs_status", ["status"], unique=False)
        batch_op.create_index("ix_legacy_jobs_queue_id", ["queue_id"], unique=False)
        batch_op.create_index(
            "ix_legacy_jobs_mlflow_run_id", ["mlflow_run_id"], unique=False
        )
        batch_op.create_index(
            "ix_legacy_jobs_experiment_id", ["experiment_id"], unique=False
        )
    # ### end Alembic commands ###