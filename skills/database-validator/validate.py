"""
SQL Schema Validator
Validates SQL schemas against company policies
"""

import sys
import re

def validate_schema(filename):
    """
    Validates SQL schema file:
    1. Table names must be snake_case
    2. Every table must have 'id' PRIMARY KEY
    3. No DROP TABLE statements allowed
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        errors = []
        
        # Check 1: No DROP TABLE
        if re.search(r'DROP TABLE', content, re.IGNORECASE):
            errors.append("ERROR: DROP TABLE statements are forbidden")
        
        # Check 2 & 3: CREATE TABLE validation
        table_defs = re.finditer(
            r'CREATE TABLE\s+(?P<name>\w+)\s*\((?P<body>.*?)\);',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        for match in table_defs:
            table_name = match.group('name')
            body = match.group('body')
            
            # Snake case check
            if not re.match(r'^[a-z][a-z0-9_]*$', table_name):
                errors.append(f"ERROR: Table '{table_name}' must be snake_case")
            
            # Primary key check
            if not re.search(r'\bid\b.*PRIMARY KEY', body, re.IGNORECASE):
                errors.append(f"ERROR: Table '{table_name}' missing 'id' PRIMARY KEY")
        
        if errors:
            for err in errors:
                print(err)
            sys.exit(1)
        else:
            print("✓ Schema validation passed")
            sys.exit(0)
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate.py <schema_file>")
        sys.exit(1)
    
    validate_schema(sys.argv[1])