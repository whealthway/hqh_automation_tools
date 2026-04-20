import tkinter as tk
from controllers.export_controller import export_data_async_login_users
from core.db import get_organisations
from tkinter import ttk
from tkinter import messagebox
import threading
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date


class ExportLoginUsersTab:

    def __init__(self, parent, organisations):
        self.frame = parent

        # Date From - DateEntry
        tk.Label(self.frame, text="Date From").grid(
            row=0, column=0, padx=5, pady=20)
        self.start_date = DateEntry(
            self.frame,
            date_pattern='mm-dd-yyyy',
            width=15,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            state='readonly'
        )
        self.start_date.grid(row=0, column=1, padx=5, pady=10)

        # Set default date
        self.start_date.set_date(date.today() - timedelta(days=7))
        self.start_date.configure(takefocus=False)

        # Date To - DateEntry
        tk.Label(self.frame, text="Date To").grid(
            row=0, column=2, padx=1, pady=20)
        self.end_date = DateEntry(
            self.frame,
            date_pattern='mm-dd-yyyy',
            width=15,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            state='readonly'
        )
        self.end_date.grid(row=0, column=3, padx=5, pady=10)

        # Set default date
        self.end_date.set_date(date.today())
        self.end_date.configure(takefocus=False)

        tk.Label(self.frame, text="Organisation").grid(row=0, column=4, padx=4)
        # Organisations for the dropdown
        options = {org["name"]: org["_id"] for org in organisations}

        def on_select(event):
            # Get selected name
            selected_name = combo.get()
            # Get corresponding code
            self.selected_code = options[selected_name]

        combo = ttk.Combobox(self.frame, values=list(options.keys()), width=50)
        combo.grid(row=0, column=5, padx=10)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.export_btn = tk.Button(
            self.frame,
            text="Export",
            command=self.handle_export,
            width=50,
            bg='#7AC6D2'
        )
        self.export_btn.grid(row=0, column=6, padx=10)

    def handle_export(self):
        # Validate first before disabling
        start_date = datetime.strptime(
            self.start_date.get(), "%m-%d-%Y") - timedelta(days=1)
        utc_start_date = start_date.replace(
            hour=16, minute=0, second=0, microsecond=0)
        end_date = datetime.strptime(self.end_date.get(), "%m-%d-%Y").replace(
            hour=16, minute=0, second=0, microsecond=0)

        orguid = getattr(self, "selected_code", None)

        if not start_date or not end_date or not orguid:
            messagebox.showerror(
                "Input Error", "Please fill up Date From,  Date To, and Organisation")
            return

        self.export_btn.config(state=tk.DISABLED, bg='#d3d3d3')

        filters = {
            "start_date": utc_start_date,
            "end_date": end_date,
            "orguid": orguid
        }

        export_data_async_login_users(filters, self.on_export_done)

    def on_export_done(self, result):
        # Ensure UI thread
        self.frame.after(0, self._update_ui_after_export, result)

    def _update_ui_after_export(self, result):
        self.export_btn.config(state=tk.NORMAL, bg='#7AC6D2')

        if result["status"] == "empty":
            messagebox.showwarning("No Data", "No data found.")
            return

        if result["status"] == "error":
            messagebox.showerror("Error", result["message"])
            return
