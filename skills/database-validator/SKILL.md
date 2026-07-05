---
name: database-validator
description: Validates SQL schema files for compliance with internal safety and naming policies. Use this when user needs to validate database schemas.
version: 1.0
author: Moosa AI
---

# Database Schema Validator Skill

## Goal
SQL schemas ko validate karna company policies ke against.

## Policies Enforced
1. **Safety**: No DROP TABLE statements
2. **Naming**: All tables must use snake_case
3. **Structure**: Every table must have 'id' PRIMARY KEY

## Instructions
1. User ka SQL file lo
2. If the user provides an invalid SQL file format, respond with: "Please provide a valid SQL file."
3. Validation script run karo:
   ```bash
   python scripts/validate.py <schema_file>
   ## Examples

### Example 1: Valid Schema
**Input:** `users.sql`
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50)
);