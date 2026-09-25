# -*- coding: utf-8 -*-
"""Unit tests for the application services: LoginService and WorkshopService."""

import unittest

from bicycle_workshop.application.services import LoginService, WorkshopService
from bicycle_workshop.domain.entities import BicicletaTaller


class LoginServiceTest(unittest.TestCase):
    """Tests for the LoginService use case."""

    def setUp(self):
        self.service = LoginService()

    def test_validate_with_correct_credentials(self):
        self.assertTrue(self.service.validate("programacion", "programacion"))

    def test_validate_with_correct_credentials_ignoring_extra_spaces(self):
        self.assertTrue(
            self.service.validate(" programacion ", " programacion "))

    def test_validate_with_wrong_password(self):
        self.assertFalse(self.service.validate("programacion", "wrong"))

    def test_validate_with_wrong_username(self):
        self.assertFalse(self.service.validate("wrong", "programacion"))

    def test_validate_with_blank_inputs(self):
        self.assertFalse(self.service.validate("", ""))
        self.assertFalse(self.service.validate("   ", "   "))


class WorkshopServiceTest(unittest.TestCase):
    """Tests for the WorkshopService use case."""

    def setUp(self):
        self.service = WorkshopService()

    # -- register_bicycle ---------------------------------------------------

    def test_register_bicycle_with_empty_serial(self):
        with self.assertRaisesRegex(ValueError, "serial number"):
            self.service.register_bicycle("", "10", "09:00")

    def test_register_bicycle_with_invalid_cost(self):
        with self.assertRaisesRegex(ValueError, "positive number"):
            self.service.register_bicycle("S1", "abc", "09:00")

    def test_register_bicycle_with_zero_cost(self):
        with self.assertRaisesRegex(ValueError, "positive number"):
            self.service.register_bicycle("S1", "0", "09:00")

    def test_register_bicycle_with_invalid_entry_time(self):
        with self.assertRaises(ValueError):
            self.service.register_bicycle("S1", "10", "25:00")

    def test_register_bicycle_with_valid_data_returns_and_appends(self):
        bike = self.service.register_bicycle("S1", "10.0", "09:00")
        self.assertIsInstance(bike, BicicletaTaller)
        self.assertEqual(len(self.service.bicycles), 1)
        self.assertIs(self.service.bicycles[0], bike)

    def test_register_bicycle_does_not_auto_select(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.assertIsNone(self.service.selected_index)

    # -- select_bicycle -----------------------------------------------------

    def test_select_bicycle_sets_selected_index(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.service.register_bicycle("S2", "12.5", "08:00")
        self.service.select_bicycle(1)
        self.assertEqual(self.service.selected_index, 1)

    # -- calculate_total ----------------------------------------------------

    def test_calculate_total_without_selection(self):
        with self.assertRaisesRegex(ValueError, "select a bicycle"):
            self.service.calculate_total("10:00")

    def test_calculate_total_with_selection_and_valid_exit(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.service.select_bicycle(0)
        self.assertEqual(self.service.calculate_total("10:30"), 15.0)

    def test_calculate_total_with_empty_exit_time(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.service.select_bicycle(0)
        with self.assertRaisesRegex(ValueError, "exit time"):
            self.service.calculate_total("")

    def test_calculate_total_with_exit_earlier_than_entry(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.service.select_bicycle(0)
        with self.assertRaises(ValueError):
            self.service.calculate_total("08:00")

    # -- remove_current -----------------------------------------------------

    def test_remove_current_removes_bicycle_and_resets_selection(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.service.select_bicycle(0)
        self.service.remove_current()
        self.assertEqual(len(self.service.bicycles), 0)
        self.assertIsNone(self.service.selected_index)

    def test_remove_current_without_selection_does_nothing(self):
        self.service.register_bicycle("S1", "10.0", "09:00")
        self.service.remove_current()
        self.assertEqual(len(self.service.bicycles), 1)
        self.assertIsNone(self.service.selected_index)


if __name__ == "__main__":
    unittest.main()
