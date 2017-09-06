from datetime import datetime

import sys
import logging

logging.basicConfig(
    format="%(levelname)-10s %(asctime)s %(filename)s %(lineno)d %(message)s",
    level=logging.DEBUG
)

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

def get_records_from_env(env_var):
    if env_var is None or len(env_var) == 0:
        return None

    rows = env_var.split(',')
    cells = map(lambda x: x.split(':'), rows)

    cell_lengths = set([len(c) for c in cells])
    cells_are_uniform = len(cell_lengths) == 1
    cell_length_is_two = list(cell_lengths)[-1] == 2

    if cells_are_uniform and cell_length_is_two:
        return cells
    else:
        return None


def get_structure_from_env(env_var):
    cells = get_records_from_env(env_var)
    if cells is None:
        return None
    else:
        formatted = map(lambda x: (x[0], get_date_from_string(x[1])), cells)

        indices = map(str, range(1, len(formatted) + 1))
        indexed = zip(indices, formatted)

        return {i: r for (i, r) in indexed}


def get_welcome_from_map(family):
    press = 'Please press'
    pound_sign = 'and then the pound sign'

    # pop off first member;
    # you need to copy the dict so that the
    # original dict isn't altered
    d = dict(family)
    first_key = d.keys()[0]
    first = "{number} {pound} for {person}".format(number=first_key,
                                                   pound=pound_sign,
                                                   person=d[first_key][0])
    del d[first_key]
    pieces = ['or {num} for {n}'.format(num=k, n=v[0]) \
              for k, v in d.iteritems()]

    final = '{press} {first} {rest}'.format(press=press,
                                            first=first,
                                            rest=' '.join(pieces))
    return final


def next_birthday(birthday, today):
    try:
        next_birthday = birthday.replace(year=today.year)
    except ValueError:
        # not a leapyear, no february 29th; use the day before
        next_birthday = birthday.replace(day=28, year=today.year)

    if next_birthday < today:  # next year
        try:
            next_birthday = birthday.replace(year=today.year + 1)
        except ValueError:
            # not a leapyear, no february 29th, use the day before
            next_birthday = birthday.replace(day=28, year=today.year + 1)

    difference = next_birthday - today
    months, days = divmod(difference.days, 30)  # assume 30 days per month
    return 'About {} months and {} days until their next birthday'.format(months, days)
