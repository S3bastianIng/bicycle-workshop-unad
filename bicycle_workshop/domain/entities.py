# -*- coding: utf-8 -*-
"""Domain entities: Usuario and BicicletaTaller (pure business logic, no GUI).

Logic copied exactly from the original single-file assignment; only the
GUI-adjacent docstrings were touched.
"""


class Usuario:
    """Represents a system user with private credentials.

    Attributes:
        _usuario (str): private username
        _password (str): private password

    Methods:
        validar(usuario_ingresado, password_ingresada): returns True only
        when both credentials match the stored values.
    """

    def __init__(self, usuario="programacion", password="programacion"):
        self._usuario = usuario
        self._password = password

    def validar(self, usuario_ingresado, password_ingresada):
        """Return True only if the given credentials match."""
        return self._usuario == usuario_ingresado and self._password == password_ingresada


class BicicletaTaller:
    """Represents a bicycle that enters a workshop for maintenance.

    Attributes:
        _serial (str): bicycle serial number (private)
        _hora_ingreso (float): time the bicycle entered, in 24h format
                               converted to minutes (private)
        _costo_por_hora (float): rate charged per hour (private)

    Methods:
        registrar_ingreso(hora): stores the entry time
        registrar_salida(hora): registers the exit time
        calcular_total(hora_salida): computes the final cost
        obtener_serial(): returns the bicycle serial number
    """

    def __init__(self, serial, costo_por_hora):
        self._serial = serial
        self._hora_ingreso = None
        self._costo_por_hora = costo_por_hora

    # -- helpers ------------------------------------------------------------

    @staticmethod
    def _to_minutes(time_str):
        """Convert a 'HH:MM' string into total minutes (int).

        Raises:
            ValueError: when the format is not valid.
        """
        try:
            parts = time_str.strip().split(":")
            if len(parts) != 2:
                raise ValueError
            hours = int(parts[0])
            minutes = int(parts[1])
            if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
                raise ValueError
            return hours * 60 + minutes
        except (ValueError, TypeError):
            raise ValueError(
                "Invalid time format. Use HH:MM in 24-hour format "
                "(e.g. 09:30 or 14:05)."
            )

    # -- public methods -----------------------------------------------------

    def registrar_ingreso(self, hora):
        """Store the entry time of the bicycle."""
        self._hora_ingreso = self._to_minutes(hora)

    def registrar_salida(self, hora):
        """Register the exit time of the bicycle.

        Validates that the exit time is greater than the entry time.
        """
        if self._hora_ingreso is None:
            raise ValueError("No entry time registered for this bicycle.")

        exit_time = self._to_minutes(hora)

        if exit_time <= self._hora_ingreso:
            raise ValueError(
                "Exit time must be greater than the entry time."
            )

        return exit_time

    def calcular_total(self, hora_salida):
        """Calculate the final cost of the maintenance service.

        Cost = elapsed hours * cost per hour.
        """
        exit_time = self.registrar_salida(hora_salida)
        elapsed_hours = (exit_time - self._hora_ingreso) / 60.0
        return round(elapsed_hours * self._costo_por_hora, 2)

    def obtener_serial(self):
        """Return the bicycle serial number."""
        return self._serial

    def obtener_hora_ingreso(self):
        """Return the entry time as a HH:MM string (for display)."""
        if self._hora_ingreso is None:
            return "--:--"
        h = self._hora_ingreso // 60
        m = self._hora_ingreso % 60
        return f"{h:02d}:{m:02d}"

    def obtener_costo_por_hora(self):
        """Return the cost per hour."""
        return self._costo_por_hora
