import re
from datetime import datetime


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
    

# def is_valid_date(date, format):
#     try:
#         date = datetime.strptime(date, format)
#         return True
#     except ValueError:
#         return False
#
def is_valid_date(date, formats):
    result = False
    for format in formats:
        try:
            date = datetime.strptime(date, format)
            result = True
        except ValueError:
            pass
    return result
