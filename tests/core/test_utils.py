from unittest import TestCase

from src.core.utils import capitalize_first_letter


class TestUtils(TestCase):
    def test_capitalize_first_letter(self):
        text = "Testing capitalize"
        text_to_test = capitalize_first_letter("testing capitalize")

        assert text == text_to_test
