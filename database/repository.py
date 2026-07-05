"""Repository helpers for persisting expenses and audit logs."""

from database.connection import get_connection
from monitoring.logger import logger


def save_expense(expense_data: dict, result: dict):
    """Persist a processed expense to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO expenses (amount, description, status, reason, llm_used, human_review)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                expense_data.get("amount", 0),
                expense_data.get("description", ""),
                result.get("status", "UNKNOWN"),
                result.get("reason", ""),
                result.get("llm_used", False),
                result.get("human_review", False),
            ),
        )
        conn.commit()
        logger.info(f"💾 Expense saved to DB: ID {cursor.lastrowid}")
        return cursor.lastrowid

    except Exception as e:
        logger.error(f"❌ Error saving expense: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def save_audit_log(event_type: str, details: str, severity: str = "INFO"):
    """Store an audit log entry for system and security events."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO audit_logs (event_type, details, severity)
            VALUES (?, ?, ?)
            """,
            (event_type, details, severity),
        )
        conn.commit()
    except Exception as e:
        logger.error(f"❌ Error saving audit log: {e}")
    finally:
        conn.close()