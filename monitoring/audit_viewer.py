"""
Audit log management utilities.
Audit logs ko display aur verify karne ke liye.
"""

from monitoring.audit_logger import audit_logger
from monitoring.logger import logger
from tabulate import tabulate
from typing import Optional
import json


class AuditLogViewer:
    """Utility to view and analyze audit logs."""
    
    @staticmethod
    def display_logs(
        agent_name: Optional[str] = None,
        decision_filter: Optional[str] = None,
        limit: int = 50
    ) -> None:
        """
        Display audit logs in a formatted table.
        
        Args:
            agent_name: Filter by agent name
            decision_filter: Filter by decision status
            limit: Maximum records to display
        """
        records = audit_logger.get_audit_summary(
            agent_name=agent_name,
            decision_filter=decision_filter,
            limit=limit
        )
        
        if not records:
            print("📭 No audit records found.")
            return
        
        # Prepare table data
        table_data = []
        for record in records:
            table_data.append([
                record.get("timestamp", "")[-8:],  # Show time only
                record.get("agent_name", ""),
                record.get("expense_id", "")[:10],  # Truncate ID
                record.get("amount", ""),
                record.get("decision", ""),
                record.get("reason", "")[:40] + "..." if len(record.get("reason", "")) > 40 else record.get("reason", ""),
            ])
        
        headers = ["Time", "Agent", "Expense ID", "Amount", "Decision", "Reason"]
        
        print("\n📋 AUDIT LOG:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\n📊 Total Records: {len(records)}\n")
    
    @staticmethod
    def display_summary_stats() -> None:
        """Display statistics about audit logs."""
        records = audit_logger.get_audit_summary(limit=1000)
        
        if not records:
            print("📭 No audit records found.")
            return
        
        # Calculate stats
        stats = {
            "total": len(records),
            "approved": sum(1 for r in records if r.get("decision") == "APPROVED"),
            "blocked": sum(1 for r in records if r.get("decision") == "BLOCKED"),
            "requires_approval": sum(1 for r in records if r.get("decision") == "REQUIRES_APPROVAL"),
            "errors": sum(1 for r in records if r.get("decision") == "ERROR"),
        }
        
        # Count by agent
        agent_counts = {}
        for record in records:
            agent = record.get("agent_name", "Unknown")
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        print("\n📊 AUDIT LOG STATISTICS:")
        print(f"  Total Records: {stats['total']}")
        print(f"  ✅ Approved: {stats['approved']}")
        print(f"  ❌ Blocked: {stats['blocked']}")
        print(f"  ⏳ Requires Approval: {stats['requires_approval']}")
        print(f"  💥 Errors: {stats['errors']}")
        print(f"\n🤖 Records by Agent:")
        for agent, count in agent_counts.items():
            percentage = (count / stats['total']) * 100
            print(f"  • {agent}: {count} ({percentage:.1f}%)")
        print()
    
    @staticmethod
    def verify_and_report() -> None:
        """Verify audit log integrity and report findings."""
        print("\n🔍 Verifying audit log integrity...")
        
        result = audit_logger.verify_integrity()
        
        print("\n" + "=" * 60)
        
        if result["is_valid"]:
            print("✅ AUDIT LOG INTEGRITY: VERIFIED")
            print(f"   Total Records: {result['total_records']}")
            print("   Status: All records are intact and unmodified")
        else:
            print("❌ AUDIT LOG INTEGRITY: COMPROMISED")
            print(f"   Total Records: {result['total_records']}")
            print(f"   Tampered Records: {len(result['tampered_records'])}")
            print(f"   Errors: {len(result['errors'])}")
            
            if result["tampered_records"]:
                print("\n   ⚠️ Tampered Records:")
                for record in result["tampered_records"]:
                    print(f"      - Row {record['row']}: {record.get('expense_id')} "
                          f"({record.get('timestamp')})")
                    print(f"        Stored Hash: {record['stored_hash'][:16]}...")
                    print(f"        Expected Hash: {record['expected_hash'][:16]}...")
            
            if result["errors"]:
                print("\n   💥 Processing Errors:")
                for error in result["errors"]:
                    print(f"      - Row {error['row']}: {error['error']}")
        
        print("=" * 60 + "\n")
    
    @staticmethod
    def export_detailed_report(filename: Optional[str] = None) -> str:
        """
        Export detailed audit report to JSON.
        
        Args:
            filename: Output filename (default: audit_report_TIMESTAMP.json)
            
        Returns:
            Path to exported file
        """
        import os
        from datetime import datetime
        
        records = audit_logger.get_audit_summary(limit=10000)
        integrity_result = audit_logger.verify_integrity()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_report_{timestamp}.json"
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "integrity": integrity_result,
            "total_records": len(records),
            "records": records
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📁 Audit report exported to: {filename}")
        print(f"📁 Audit report exported to: {filename}\n")
        
        return filename


# Create singleton
audit_viewer = AuditLogViewer()
