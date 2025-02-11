import re
from datetime import datetime

def extract_amount(notification: str) -> float:
    # Look for UGX followed by amount
    amount_match = re.search(r'UGX\s*([\d,]+)', notification)
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '')
        return float(amount_str)
    raise ValueError("Could not extract amount from notification")

def extract_date(notification: str) -> datetime:
    # Look for date pattern
    date_match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', notification)
    if date_match:
        return datetime.strptime(date_match.group(1), '%Y-%m-%d %H:%M')
    raise ValueError("Could not extract date from notification")

def extract_description(notification: str) -> str:
    # Look for transaction description after "Description:"
    desc_match = re.search(r'Transaction Description:\s*([^\n]+)', notification)
    if desc_match:
        return desc_match.group(1).strip()
    raise ValueError("Could not extract description from notification")
