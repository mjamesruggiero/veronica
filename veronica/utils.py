from datetime import datetime

def get_date_from_string(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return None

def get_fancy_date(dt):
    fmt = '%B %d, %Y'
    return dt.strftime(fmt)
