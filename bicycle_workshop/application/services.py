# -*- coding: utf-8 -*-
"""Servicios de aplicación (casos de uso): Python puro, sin dependencias de GUI.

Estas clases contienen el estado y las reglas de la aplicación a los que
la GUI (vista) delega. Nunca deben importar tkinter ni customtkinter.
"""

from bicycle_workshop.domain.entities import BicicletaTaller, Usuario


class LoginService:
    """Caso de uso: validar las credenciales de ingreso."""

    def __init__(self, user=None):
        """Crea el servicio, usando un ``Usuario`` por defecto cuando no se indica uno."""
        self.user = user if user is not None else Usuario()

    def validate(self, username, password):
        """Retorna True solo para credenciales no vacías que coinciden.

        Las entradas se normalizan sin espacios en los extremos; las
        credenciales vacías nunca se validan.
        """
        username = (username or "").strip()
        password = (password or "").strip()
        if not username or not password:
            return False
        return self.user.validar(username, password)


class WorkshopService:
    """Caso de uso: gestionar las bicicletas registradas en el taller."""

    def __init__(self):
        self.bicycles = []          # lista interna de objetos BicicletaTaller
        self.selected_index = None  # índice de la bicicleta seleccionada actualmente

    def register_bicycle(self, serial, cost_str, entry_time_str):
        """Registra una nueva bicicleta en el taller.

        Lanza:
            ValueError: cuando el número de serie está vacío, el costo no es
                un número positivo o la hora de ingreso no es válida.

        En caso de éxito, la nueva bicicleta se agrega y se retorna. NO se
        selecciona automáticamente.
        """
        serial = serial.strip()
        if not serial:
            raise ValueError("Please enter the serial number.")

        try:
            cost = float(cost_str.strip())
            if cost <= 0:
                raise ValueError
        except ValueError:
            raise ValueError(
                "The cost per hour must be a positive number.")

        bike = BicicletaTaller(serial, cost)
        # la validación de la hora de ingreso se delega al mensaje propio de BicicletaTaller
        bike.registrar_ingreso(entry_time_str.strip())

        self.bicycles.append(bike)
        return bike

    def select_bicycle(self, index):
        """Marca como seleccionada la bicicleta ubicada en ``index``."""
        self.selected_index = index

    def calculate_total(self, exit_time_str):
        """Calcula el costo total de la bicicleta seleccionada.

        Lanza:
            ValueError: cuando no hay bicicleta seleccionada, la hora de
                salida está vacía o la hora de salida no es válida
                (delegado a la entidad).
        """
        if self.selected_index is None:
            raise ValueError("Please select a bicycle from the list.")

        exit_time_str = exit_time_str.strip()
        if not exit_time_str:
            raise ValueError("Please enter the exit time (HH:MM).")

        bike = self.bicycles[self.selected_index]
        return bike.calcular_total(exit_time_str)

    def remove_current(self):
        """Elimina la bicicleta seleccionada y restablece la selección."""
        if self.selected_index is None:
            return
        self.bicycles.pop(self.selected_index)
        self.selected_index = None
