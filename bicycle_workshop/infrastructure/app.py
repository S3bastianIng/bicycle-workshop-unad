# -*- coding: utf-8 -*-
"""Raíz de composición: conecta los servicios, la ventana de ingreso y la ventana principal."""

import customtkinter as ctk

from bicycle_workshop.infrastructure.ui.login_window import LoginWindow
from bicycle_workshop.infrastructure.ui.main_window import BicycleWorkshopApp


def main():
    """Inicia la aplicación mostrando primero la pantalla de ingreso.

    Se reutiliza una única raíz CTk durante toda la aplicación: tras un
    ingreso exitoso se eliminan los componentes de ingreso y el sistema
    principal se construye sobre la MISMA raíz. Crear un segundo CTk()
    después de destruir el primero puede bloquear CustomTkinter en Windows,
    por lo cual nunca se hace.
    """
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    app_root = ctk.CTk()

    def open_main_system():
        # elimina todos los componentes de ingreso y mantiene viva la raíz
        for child in app_root.winfo_children():
            child.destroy()
        app_root.title("Bicycle Workshop Control System")
        app_root.geometry("660x560")
        app_root.minsize(660, 560)
        app_root.resizable(False, False)
        BicycleWorkshopApp(app_root)

    LoginWindow(app_root, on_success=open_main_system)
    app_root.mainloop()
