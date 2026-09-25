# -*- coding: utf-8 -*-
"""Unit tests for the domain entities: Usuario and BicicletaTaller."""

import unittest

from bicycle_workshop.domain.entities import BicicletaTaller, Usuario


class UsuarioTest(unittest.TestCase):
    """Tests for the Usuario login entity."""

    def setUp(self):
        self.user = Usuario()

    def test_validar_with_correct_credentials(self):
        self.assertTrue(self.user.validar("programacion", "programacion"))

    def test_validar_with_wrong_password(self):
        self.assertFalse(self.user.validar("programacion", "wrong"))

    def test_validar_with_wrong_usuario(self):
        self.assertFalse(self.user.validar("wrong", "programacion"))

    def test_validar_with_empty_strings(self):
        self.assertFalse(self.user.validar("", ""))


class BicicletaTallerTest(unittest.TestCase):
    """Tests for the BicicletaTaller time/cost entity."""

    # -- _to_minutes / registrar_ingreso -----------------------------------

    def test_to_minutes_with_valid_time(self):
        self.assertEqual(BicicletaTaller._to_minutes("09:30"), 570)

    def test_to_minutes_with_invalid_hour(self):
        with self.assertRaises(ValueError):
            BicicletaTaller._to_minutes("25:00")

    def test_to_minutes_with_invalid_minute(self):
        with self.assertRaises(ValueError):
            BicicletaTaller._to_minutes("09:60")

    def test_to_minutes_with_non_time_string(self):
        with self.assertRaises(ValueError):
            BicicletaTaller._to_minutes("abc")

    def test_to_minutes_with_unpadded_hour_accepted(self):
        self.assertEqual(BicicletaTaller._to_minutes("9:30"), 570)

    def test_registrar_ingreso_with_valid_time(self):
        bike = BicicletaTaller("S1", 10.0)
        bike.registrar_ingreso("09:30")
        self.assertEqual(bike.obtener_hora_ingreso(), "09:30")

    # -- registrar_salida ----------------------------------------------------

    def test_registrar_salida_without_ingreso(self):
        bike = BicicletaTaller("S1", 10.0)
        with self.assertRaises(ValueError):
            bike.registrar_salida("10:00")

    def test_registrar_salida_earlier_than_ingreso(self):
        bike = BicicletaTaller("S1", 10.0)
        bike.registrar_ingreso("09:00")
        with self.assertRaises(ValueError):
            bike.registrar_salida("08:00")

    def test_registrar_salida_equal_to_ingreso(self):
        bike = BicicletaTaller("S1", 10.0)
        bike.registrar_ingreso("09:00")
        with self.assertRaises(ValueError):
            bike.registrar_salida("09:00")

    def test_registrar_salida_valid_returns_minutes(self):
        bike = BicicletaTaller("S1", 10.0)
        bike.registrar_ingreso("09:00")
        self.assertEqual(bike.registrar_salida("10:30"), 630)

    # -- calcular_total / obtener_serial -------------------------------------

    def test_calcular_total_hour_and_a_half(self):
        bike = BicicletaTaller("S1", 10.0)
        bike.registrar_ingreso("09:00")
        self.assertEqual(bike.calcular_total("10:30"), 15.0)

    def test_calcular_total_exact_hour(self):
        bike = BicicletaTaller("S1", 12.5)
        bike.registrar_ingreso("08:00")
        self.assertEqual(bike.calcular_total("09:00"), 12.5)

    def test_obtener_serial_returns_serial(self):
        bike = BicicletaTaller("SN-001", 5.0)
        self.assertEqual(bike.obtener_serial(), "SN-001")


if __name__ == "__main__":
    unittest.main()
