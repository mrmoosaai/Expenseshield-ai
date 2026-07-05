"""
Command-line utility for audit log management.
Terminal se audit logs ko easily check karenge.
"""

import click
from monitoring.audit_viewer import audit_viewer
from monitoring.audit_logger import audit_logger


@click.group()
def cli():
    """Audit Log Management Tool - Tamper-proof decision tracking."""
    pass


@cli.command()
@click.option('--agent', default=None, help='Filter by agent name')
@click.option('--decision', default=None, help='Filter by decision (APPROVED/BLOCKED/REQUIRES_APPROVAL)')
@click.option('--limit', default=50, help='Maximum records to display')
def logs(agent, decision, limit):
    """Display recent audit logs."""
    click.echo(f"\n📋 Fetching audit logs (limit: {limit})...")
    if agent:
        click.echo(f"   Filter: Agent = {agent}")
    if decision:
        click.echo(f"   Filter: Decision = {decision}")
    
    audit_viewer.display_logs(agent_name=agent, decision_filter=decision, limit=limit)


@cli.command()
def stats():
    """Display audit log statistics."""
    click.echo("\n📊 Generating audit statistics...\n")
    audit_viewer.display_summary_stats()


@cli.command()
def verify():
    """Verify audit log integrity."""
    click.echo("\n🔍 Verifying audit log integrity...\n")
    audit_viewer.verify_and_report()


@cli.command()
@click.option('--filename', default=None, help='Output filename (default: audit_report_TIMESTAMP.json)')
def export(filename):
    """Export detailed audit report."""
    if filename:
        click.echo(f"\n📁 Exporting audit report to: {filename}\n")
        filepath = audit_viewer.export_detailed_report(filename)
    else:
        click.echo(f"\n📁 Exporting audit report...\n")
        filepath = audit_viewer.export_detailed_report()
    
    click.echo(f"✅ Report exported to: {filepath}")


@cli.command()
@click.argument('expense_id')
def find(expense_id):
    """Find all audit records for an expense."""
    click.echo(f"\n🔎 Searching for expense: {expense_id}\n")
    
    records = audit_logger.get_audit_summary(limit=10000)
    expense_records = [r for r in records if r.get('expense_id') == expense_id]
    
    if not expense_records:
        click.echo(f"❌ No records found for expense: {expense_id}")
        return
    
    click.echo(f"📋 Found {len(expense_records)} record(s):\n")
    
    for i, record in enumerate(expense_records, 1):
        click.echo(f"  {i}. Agent: {record.get('agent_name')}")
        click.echo(f"     Decision: {record.get('decision')}")
        click.echo(f"     Reason: {record.get('reason')}")
        click.echo(f"     Timestamp: {record.get('timestamp')[:19]}")
        click.echo()


@cli.command()
@click.option('--agent', default=None, help='Count records for specific agent')
@click.option('--decision', default=None, help='Count records with specific decision')
def count(agent, decision):
    """Count audit records."""
    click.echo(f"\n📊 Counting audit records...\n")
    
    records = audit_logger.get_audit_summary(
        agent_name=agent,
        decision_filter=decision,
        limit=100000
    )
    
    if agent:
        click.echo(f"   Agent: {agent}")
    if decision:
        click.echo(f"   Decision: {decision}")
    
    click.echo(f"   Total: {len(records)} records\n")


@cli.command()
def summary():
    """Quick summary of audit status."""
    click.echo("\n" + "=" * 60)
    click.echo("📋 AUDIT LOG SUMMARY")
    click.echo("=" * 60 + "\n")
    
    # Get integrity status
    integrity = audit_logger.verify_integrity()
    
    if integrity['is_valid']:
        status = "✅ VERIFIED"
        color = 'green'
    else:
        status = "⚠️ COMPROMISED"
        color = 'red'
    
    click.secho(f"Status: {status}", fg=color, bold=True)
    click.echo(f"Total Records: {integrity['total_records']}")
    
    if not integrity['is_valid']:
        click.secho(f"Tampered Records: {len(integrity['tampered_records'])}", fg='red')
        click.secho(f"Errors: {len(integrity['errors'])}", fg='red')
    
    click.echo("\n" + "=" * 60 + "\n")


@cli.command()
def test():
    """Run audit logging tests."""
    click.echo("\n🧪 Running audit logging tests...\n")
    
    import subprocess
    import sys
    
    try:
        result = subprocess.run(
            [sys.executable, "test_audit_logging.py"],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            click.secho("\n✅ All tests passed!", fg='green', bold=True)
        else:
            click.secho(f"\n❌ Tests failed (exit code: {result.returncode})", fg='red', bold=True)
    
    except Exception as e:
        click.secho(f"\n❌ Error running tests: {e}", fg='red', bold=True)


@cli.command()
def help_audit():
    """Show audit logging help and examples."""
    help_text = """
╔════════════════════════════════════════════════════════════════════╗
║         AUDIT LOGGING SYSTEM - HELP & EXAMPLES                    ║
╚════════════════════════════════════════════════════════════════════╝

📋 COMMAND EXAMPLES:

1. View Recent Logs
   python audit_cli.py logs --limit 20
   
2. Filter by Agent
   python audit_cli.py logs --agent "Finance Agent" --limit 10
   
3. Filter by Decision Status
   python audit_cli.py logs --decision BLOCKED --limit 10
   
4. View Statistics
   python audit_cli.py stats
   
5. Verify Integrity
   python audit_cli.py verify
   
6. Export Report
   python audit_cli.py export
   python audit_cli.py export --filename my_report.json
   
7. Find Specific Expense
   python audit_cli.py find EXP001
   python audit_cli.py find EXP_SECURITY_001
   
8. Count Records
   python audit_cli.py count
   python audit_cli.py count --agent "Finance Agent"
   python audit_cli.py count --decision APPROVED
   
9. Quick Summary
   python audit_cli.py summary
   
10. Run Tests
    python audit_cli.py test

═════════════════════════════════════════════════════════════════════

📊 DECISION STATUSES:
   • APPROVED           - Expense approved
   • BLOCKED            - Expense blocked (security/fraud)
   • REQUIRES_APPROVAL  - Needs manager review
   • SUCCESS            - Operation completed successfully
   • ERROR              - System error occurred

🤖 AGENT NAMES:
   • Security Agent     - Security screening
   • Finance Agent      - Budget checking
   • Skill Agent        - Skill execution
   • Orchestrator Agent - Final workflow decision
   • MultiAgentSystem   - System-level errors

════════════════════════════════════════════════════════════════════

🔐 SECURITY:
   ✅ All records are HMAC-SHA256 signed
   ✅ Tampering is immediately detected
   ✅ Cannot forge or modify records
   ✅ Cryptographically secure

📋 CSV Format:
   audit_logs/decisions.csv contains:
   - timestamp: When decision was made
   - transaction_id: Unique transaction ID
   - agent_name: Which agent made decision
   - expense_id: Expense identifier
   - amount: Expense amount
   - category: Expense category
   - decision: APPROVED/BLOCKED/etc
   - reason: Why this decision
   - details: JSON details
   - hash: HMAC-SHA256 signature

════════════════════════════════════════════════════════════════════

For more details, see: AUDIT_LOGGING_GUIDE.md
    """
    click.echo(help_text)


if __name__ == '__main__':
    cli()
