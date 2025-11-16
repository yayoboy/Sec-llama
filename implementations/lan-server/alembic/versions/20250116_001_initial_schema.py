"""Initial schema with all tables

Revision ID: 001_initial
Revises:
Create Date: 2025-01-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'analyst', 'viewer')")
    op.execute("CREATE TYPE scanstatus AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled')")
    op.execute("CREATE TYPE incidentseverity AS ENUM ('critical', 'high', 'medium', 'low', 'info')")
    op.execute("CREATE TYPE incidentstatus AS ENUM ('new', 'investigating', 'contained', 'remediated', 'closed')")

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('role', postgresql.ENUM('admin', 'analyst', 'viewer', name='userrole', create_type=False), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create api_keys table
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key_id', sa.String(length=64), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('usage_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_keys_id'), 'api_keys', ['id'], unique=False)
    op.create_index(op.f('ix_api_keys_key_id'), 'api_keys', ['key_id'], unique=True)
    op.create_index('idx_api_key_user', 'api_keys', ['user_id'], unique=False)

    # Create llm_configurations table
    op.create_table(
        'llm_configurations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('host', sa.String(length=255), nullable=True),
        sa.Column('api_key', sa.String(length=255), nullable=True),
        sa.Column('model_name', sa.String(length=255), nullable=False),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('last_tested', sa.DateTime(timezone=True), nullable=True),
        sa.Column('test_status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_llm_configurations_id'), 'llm_configurations', ['id'], unique=False)

    # Create scan_executions table
    op.create_table(
        'scan_executions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('execution_id', sa.String(length=64), nullable=False),
        sa.Column('tool_name', sa.String(length=100), nullable=False),
        sa.Column('tool_category', sa.String(length=50), nullable=False),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('status', postgresql.ENUM('pending', 'running', 'completed', 'failed', 'cancelled', name='scanstatus', create_type=False), nullable=False),
        sa.Column('progress', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('findings_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('critical_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('high_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('medium_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('low_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scan_executions_id'), 'scan_executions', ['id'], unique=False)
    op.create_index(op.f('ix_scan_executions_execution_id'), 'scan_executions', ['execution_id'], unique=True)
    op.create_index(op.f('ix_scan_executions_tool_name'), 'scan_executions', ['tool_name'], unique=False)
    op.create_index('idx_scan_tool_status', 'scan_executions', ['tool_name', 'status'], unique=False)
    op.create_index('idx_scan_user_date', 'scan_executions', ['user_id', 'started_at'], unique=False)

    # Create discovered_hosts table
    op.create_table(
        'discovered_hosts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=False),
        sa.Column('mac_address', sa.String(length=17), nullable=True),
        sa.Column('hostname', sa.String(length=255), nullable=True),
        sa.Column('os_guess', sa.String(length=255), nullable=True),
        sa.Column('ttl', sa.Integer(), nullable=True),
        sa.Column('open_ports', sa.JSON(), nullable=True),
        sa.Column('is_alive', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('first_seen', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('discovery_scan_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['discovery_scan_id'], ['scan_executions.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ip_address', 'mac_address', name='uq_host_ip_mac')
    )
    op.create_index(op.f('ix_discovered_hosts_id'), 'discovered_hosts', ['id'], unique=False)
    op.create_index(op.f('ix_discovered_hosts_ip_address'), 'discovered_hosts', ['ip_address'], unique=False)
    op.create_index(op.f('ix_discovered_hosts_mac_address'), 'discovered_hosts', ['mac_address'], unique=False)
    op.create_index('idx_host_ip_mac', 'discovered_hosts', ['ip_address', 'mac_address'], unique=False)

    # Create vulnerabilities table
    op.create_table(
        'vulnerabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vuln_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cve_id', sa.String(length=20), nullable=True),
        sa.Column('cvss_score', sa.Float(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('affected_host', sa.String(length=255), nullable=True),
        sa.Column('affected_service', sa.String(length=255), nullable=True),
        sa.Column('affected_file', sa.String(length=500), nullable=True),
        sa.Column('affected_line', sa.Integer(), nullable=True),
        sa.Column('remediation', sa.Text(), nullable=True),
        sa.Column('references', sa.JSON(), nullable=True),
        sa.Column('scan_execution_id', sa.Integer(), nullable=True),
        sa.Column('is_false_positive', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_resolved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('discovered_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['scan_execution_id'], ['scan_executions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vulnerabilities_id'), 'vulnerabilities', ['id'], unique=False)
    op.create_index(op.f('ix_vulnerabilities_vuln_id'), 'vulnerabilities', ['vuln_id'], unique=True)
    op.create_index(op.f('ix_vulnerabilities_cve_id'), 'vulnerabilities', ['cve_id'], unique=False)
    op.create_index('idx_vuln_severity_resolved', 'vulnerabilities', ['severity', 'is_resolved'], unique=False)
    op.create_index('idx_vuln_cve', 'vulnerabilities', ['cve_id'], unique=False)

    # Create incidents table
    op.create_table(
        'incidents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('incident_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('severity', postgresql.ENUM('critical', 'high', 'medium', 'low', 'info', name='incidentseverity', create_type=False), nullable=False),
        sa.Column('status', postgresql.ENUM('new', 'investigating', 'contained', 'remediated', 'closed', name='incidentstatus', create_type=False), nullable=False),
        sa.Column('incident_type', sa.String(length=100), nullable=True),
        sa.Column('affected_systems', sa.JSON(), nullable=True),
        sa.Column('iocs', sa.JSON(), nullable=True),
        sa.Column('playbook', sa.JSON(), nullable=True),
        sa.Column('containment_actions', sa.JSON(), nullable=True),
        sa.Column('remediation_steps', sa.JSON(), nullable=True),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incidents_id'), 'incidents', ['id'], unique=False)
    op.create_index(op.f('ix_incidents_incident_id'), 'incidents', ['incident_id'], unique=True)
    op.create_index('idx_incident_severity_status', 'incidents', ['severity', 'status'], unique=False)

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=True),
        sa.Column('resource_id', sa.String(length=64), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)
    op.create_index('idx_audit_user_action', 'audit_logs', ['user_id', 'action'], unique=False)
    op.create_index('idx_audit_date', 'audit_logs', ['created_at'], unique=False)

    # Create reports table
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('format', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('scan_execution_ids', sa.JSON(), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('generated_by', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['generated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reports_id'), 'reports', ['id'], unique=False)
    op.create_index(op.f('ix_reports_report_id'), 'reports', ['report_id'], unique=True)
    op.create_index('idx_report_type_date', 'reports', ['report_type', 'generated_at'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('idx_report_type_date', table_name='reports')
    op.drop_index(op.f('ix_reports_report_id'), table_name='reports')
    op.drop_index(op.f('ix_reports_id'), table_name='reports')
    op.drop_table('reports')

    op.drop_index('idx_audit_date', table_name='audit_logs')
    op.drop_index('idx_audit_user_action', table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_created_at'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_table('audit_logs')

    op.drop_index('idx_incident_severity_status', table_name='incidents')
    op.drop_index(op.f('ix_incidents_incident_id'), table_name='incidents')
    op.drop_index(op.f('ix_incidents_id'), table_name='incidents')
    op.drop_table('incidents')

    op.drop_index('idx_vuln_cve', table_name='vulnerabilities')
    op.drop_index('idx_vuln_severity_resolved', table_name='vulnerabilities')
    op.drop_index(op.f('ix_vulnerabilities_cve_id'), table_name='vulnerabilities')
    op.drop_index(op.f('ix_vulnerabilities_vuln_id'), table_name='vulnerabilities')
    op.drop_index(op.f('ix_vulnerabilities_id'), table_name='vulnerabilities')
    op.drop_table('vulnerabilities')

    op.drop_index('idx_host_ip_mac', table_name='discovered_hosts')
    op.drop_index(op.f('ix_discovered_hosts_mac_address'), table_name='discovered_hosts')
    op.drop_index(op.f('ix_discovered_hosts_ip_address'), table_name='discovered_hosts')
    op.drop_index(op.f('ix_discovered_hosts_id'), table_name='discovered_hosts')
    op.drop_table('discovered_hosts')

    op.drop_index('idx_scan_user_date', table_name='scan_executions')
    op.drop_index('idx_scan_tool_status', table_name='scan_executions')
    op.drop_index(op.f('ix_scan_executions_tool_name'), table_name='scan_executions')
    op.drop_index(op.f('ix_scan_executions_execution_id'), table_name='scan_executions')
    op.drop_index(op.f('ix_scan_executions_id'), table_name='scan_executions')
    op.drop_table('scan_executions')

    op.drop_index(op.f('ix_llm_configurations_id'), table_name='llm_configurations')
    op.drop_table('llm_configurations')

    op.drop_index('idx_api_key_user', table_name='api_keys')
    op.drop_index(op.f('ix_api_keys_key_id'), table_name='api_keys')
    op.drop_index(op.f('ix_api_keys_id'), table_name='api_keys')
    op.drop_table('api_keys')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

    # Drop ENUM types
    op.execute("DROP TYPE incidentstatus")
    op.execute("DROP TYPE incidentseverity")
    op.execute("DROP TYPE scanstatus")
    op.execute("DROP TYPE userrole")
