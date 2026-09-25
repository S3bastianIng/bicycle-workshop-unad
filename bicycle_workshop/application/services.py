# -*- coding: utf-8 -*-
"""Application services (use cases): plain Python, no GUI dependencies.

These classes own the application state and rules that the GUI (view)
delegates to. They must never import tkinter or customtkinter.
"""

from bicycle_workshop.domain.entities import BicicletaTaller, Usuario


class LoginService:
    """Use case: validate login credentials."""

    def __init__(self, user=None):
        """Create the service, using a default ``Usuario`` when none is given."""
        self.user = user if user is not None else Usuario()

    def validate(self, username, password):
        """Return True only for non-empty credentials that match.

        Inputs are stripped; blank credentials never validate.
        """
        username = (username or "").strip()
        password = (password or "").strip()
        if not username or not password:
            return False
        return self.user.validar(username, password)


class WorkshopService:
    """Use case: manage the bicycles registered in the workshop."""

    def __init__(self):
        self.bicycles = []          # internal list of BicicletaTaller objects
        self.selected_index = None  # index of the currently selected bicycle

    def register_bicycle(self, serial, cost_str, entry_time_str):
        """Register a new bicycle in the workshop.

        Raises:
            ValueError: when the serial is empty, the cost is not a
                positive number, or the entry time is invalid.

        On success the new bicycle is appended and returned. It is NOT
        auto-selected.
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
        # entry time validation delegates to BicicletaTaller's own message
        bike.registrar_ingreso(entry_time_str.strip())

        self.bicycles.append(bike)
        return bike

    def select_bicycle(self, index):
        """Mark the bicycle at ``index`` as selected."""
        self.selected_index = index

    def calculate_total(self, exit_time_str):
        """Calculate the total cost for the selected bicycle.

        Raises:
            ValueError: when no bicycle is selected, the exit time is
                empty, or the exit time is invalid (delegated to the
                entity).
        """
        if self.selected_index is None:
            raise ValueError("Please select a bicycle from the list.")

        exit_time_str = exit_time_str.strip()
        if not exit_time_str:
            raise ValueError("Please enter the exit time (HH:MM).")

        bike = self.bicycles[self.selected_index]
        return bike.calcular_total(exit_time_str)

    def remove_current(self):
        """Remove the selected bicycle and reset the selection."""
        if self.selected_index is None:
            return
        self.bicycles.pop(self.selected_index)
        self.selected_index = None
