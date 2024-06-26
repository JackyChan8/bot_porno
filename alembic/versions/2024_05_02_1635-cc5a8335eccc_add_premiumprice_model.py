"""Add PremiumPrice Model

Revision ID: cc5a8335eccc
Revises: 903833af2b2b
Create Date: 2024-05-02 16:35:41.289603

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc5a8335eccc"
down_revision: Union[str, None] = "903833af2b2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "premiumprice",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("premiumprice")
    # ### end Alembic commands ###
