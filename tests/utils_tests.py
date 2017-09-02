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
