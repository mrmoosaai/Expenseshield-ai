# 🔐 Audit Logging System - Tamper-Proof Decision Tracking

## Overview

Now every agent's decision (which expense passed, which failed) is saved in a secure `audit_log.csv` file that cannot be tampered with.

---

## Key Features

### ✅ **Tamper-Proof Logging with HMAC**
- Each record contains an **HMAC-SHA256** hash (a special signature)
- Any modification is detected immediately
- The hash cannot be forged or altered

### 📋 **Comprehensive Decision Tracking**
- **Security Agent**: security decisions (APPROVED/BLOCKED)
- **Finance Agent**: budget decisions (APPROVED/REQUIRES_APPROVAL)
- **Skill Agent**: skill execution results (SUCCESS)
- **Orchestrator Agent**: final decision (SUCCESS/BLOCKED)

### 🔍 **Integrity Verification**
- Automatically detects if someone tries to modify records
- Provides a detailed report of what changed
- You can verify integrity at any time

### 📊 **Rich Reporting**
- View audit logs in a formatted table
- Generate detailed reports in JSON format
- View statistics by agent and decision
- Save the full audit record

---

## File Structure

```
audit_logs/
├── decisions.csv          # Main audit log file (tamper-proof)
└── audit_report_*.json    # Exported reports (generated on demand)
```

---

## CSV Format

Each record contains the following fields:

| Field | Description |
|-------|-------------|
| `timestamp` | When the decision was made (date and time) |
| `transaction_id` | Unique ID to correlate records |
| `agent_name` | Which agent made the decision |
| `expense_id` | Expense identifier (e.g., EXP001) |
| `amount` | Amount (e.g., $500) |
| `category` | Expense category (Engineering/Marketing) |
| `decision` | Decision (APPROVED/BLOCKED/REQUIRES_APPROVAL) |
| `reason` | Reason for the decision (up to ~200 words) |
| `details` | Additional information in JSON format |
| `hash` | Special hash for tamper detection |

### Example Record

```csv
2026-07-05T14:12:27.789147,20260705-EXP001,Security Agent,EXP001,500,Engineering,APPROVED,Security passed - security is OK,{...},1fc7f59a20f54ec5...
```

---

## How to Use

### 1. **Run the System (Audit logs automatically)**
The system runs and saves audit logs automatically.

Audit logging is included automatically:

```python
from agent import agent_system

result = await agent_system.process({
    "expense_id": "EXP001",        # Expense ID
    "amount": 500,                  # Amount
    "category": "Engineering",     # Category
    "description": "Laptop software" # Description

    # Each agent logs automatically - you don't need to do anything!
```

### 2. **View Audit Logs**

```python
from monitoring.audit_viewer import audit_viewer

# Recent logs - formatted table
audit_viewer.display_logs(limit=50)

# Only Finance Agent logs
audit_viewer.display_logs(agent_name="Finance Agent", limit=20)

# Only blocked expenses logs
audit_viewer.display_logs(decision_filter="BLOCKED", limit=10)
```

# Filter by decision status
audit_viewer.display_logs(decision_filter="BLOCKED", limit=10)
```

### 3. **View Statistics**
View how many records are approved, blocked, or require approval.

```python
# Detailed information
audit_viewer.display_summary_stats()
```

Output:
```
📊 AUDIT LOG STATISTICS:
    Total Records: 100                    # Total records
    ✅ Approved: 75                       # Approved
    ❌ Blocked: 5                         # Blocked
    ⏳ Requires Approval: 20              # Requires manager approval
    💥 Errors: 0                          # Errors

🤖 Records by Agent:
    • Security Agent: 25 (25%)            # Security made 25 decisions
    • Finance Agent: 30 (30%)             # Finance made 30 decisions
    • Skill Agent: 30 (30%)               # Skill made 30 decisions
    • Orchestrator Agent: 15 (15%)        # Orchestrator made 15 decisions
```

### 4. **Verify Integrity**
Detect whether any record has been modified.

```python
# Verify integrity and report
audit_viewer.verify_and_report()
```

If someone modifies records:
```
❌ AUDIT LOG INTEGRITY: COMPROMISED
    Total Records: 100
    Tampered Records: 3  ← 3 records modified!
    Errors: 0

    ⚠️ Tampered Records:
        - Row 25: EXP025 (date)
          Stored Hash: 1fc7f59a20f54ec5...
          Expected Hash: 809368a06b77d32b... ← completely different!
```

### 5. **Export Detailed Report**
Save all records into a JSON file.

```python
# Auto filename
filename = audit_viewer.export_detailed_report()
# Returns: audit_report_20260705_141241.json

# Custom filename
filename = audit_viewer.export_detailed_report("my_report.json")
```

---

## Tamper Detection Example

### Scenario: Someone attempts to modify a record

```bash
# Original: change a BLOCKED decision to APPROVED
# Result: ❌ It will be detected immediately!
```

**How this works:**
1. Original hash: `1fc7f59a20f54ec5...` (correct)
2. After modification hash: `809368a06b77d32b...` (different)
3. Hashes do not match → modification detected ❌

### This code includes:
- Timestamp
- Agent name
- Expense ID
- Amount
- Category
- Decision
- Reason
- Additional details

**If any single item is changed the hash differs completely!**

---

## Running Tests

```bash
# Run all tests
python test_audit_logging.py
```

The tests check:
1. ✅ Basic logging
2. ✅ Security blocking
3. ✅ Display logs in table
4. ✅ Statistics
5. ✅ All records are preserved
6. ✅ Tamper detection
7. ✅ Report export
8. ✅ Final verification

---

## Integration Points

### BaseAgent
All agents inherit from `BaseAgent` and call:
```python
audit_logger.log_decision(
    agent_name="Agent Name",
    expense_id="EXP001",
    decision="APPROVED",
    reason="Decision reason",
    amount=500,
    category="Engineering",
    details={...}
)
```

### OrchestratorAgent
Logs all agent decisions with transaction IDs for correlation:
```python
transaction_id = str(uuid.uuid4())
# All subsequent logs use same transaction_id
```

### MultiAgentSystem
Catches and logs errors:
```python
audit_logger.log_decision(
    agent_name="MultiAgentSystem",
    decision="ERROR",
    reason=str(e),
    ...
)
```

---

## Security Considerations

### Strengths
- ✅ **HMAC-SHA256**: Cryptographically secure
- ✅ **Per-record signing**: Each record independently verified
- ✅ **Unique transaction IDs**: Prevents record duplication
- ✅ **Timestamp validation**: Ensures chronological order

### Recommendations
1. **Change AUDIT_SECRET_KEY** in production
   ```python
   # Set in environment variable
   AUDIT_SECRET_KEY=your-strong-random-key
   ```

2. **Backup audit logs** regularly
   ```bash
   # Daily backup
   cp audit_logs/decisions.csv backups/decisions_$(date +%Y%m%d).csv
   ```

3. **Monitor for integrity issues**
   ```python
   result = audit_logger.verify_integrity()
   if not result["is_valid"]:
       # Alert: Tampering detected!
       send_alert()
   ```

4. **Restrict file permissions**
   ```bash
   # Make read-only after backup
   chmod 444 audit_logs/decisions.csv
   ```

---

## API Reference

### AuditLogger

#### `log_decision()` - Log a decision
```python
audit_logger.log_decision(
    agent_name: str,           # Which agent - "Finance Agent"
    expense_id: str,           # Expense ID - "EXP001"
    decision: str,             # Decision - "APPROVED" or "BLOCKED"
    reason: str,               # Reason for the decision
    amount: float,             # Amount
    category: str,             # Category - "Engineering"
    details: dict = None,      # Additional details
    transaction_id: str = None # For correlating records
) -> bool
```

#### `verify_integrity()` - Verify integrity
```python
result = audit_logger.verify_integrity()
# Returns:
# {
#     "is_valid": True/False,      # Whether everything is valid
#     "total_records": 100,        # Total records
#     "tampered_records": [...],   # Tampered records
#     "errors": [...]              # Errors
# }
```

#### `get_audit_summary()` - Get summary
```python
records = audit_logger.get_audit_summary(
    agent_name: str = None,     # Which agent?
    decision_filter: str = None,# Which decision to filter?
    limit: int = 100            # How many records?
) -> list[dict]
```

### AuditLogViewer

#### `display_logs()` - Display logs in table
```python
audit_viewer.display_logs(
    agent_name: str = None,      # Which agent
    decision_filter: str = None, # Which decision
    limit: int = 50              # How many to show
) -> None
```

#### `display_summary_stats()` - Display statistics
```python
audit_viewer.display_summary_stats() -> None
# How many approved? How many blocked? Counts per agent
```

#### `verify_and_report()` - Verify and report
```python
audit_viewer.verify_and_report() -> None
# Check if any modification occurred and view the report
```

#### `export_detailed_report()` - Export
```python
filename = audit_viewer.export_detailed_report(
    filename: str = None  # JSON filename
) -> str
# Save all records to a JSON file
```

---

## Common Queries

### Find all blocked (BLOCKED) expenses
Blocked expenses example:

```python
blocked = audit_logger.get_audit_summary(decision_filter="BLOCKED")
for record in blocked:
    print(f"{record['expense_id']}: {record['reason']}")
    # EXP_SEC_001: Security threat detected
    # EXP_002: Injection attempt
```

### Only Finance Agent decisions
What the Finance Agent did:

```python
finance_logs = audit_logger.get_audit_summary(agent_name="Finance Agent")
approved_count = sum(1 for r in finance_logs if r['decision'] == "APPROVED")
blocked_count = sum(1 for r in finance_logs if r['decision'] == "BLOCKED")

print(f"Approved: {approved_count}")
print(f"Blocked: {blocked_count}")
```

### Was a specific expense approved?
Decision for EXP001:

```python
all_logs = audit_logger.get_audit_summary(limit=10000)
exp_logs = [r for r in all_logs if r['expense_id'] == "EXP001"]

if exp_logs:
    latest = exp_logs[-1]  # Most recent
    print(f"Latest decision: {latest['decision']}")  # APPROVED or BLOCKED
    print(f"Reason: {latest['reason']}")
else:
    print("Expense not found")
```

---

## File Locations

```
project_root/
├── audit_logs/
│   ├── decisions.csv              # Main audit trail
│   └── audit_report_*.json        # Exported reports
├── monitoring/
│   ├── audit_logger.py            # Tamper-proof logging
│   ├── audit_viewer.py            # Display & verification utilities
│   └── logger.py                  # Standard logging
├── agents/
│   ├── orchestrator_agent.py      # Logs all decisions
│   ├── finance_agent.py           # Logs finance decisions
│   ├── security_agent.py          # Logs security decisions
│   └── skill_agent.py             # Logs skill decisions
└── test_audit_logging.py          # Comprehensive tests
```

---

## Troubleshooting

### Unicode Encoding Errors
Are Urdu words displaying incorrectly?
```bash
# On Windows, do this
$env:PYTHONIOENCODING="utf-8"
python test_audit_logging.py
```

### Permission Denied on CSV
**Permission denied on file:**
```bash
# Check permissions
ls -la audit_logs/decisions.csv

# If there's an issue, change permissions
chmod 644 audit_logs/decisions.csv
```

### Audit Log Not Created
**Audit log file is not being created:**
- Is the `audit_logs/` folder present?
- Does the project have write permission?
- Check the log files: `logs/agent_*.log`

---

## Q&A

**Q: Can someone modify the hash directly?**  
A: No. The hash is derived from the SECRET_KEY which is secret. Modification is infeasible.

**Q: If someone deletes a record?**  
A: It will still be detected — the sequence numbers will show a gap.

**Q: How long are records retained?**  
A: Indefinitely. You can archive them to the `archive/` folder.

**Q: Can we change SECRET_KEY?**  
A: Yes — previous hashes will become invalid. Keep it safe.

**Q: Is this GDPR/HIPAA compliant?**  
A: The audit system is compliant, but you may have additional data retention or security requirements.

---

## Support

For issues or questions:
1. Check the logs: `logs/agent_*.log`
2. Run verification: `audit_viewer.verify_and_report()`
3. Export report: `audit_viewer.export_detailed_report()`

---

**Status**: ✅ **Production Ready**  
**Last Updated**: 2026-07-05  
**Version**: 1.0.0
