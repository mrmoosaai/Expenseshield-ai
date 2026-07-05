from pathlib import Path
from email.message import EmailMessage
import os
from datetime import datetime

p = Path.cwd()
pdfs = sorted(p.glob('ExpenseShield_Report_*.pdf'), key=lambda f: f.stat().st_mtime)
if not pdfs:
    print('No ExpenseShield_Report_*.pdf found')
    raise SystemExit(1)
latest = pdfs[-1]
subject = 'Expense Report - Your requested PDF'
body = 'Attached is the expense report you requested.'
eml = EmailMessage()
eml['Subject'] = subject
eml['From'] = os.getenv('SENDER_EMAIL','noreply@example.com')
eml['To'] = os.getenv('MANAGER_EMAIL','you@example.com')
eml.set_content(body)
with open(latest, 'rb') as fh:
    data = fh.read()
eml.add_attachment(data, maintype='application', subtype='pdf', filename=latest.name)
out_path = p / (latest.stem + '.eml')
with open(out_path, 'wb') as f:
    f.write(eml.as_bytes())
print('EML_CREATED:', out_path)
