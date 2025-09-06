from datetime import date, datetime
from typing import Optional

def parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()
