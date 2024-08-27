import re
from datetime import datetime

def extract_date(text):
    match = re.search(r"\b\w+ \d{1,2}, \d{4} \d{1,2}:\d{2} \wM\b", text)
    if match:
        date_str = match.group(0)
        date_obj = datetime.strptime(date_str, "%b %d, %Y %I:%M %p")
        return date_obj.strftime("%d/%m/%Y")
    return None

# Ví dụ sử dụng
text = "Account temporarily suspended until May 2, 2024 10:29 AM"
result = extract_date(text)
print(result)  # Sẽ in ra: 02/09/2024
