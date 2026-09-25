# -*- coding: utf-8 -*-
"""Ventana de ingreso (interfaz CustomTkinter); depende solo de LoginService."""

import tkinter as tk

import customtkinter as ctk

from bicycle_workshop.application.services import LoginService


class LoginWindow:
    """Ingreso moderno y dinámico construido con CustomTkinter: diseño de dos
    paneles, campos con subrayado, error en línea, efecto de vibración y
    estado de carga."""

    BRAND = "#1b5e20"
    BRAND_ACCENT = "#2e7d32"
    BG = "#f5f7f5"
    ERROR = "#c62828"

    def __init__(self, root, on_success, service=None):
        self.root = root
        self.on_success = on_success
        self.service = service if service is not None else LoginService()

        root.title("Bicycle Workshop - Login")
        root.geometry("760x420")
        root.minsize(760, 420)
        root.resizable(False, False)

        # -- contenedor global ------------------------------------------------
        container = ctk.CTkFrame(root, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # =================================================================
        # IZQUIERDA: panel de marca
        # =================================================================
        brand = ctk.CTkFrame(container, fg_color=self.BRAND,
                             corner_radius=0, width=300)
        brand.pack(side="left", fill="y")
        brand.pack_propagate(False)

        ctk.CTkLabel(brand, text="\U0001F6B2", font=("Segoe UI Emoji", 64),
                     text_color="white").pack(pady=(56, 0))

        ctk.CTkLabel(brand, text="Bicycle Workshop",
                     text_color="white",
                     font=ctk.CTkFont("Segoe UI", 20, "bold")).pack(
            pady=(8, 0))
        ctk.CTkLabel(brand, text="Control System",
                     text_color="#c8e6c9",
                     font=ctk.CTkFont("Segoe UI", 13)).pack()
        ctk.CTkLabel(brand,
                     text="Fast, safe and automatic\ncontrol of your workshop",
                     text_color="#a5d6a7",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(pady=(18, 0))

        # =================================================================
        # DERECHA: panel de formulario
        # =================================================================
        form = ctk.CTkFrame(container, fg_color=self.BG, corner_radius=0)
        form.pack(side="left", fill="both", expand=True)

        # botón discreto Exit en la esquina superior derecha del formulario
        top_row = ctk.CTkFrame(form, fg_color="transparent")
        top_row.pack(fill="x", padx=48, pady=(18, 0))
        ctk.CTkButton(top_row, text="Exit",
                      command=lambda: self.root.destroy(),
                      fg_color="transparent", hover_color="#eceff1",
                      text_color="#546e7a", width=64, height=30,
                      corner_radius=6, border_width=1, border_color="#b0bec5",
                      font=ctk.CTkFont("Segoe UI", 10)).pack(side="right")

        ctk.CTkLabel(form, text="Sign in",
                     text_color="#263238",
                     font=ctk.CTkFont("Segoe UI", 24, "bold")).pack(
            anchor="w", padx=48, pady=(16, 0))
        ctk.CTkLabel(form, text="Enter your credentials to access the system.",
                     text_color="#607d8b",
                     font=ctk.CTkFont("Segoe UI", 11)).pack(
            anchor="w", padx=48, pady=(2, 24))

        # nombre de usuario (estilo con subrayado: campo transparente + línea inferior)
        ctk.CTkLabel(form, text="Username", text_color="#37474f",
                     font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=48)
        self._underline_entry(form, "username", "Enter your username",
                              secret=False, pady=(2, 22))

        # contraseña (estilo con subrayado: campo transparente + línea inferior)
        ctk.CTkLabel(form, text="Password", text_color="#37474f",
                     font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=48)
        self._underline_entry(form, "password", "Enter your password",
                              secret=True, pady=(2, 2))

        # interruptor para mostrar u ocultar la contraseña
        self.show_pwd = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(form, text="Show password", variable=self.show_pwd,
                        command=self._toggle_password, corner_radius=6,
                        text_color="#455a64",
                        font=ctk.CTkFont("Segoe UI", 10),
                        fg_color=self.BRAND_ACCENT,
                        hover_color="#388e3c").pack(
            anchor="w", padx=48, pady=(10, 4))

        # etiqueta de error en línea (oculta por defecto)
        self.error_label = ctk.CTkLabel(form, text="", text_color=self.ERROR,
                                        font=ctk.CTkFont("Segoe UI", 10,
                                                         "bold"))
        self.error_label.pack(anchor="w", padx=48, pady=(0, 6))

        # botón Sign In (dinámico: resaltado + estado de carga)
        self.signin_btn = ctk.CTkButton(
            form, text="Sign In", command=self._validate_credentials,
            fg_color=self.BRAND_ACCENT, hover_color="#388e3c",
            text_color="white", height=44, corner_radius=8,
            font=ctk.CTkFont("Segoe UI", 14, "bold"))
        self.signin_btn.pack(fill="x", padx=48, pady=(2, 0))

        # sugerencia discreta en el pie
        ctk.CTkLabel(form,
                     text="Default credentials: programacion / programacion",
                     text_color="#90a4ae",
                     font=ctk.CTkFont("Segoe UI", 9)).pack(
            side="bottom", pady=(0, 14))

        root.bind("<Return>", lambda _e: self._validate_credentials())

    # -- auxiliares ----------------------------------------------------------

    def _underline_entry(self, parent, name, placeholder, secret, pady):
        """Crea un campo transparente con solo una línea inferior (estilo con
        subrayado). La línea se vuelve verde cuando el campo recibe el foco.

        NOTA: no se usa ``placeholder_text`` nativo. Se ha observado que el
        mecanismo de marcador de CustomTkinter omite pulsaciones de teclas y
        bloquea la ventana en Windows, por lo cual los campos inician vacíos;
        las etiquetas estáticas "Username"/"Password" ya explican los campos.
        """
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(fill="x", padx=48, pady=pady)

        entry = ctk.CTkEntry(
            wrapper, height=30,
            fg_color="transparent", border_width=0,
            corner_radius=0,
            text_color="#263238")
        entry.pack(fill="x")

        # el subrayado es un marco delgado ubicado justo debajo del campo
        line = ctk.CTkFrame(wrapper, height=2,
                            fg_color="#b0bec5", corner_radius=0)
        line.pack(fill="x", pady=(0, 0))

        if secret:
            entry.configure(show="*")
            self.password_var = tk.StringVar()
            entry.configure(textvariable=self.password_var)
            self.password_entry = entry
        else:
            self.username_var = tk.StringVar()
            entry.configure(textvariable=self.username_var)
            self.username_entry = entry

        def on_focus_in(_event=None):
            line.configure(fg_color="#2e7d32")

        def on_focus_out(_event=None):
            line.configure(fg_color="#b0bec5")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<KeyRelease>", self._on_type)

    # -- comportamiento dinámico ---------------------------------------------

    def _on_type(self, _event=None):
        # borra el error en línea tan pronto como el usuario vuelve a escribir.
        # NOTA: nunca se vuelve a asociar el evento aquí; reasociar
        # <KeyRelease> en cada pulsación interfiere con las asociaciones
        # internas de CustomTkinter y puede bloquear la ventana en Windows.
        if self.error_label.cget("text"):
            self.error_label.configure(text="")

    def _toggle_password(self):
        if self.show_pwd.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    # -- validación ----------------------------------------------------------

    def _validate_credentials(self):
        """Validación dinámica: vibración + error en línea ante un fallo;
        estado de carga y transición ante el éxito."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if self.service.validate(username, password):
            self._grant_access()
        else:
            if not username or not password:
                self._show_error(
                    "Please enter your username and password.")
                return
            self._show_error(
                "Invalid username or password. Please try again.")
            self.password_var.set("")
            self._shake()

    def _show_error(self, message):
        self.error_label.configure(text=message)

    def _shake(self):
        """Pequeña animación horizontal para indicar un ingreso fallido."""
        x, y = self.root.winfo_x(), self.root.winfo_y()
        for delta in (0, 6, -6, 4, -4, 0):
            self.root.geometry(f"760x420+{x + delta}+{y}")
            self.root.update_idletasks()

    def _grant_access(self):
        """Breve estado de carga y luego entrega el control al sistema principal."""
        self.signin_btn.configure(text="Signing in...", state="disabled",
                                  fg_color="#388e3c")
        self.root.update_idletasks()
        self.root.after(500, self._open_main)

    def _open_main(self):
        # NO se destruye la raíz de la aplicación aquí: CustomTkinter puede
        # bloquearse en Windows cuando se crea un nuevo CTk() después de
        # destruir el anterior. Se devuelve la MISMA raíz activa a main().
        self.on_success()
