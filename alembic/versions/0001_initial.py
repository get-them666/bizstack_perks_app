from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
dependencies = None


def upgrade():
    # Create deals table
    op.create_table(
        'deals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('brand', sa.String(length=128), nullable=True),
        sa.Column('hotel_name', sa.String(length=256), nullable=True),
        sa.Column('city', sa.String(length=32), nullable=True),
        sa.Column('monetized_url', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create leads table
    op.create_table(
        'leads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('business_name', sa.String(length=256), nullable=False),
        sa.Column('annual_revenue', sa.Float(), nullable=False),
        sa.Column('credit_score', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('sellable', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create click_events table
    op.create_table(
        'click_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('deal_id', sa.Integer(), sa.ForeignKey('deals.id'), nullable=False),
        sa.Column('referrer', sa.String(length=512), nullable=True),
        sa.Column('user_agent', sa.String(length=512), nullable=True),
        sa.Column('remote_addr', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create premium_orders table
    op.create_table(
        'premium_orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(length=128), nullable=True),
        sa.Column('stripe_checkout_id', sa.String(length=256), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(length=8), nullable=True),
        sa.Column('product', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create underwrite_assessments table
    op.create_table(
        'underwrite_assessments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('lead_id', sa.Integer(), sa.ForeignKey('leads.id'), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('decision', sa.String(length=64), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )


def downgrade():
    op.drop_table('underwrite_assessments')
    op.drop_table('premium_orders')
    op.drop_table('click_events')
    op.drop_table('leads')
    op.drop_table('deals')
