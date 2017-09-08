import unittest
import datetime
from veronica import utils

class UtilsTests(unittest.TestCase):
    def test_get_date_from_string_returns_valid_date(self):
        """utils - you get a good date from a good string"""
        sut = utils.get_date_from_string('2017-01-01')
        expected = datetime.datetime(2017, 1, 1, 0, 0)
        self.assertEqual(sut, expected)

    def test_get_date_from_string_returns_none_from_invalid_date(self):
        """utils - you get None from a bad string"""
        sut = utils.get_date_from_string('foo')
        self.assertEqual(sut, None)

    def test_get_fancy_date_gives_you_something_fancy(self):
        """utils - given a date, get_fancy_date gives you fancy"""
        sut = utils.get_fancy_date(datetime.datetime(1967, 9, 30, 0, 0))
        expected = 'September 30, 1967'
        self.assertEqual(sut, expected)

    def test_get_age_returns_elaborate_age_string(self):
        """utils - a valid age returns an elaborate age string"""
        today = datetime.datetime(2017, 1, 1, 0, 0)
        birthdate = datetime.datetime(1967, 9, 30, 0, 0)
        sut = utils.get_age(birthdate, today)
        expected = "49 years old"
        self.assertEqual(sut, expected)

    def test_get_age_returns_error_message_when_given_invalid_date(self):
        """utils - invalid age returns an error string"""
        today = datetime.datetime(2017, 1, 1, 0, 0)
        birthdate = 'foo'
        sut = utils.get_age(birthdate, today)
        expected = "I cannot tell how old"
        self.assertEqual(sut, expected)

    def test_env_vars_can_munge_into_map(self):
        """utils - valid env var can be extracted into data"""
        env_var = "Ted:1967-09-30,Alice:1969-04-21"
        teds_date = datetime.datetime(1967, 9, 30, 0, 0)
        alices_date = datetime.datetime(1969, 4, 21, 0, 0)

        expected = {'1': ('Ted', teds_date),
                    '2': ('Alice', alices_date)}
        sut = utils.get_structure_from_env(env_var)
        self.assertEqual(sut, expected)

    def test_env_vars_can_handle_empty_values(self):
        """utils - given empty value, get_structure_from_env returns None"""
        sut = utils.get_structure_from_env('')
        self.assertIsNone(sut)

    def test_get_structure_from_env_handles_bad_env_var(self):
        """utils - invalid age returns an error string"""
        env_var = 'foo'
        self.assertIsNone(utils.get_structure_from_env(env_var))

    def test_get_structure_from_env_handles_bad_env_var(self):
        """utils - invalid age returns an error string"""
        env_var = 'foo'
        self.assertIsNone(utils.get_structure_from_env(env_var))

    def test_get_welcome_from_dict_returns_sensible_menu_msg(self):
        """utils - given a useful map, a useful message can be delivered"""
        teds_date = datetime.datetime(1967, 9, 30, 0, 0)
        alices_date = datetime.datetime(1969, 4, 21, 0, 0)

        family = {'1': ('Bob', teds_date),
                  '2': ('Alice', alices_date)}
        sut = utils.get_welcome_from_map(family)
        expected = 'Please press 1 and then the pound sign for Bob' \
                   +' or 2 for Alice'
        self.assertEqual(sut, expected)

    def test_get_next_birthday_returns_sensible_msg_for_future_birthday(self):
        """utils - happy path for future birthday"""
        teds_date = datetime.datetime(1967, 9, 30, 0, 0)
        todays_date = datetime.datetime(2017, 9, 6, 0, 0)
        sut = utils.get_next_birthday(teds_date, todays_date)
        self.assertEqual(sut, (0, 24))

    def test_get_next_birthday_handles_leap_year_coming_up(self):
        """utils - can handle leap year a few days away"""
        teds_date = datetime.datetime(1996, 2, 29, 0, 0)
        todays_date = datetime.datetime(2017, 2, 18, 0, 0)
        sut = utils.get_next_birthday(teds_date, todays_date)
        self.assertEqual(sut, (0, 10))

    def test_get_next_birthday_handles_leap_year_just_passed(self):
        """utils - can handle leap year day just passed"""
        teds_date = datetime.datetime(1996, 2, 29, 0, 0)
        todays_date = datetime.datetime(2017, 3, 1, 0, 0)
        sut = utils.get_next_birthday(teds_date, todays_date)
        self.assertEqual(sut, (12, 4))

    def test_next_birthday_message_formats_the_message(self):
        """utils - happy path for next birthday messages"""
        expected = 'About 0 months and 24 days until their next birthday'
        sut = utils.get_next_birthday_message(0, 24)
        self.assertEqual(sut, expected)
