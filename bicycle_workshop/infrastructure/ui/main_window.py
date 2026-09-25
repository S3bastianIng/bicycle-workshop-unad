# -*- coding: utf-8 -*-
"""Main system window (CustomTkinter UI) - depends on WorkshopService only."""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from bicycle_workshop.application.services import WorkshopService


class BicycleWorkshopApp:
    """Main window of the bicycle control system (CustomTkinter)."""

    def __init__(self, root, service=None):
        self.root = root
        self.service = service if service is not None else WorkshopService()

        root.title("Bicycle Workshop Control System")
        root.geometry("660x560")
        root.minsize(660, 560)
        root.resizable(False, False)

        # -- header ----------------------------------------------------------
        header = ctk.CTkFrame(root, fg_color="#1b5e20", corner_radius=0,
                              height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="\U0001F6B2  Bicycle Workshop Control "
                                  "System",
                     text_color="white",
                     font=ctk.CTkFont("Segoe UI", 15, "bold")).pack(
            side="left", padx=16)

        # -- registration frame --------------------------------------------
        register_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="white")
        register_frame.pack(fill="x", padx=14, pady=(14, 8))

        ctk.CTkLabel(register_frame, text="Register Bicycle",
                     text_color="#1b5e20",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=14, pady=(10, 4))

        fields = ctk.CTkFrame(register_frame, fg_color="transparent")
        fields.pack(fill="x", padx=14, pady=(0, 12))

        # serial
        ctk.CTkLabel(fields, text="Serial number:", text_color="#37474f",
                     font=ctk.CTkFont("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", padx=(0, 6))
        self.serial_var = tk.StringVar()
        ctk.CTkEntry(fields, textvariable=self.serial_var, width=150,
                     height=34, corner_radius=6).grid(
            row=0, column=1, sticky="w", padx=(0, 12), pady=3)

        # cost
        ctk.CTkLabel(fields, text="Cost per hour (USD):",
                     text_color="#37474f",
                     font=ctk.CTkFont("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=(0, 6))
        self.cost_var = tk.StringVar()
        ctk.CTkEntry(fields, textvariable=self.cost_var, width=150,
                     height=34, corner_radius=6).grid(
            row=1, column=1, sticky="w", padx=(0, 12), pady=3)

        # entry time
        ctk.CTkLabel(fields, text="Entry time (HH:MM):",
                     text_color="#37474f",
                     font=ctk.CTkFont("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", padx=(0, 6))
        self.entry_time_var = tk.StringVar()
        ctk.CTkEntry(fields, textvariable=self.entry_time_var, width=150,
                     height=34, corner_radius=6).grid(
            row=2, column=1, sticky="w", padx=(0, 12), pady=3)

        ctk.CTkButton(fields, text="Register Entry",
                      command=self._register_bicycle,
                      fg_color="#2e7d32", hover_color="#388e3c",
                      height=38, corner_radius=8,
                      font=ctk.CTkFont("Segoe UI", 11, "bold")).grid(
            row=0, column=2, rowspan=3, padx=(12, 0))

        # -- bicycles list frame -------------------------------------------
        list_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="white")
        list_frame.pack(fill="both", expand=True, padx=14, pady=8)

        ctk.CTkLabel(list_frame, text="Bicycles in Workshop",
                     text_color="#1b5e20",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=14, pady=(10, 4))

        # a scrollable container where each bicycle is a selectable row
        self.list_container = ctk.CTkScrollableFrame(
            list_frame, fg_color="#f5f7f5", corner_radius=8)
        self.list_container.pack(fill="both", expand=True, padx=14,
                                 pady=(0, 12))

        ctk.CTkLabel(list_frame, text="No bicycles registered yet.",
                     text_color="#90a4ae",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(
            side="bottom", pady=(0, 8))

        # -- exit frame ------------------------------------------------------
        exit_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="white")
        exit_frame.pack(fill="x", padx=14, pady=(8, 14))

        ctk.CTkLabel(exit_frame, text="Register Exit",
                     text_color="#1b5e20",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=14, pady=(10, 4))

        exit_row = ctk.CTkFrame(exit_frame, fg_color="transparent")
        exit_row.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkLabel(exit_row, text="Exit time (HH:MM):",
                     text_color="#37474f",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(side="left")
        self.exit_time_var = tk.StringVar()
        ctk.CTkEntry(exit_row, textvariable=self.exit_time_var, width=100,
                     height=34, corner_radius=6).pack(side="left", padx=8)

        ctk.CTkButton(exit_row, text="Calculate Total",
                      command=self._calculate_total,
                      fg_color="#2e7d32", hover_color="#388e3c",
                      height=36, corner_radius=8,
                      font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(
            side="left", padx=8)

        self.total_label = ctk.CTkLabel(exit_row, text="Total:  $0.00",
                                        text_color="#1b5e20",
                                        font=ctk.CTkFont(
                                            "Segoe UI", 13, "bold"))
        self.total_label.pack(side="right", padx=(8, 4))

        # -- EXIT APP BUTTON (modern outline, discreet) ----------------------
        exit_app_frame = ctk.CTkFrame(root, fg_color="transparent")
        exit_app_frame.pack(fill="x", padx=14, pady=(0, 14))

        ctk.CTkButton(exit_app_frame, text="Exit",
                      command=lambda: self.root.destroy(),
                      fg_color="transparent", hover_color="#f0f2f0",
                      text_color="#546e7a", width=96, height=34,
                      corner_radius=8, border_width=1,
                      border_color="#b0bec5",
                      font=ctk.CTkFont("Segoe UI", 11)).pack(side="right")

    # -- actions ------------------------------------------------------------

    def _refresh_list(self):
        """Rebuild the selectable rows from the current bicycle list."""
        for widget in self.list_container.winfo_children():
            widget.destroy()

        if not self.service.bicycles:
            ctk.CTkLabel(self.list_container,
                         text="No bicycles registered yet.",
                         text_color="#90a4ae",
                         font=ctk.CTkFont("Segoe UI", 10)).pack(
                pady=14)
            return

        for idx, bike in enumerate(self.service.bicycles):
            row_text = (f"Serial: {bike.obtener_serial():<12} | "
                        f"In: {bike.obtener_hora_ingreso()} | "
                        f"$ {bike.obtener_costo_por_hora():.2f}/h")
            is_selected = (idx == self.service.selected_index)
            row = ctk.CTkButton(
                self.list_container, text=row_text, anchor="w",
                command=lambda i=idx: self._select_bike(i),
                fg_color=("#2e7d32" if is_selected else "transparent"),
                hover_color="#c8e6c9",
                text_color=("white" if is_selected else "#263238"),
                height=34, corner_radius=6,
                font=ctk.CTkFont("Consolas", 10))
            row.pack(fill="x", pady=2, padx=2)

    def _select_bike(self, index):
        """Highlight the selected bicycle row."""
        self.service.select_bicycle(index)
        self._refresh_list()

    def _register_bicycle(self):
        """Delegate registration to the service and refresh the list."""
        serial = self.serial_var.get().strip()
        cost_str = self.cost_var.get().strip()
        entry_time = self.entry_time_var.get().strip()

        try:
            self.service.register_bicycle(serial, cost_str, entry_time)
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        self._refresh_list()

        self.serial_var.set("")
        self.cost_var.set("")
        self.entry_time_var.set("")

    def _calculate_total(self):
        """Calculate and show the total cost for the selected bicycle."""
        exit_time = self.exit_time_var.get().strip()

        try:
            total = self.service.calculate_total(exit_time)
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        bike = self.service.bicycles[self.service.selected_index]
        self.total_label.configure(text=f"Total:  ${total:.2f}")
        messagebox.showinfo(
            "Service Completed",
            f"Bicycle {bike.obtener_serial()}\n"
            f"Entry time: {bike.obtener_hora_ingreso()}\n"
            f"Exit time:  {exit_time}\n"
            f"Total cost: ${total:.2f}"
        )

        # remove the bike from the workshop list once the service is done
        self.service.remove_current()
        self.total_label.configure(text="Total:  $0.00")
        self._refresh_list()
        self.exit_time_var.set("")