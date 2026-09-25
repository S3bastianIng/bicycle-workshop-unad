# -*- coding: utf-8 -*-
"""Entidades de dominio: Usuario y BicicletaTaller (lógica pura de negocio, sin GUI).

Lógica copiada exactamente de la asignación original de un solo archivo; solo
se ajustaron las cadenas de documentación cercanas a la GUI.
"""


class Usuario:
    """Representa un usuario del sistema con credenciales privadas.

    Atributos:
        _usuario (str): nombre de usuario privado
        _password (str): contraseña privada

    Métodos:
        validar(usuario_ingresado, password_ingresada): retorna True solo
        cuando ambas credenciales coinciden con los valores almacenados.
    """

    def __init__(self, usuario="programacion", password="programacion"):
        self._usuario = usuario
        self._password = password

    def validar(self, usuario_ingresado, password_ingresada):
        """Retorna True solo si las credenciales indicadas coinciden."""
        return self._usuario == usuario_ingresado and self._password == password_ingresada


class BicicletaTaller:
    """Representa una bicicleta que ingresa al taller para mantenimiento.

    Atributos:
        _serial (str): número de serie de la bicicleta (privado)
        _hora_ingreso (float): hora de ingreso de la bicicleta, en formato
                               de 24 horas convertida a minutos (privado)
        _costo_por_hora (float): tarifa cobrada por hora (privado)

    Métodos:
        registrar_ingreso(hora): almacena la hora de ingreso
        registrar_salida(hora): registra la hora de salida
        calcular_total(hora_salida): calcula el costo final
        obtener_serial(): retorna el número de serie de la bicicleta
    """

    def __init__(self, serial, costo_por_hora):
        self._serial = serial
        self._hora_ingreso = None
        self._costo_por_hora = costo_por_hora

    # -- auxiliares ----------------------------------------------------------

    @staticmethod
    def _to_minutes(time_str):
        """Convierte una cadena 'HH:MM' a minutos totales (int).

        Lanza:
            ValueError: cuando el formato no es válido.
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

    # -- métodos públicos ----------------------------------------------------

    def registrar_ingreso(self, hora):
        """Almacena la hora de ingreso de la bicicleta."""
        self._hora_ingreso = self._to_minutes(hora)

    def registrar_salida(self, hora):
        """Registra la hora de salida de la bicicleta.

        Valida que la hora de salida sea posterior a la hora de ingreso.
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
        """Calcula el costo final del servicio de mantenimiento.

        Costo = horas transcurridas * costo por hora.
        """
        exit_time = self.registrar_salida(hora_salida)
        elapsed_hours = (exit_time - self._hora_ingreso) / 60.0
        return round(elapsed_hours * self._costo_por_hora, 2)

    def obtener_serial(self):
        """Retorna el número de serie de la bicicleta."""
        return self._serial

    def obtener_hora_ingreso(self):
        """Retorna la hora de ingreso como cadena HH:MM (para mostrar)."""
        if self._hora_ingreso is None:
            return "--:--"
        h = self._hora_ingreso // 60
        m = self._hora_ingreso % 60
        return f"{h:02d}:{m:02d}"

    def obtener_costo_por_hora(self):
        """Retorna el costo por hora."""
        return self._costo_por_hora
