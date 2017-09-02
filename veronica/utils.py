from datetime import datetime

def get_date_from_string(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return None

def get_fancy_date(dt):
    fmt = '%B %d, %Y'
    return dt.strftime(fmt)

def get_age(birth_date, more_recent_date):
    try:
        years = more_recent_date.year - birth_date.year - \
                ((more_recent_date.month, more_recent_date.day) < \
                 (birth_date.month, birth_date.day))
        return "{y} years old".format(y=years)
    except AttributeError:
        return "I cannot tell how old"
