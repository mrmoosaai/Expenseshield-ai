"""
Tamper-proof audit logging system with HMAC integrity verification.
Har agent ka decision ek audit log mein save hota hai jo change nahi ho sakta.
"""

import csv
import os
import hashlib
import hmac
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from monitoring.logger import logger

# Security key for HMAC (in production, use environment variable)
AUDIT_SECRET_KEY = os.getenv("AUDIT_SECRET_KEY", "expense-shield-audit-key-2026").encode()
AUDIT_LOG_DIR = "audit_logs"
AUDIT_LOG_FILE = os.path.join(AUDIT_LOG_DIR, "decisions.csv")
AUDIT_INTEGRITY_FILE = os.path.join(AUDIT_LOG_DIR, ".integrity")


class AuditLogger:
    """Tamper-proof audit logging system."""
    
    CSV_HEADERS = [
        "timestamp",
        "transaction_id",
        "agent_name",
        "expense_id",
        "amount",
        "category",
        "decision",
        "reason",
        "details",
        "hash"
    ]
    
    @staticmethod
    def _ensure_audit_dir():
        """Create audit directory if it doesn't exist."""
        Path(AUDIT_LOG_DIR).mkdir(exist_ok=True)
    
    @staticmethod
    def _compute_hash(row_dict: Dict[str, str]) -> str:
        """
        Compute HMAC hash for a row to detect tampering.
        """
        # Create a consistent string representation (excluding hash field)
        row_data = {k: v for k, v in row_dict.items() if k != "hash"}
        row_string = json.dumps(row_data, sort_keys=True)
        
        # Compute HMAC-SHA256
        hash_obj = hmac.new(
            AUDIT_SECRET_KEY,
            row_string.encode(),
            hashlib.sha256
        )
        return hash_obj.hexdigest()
    
    @staticmethod
    def log_decision(
        agent_name: str,
        expense_id: str,
        decision: str,  # "APPROVED", "BLOCKED", "REQUIRES_APPROVAL"
        reason: str,
        amount: float,
        category: str = "General",
        details: Optional[Dict[str, Any]] = None,
        transaction_id: Optional[str] = None
    ) -> bool:
        """
        Log an agent decision to the audit trail.
        
        Args:
            agent_name: Name of the agent making decision
            expense_id: Unique expense identifier
            decision: Decision status (APPROVED/BLOCKED/REQUIRES_APPROVAL/ERROR)
            reason: Why this decision was made
            amount: Expense amount
            category: Expense category
            details: Additional context as dict
            transaction_id: Optional unique transaction ID for correlation
            
        Returns:
            bool: True if logged successfully, False otherwise
        """
        try:
            AuditLogger._ensure_audit_dir()
            
            # Generate transaction ID if not provided
            if not transaction_id:
                transaction_id = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{expense_id}"
            
            timestamp = datetime.now().isoformat()
            details_str = json.dumps(details) if details else "{}"
            
            # Create row
            row = {
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "agent_name": agent_name,
                "expense_id": expense_id,
                "amount": str(amount),
                "category": category,
                "decision": decision,
                "reason": reason[:200],  # Truncate to 200 chars
                "details": details_str,
                "hash": ""
            }
            
            # Compute and add hash
            row["hash"] = AuditLogger._compute_hash(row)
            
            # Append to CSV
            file_exists = os.path.exists(AUDIT_LOG_FILE)
            with open(AUDIT_LOG_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=AuditLogger.CSV_HEADERS)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(row)
            
            logger.info(
                f"📋 Audit logged: {agent_name} → {decision} "
                f"(Expense: {expense_id}, Amount: ${amount})"
            )
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Audit logging failed: {e}", exc_info=True)
            return False
    
    @staticmethod
    def verify_integrity() -> Dict[str, Any]:
        """
        Verify if audit log has been tampered with.
        
        Returns:
            Dict with verification results:
            {
                "is_valid": bool,
                "total_records": int,
                "tampered_records": list,
                "errors": list
            }
        """
        try:
            AuditLogger._ensure_audit_dir()
            
            if not os.path.exists(AUDIT_LOG_FILE):
                return {
                    "is_valid": True,
                    "total_records": 0,
                    "tampered_records": [],
                    "errors": []
                }
            
            tampered_records = []
            errors = []
            total_records = 0
            
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    try:
                        total_records += 1
                        
                        stored_hash = row.get("hash", "")
                        computed_hash = AuditLogger._compute_hash(row)
                        
                        if stored_hash != computed_hash:
                            tampered_records.append({
                                "row": row_num,
                                "expense_id": row.get("expense_id"),
                                "timestamp": row.get("timestamp"),
                                "stored_hash": stored_hash,
                                "expected_hash": computed_hash
                            })
                    except Exception as e:
                        errors.append({
                            "row": row_num,
                            "error": str(e)
                        })
            
            is_valid = len(tampered_records) == 0 and len(errors) == 0
            
            result = {
                "is_valid": is_valid,
                "total_records": total_records,
                "tampered_records": tampered_records,
                "errors": errors
            }
            
            if not is_valid:
                logger.warning(
                    f"⚠️ Audit log integrity issue detected! "
                    f"Tampered: {len(tampered_records)}, Errors: {len(errors)}"
                )
            else:
                logger.info(f"✅ Audit log verified: {total_records} records are intact")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Integrity verification failed: {e}", exc_info=True)
            return {
                "is_valid": False,
                "total_records": 0,
                "tampered_records": [],
                "errors": [str(e)]
            }
    
    @staticmethod
    def get_audit_summary(
        agent_name: Optional[str] = None,
        decision_filter: Optional[str] = None,
        limit: int = 100
    ) -> list:
        """
        Get audit log summary with optional filters.
        
        Args:
            agent_name: Filter by agent name
            decision_filter: Filter by decision status
            limit: Maximum records to return
            
        Returns:
            List of audit records
        """
        try:
            AuditLogger._ensure_audit_dir()
            
            if not os.path.exists(AUDIT_LOG_FILE):
                return []
            
            records = []
            
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Apply filters
                    if agent_name and row.get("agent_name") != agent_name:
                        continue
                    if decision_filter and row.get("decision") != decision_filter:
                        continue
                    
                    records.append(row)
                    
                    if len(records) >= limit:
                        break
            
            return records
            
        except Exception as e:
            logger.error(f"❌ Failed to get audit summary: {e}")
            return []


# Singleton instance
audit_logger = AuditLogger()
