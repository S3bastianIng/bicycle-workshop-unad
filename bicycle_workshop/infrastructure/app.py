# -*- coding: utf-8 -*-
"""Composition root: wires the services, login window and main window."""

import customtkinter as ctk

from bicycle_workshop.infrastructure.ui.login_window import LoginWindow
from bicycle_workshop.infrastructure.ui.main_window import BicycleWorkshopApp


def main():
    """Start the application showing the login screen first.

    A single CTk root is reused for the whole app: after a successful login
    the login widgets are cleared and the main system builds on the SAME
    root. Creating a second CTk() after destroying the first one can hang
    CustomTkinter on Windows, so we never do that.
    """
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    app_root = ctk.CTk()

    def open_main_system():
        # clear every login widget, keep the root alive
        for child in app_root.winfo_children():
            child.destroy()
        app_root.title("Bicycle Workshop Control System")
        app_root.geometry("660x560")
        app_root.minsize(660, 560)
        app_root.resizable(False, False)
        BicycleWorkshopApp(app_root)

    LoginWindow(app_root, on_success=open_main_system)
    app_root.mainloop()