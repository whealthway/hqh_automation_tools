import tkinter as tk
from controllers.export_controller import export_data_async_login_users
from core.db import get_organisations
from tkinter import ttk
from tkinter import messagebox
import threading
from tkcalendar import DateEntry
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExportLoginUsersTab:

    def __init__(self, parent):
        self.frame = parent

        tk.Label(self.frame, text="Date From").grid(
            row=0, column=0, padx=5, pady=20)
        start_date = DateEntry(self.frame, date_pattern='mm-dd-yyyy')
        start_date.grid(row=0, column=1, padx=5, pady=20)
        start_date.set_date(datetime.today())

        tk.Label(self.frame, text="Date To").grid(
            row=0, column=2, padx=1, pady=20)
        end_date = DateEntry(self.frame, date_pattern='mm-dd-yyyy')
        end_date.grid(row=0, column=3, padx=3)
        end_date.set_date(datetime.today() - relativedelta(days=7))

        tk.Label(self.frame, text="Organisation").grid(row=0, column=4, padx=4)
        # Organisations for the dropdown
        organisations = get_organisations()
        options = {org["name"]: org["_id"] for org in organisations}

        def on_select(event):
            # Get selected name
            selected_name = combo.get()
            # Get corresponding code
            self.selected_code = options[selected_name]
            print(
                f"Selected: {selected_name}, Code for query: {self.selected_code}")

        combo = ttk.Combobox(self.frame, values=list(options.keys()), width=50)
        combo.grid(row=0, column=5, padx=10)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.export_btn = tk.Button(
            self.frame,
            text="Export",
            command=self.handle_export,
            width=50,
            bg='#7AC6D2',
        )
        self.export_btn.grid(row=0, column=6, padx=10)

    def handle_export(self):
        # Validate first before disabling
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        if not start_date or not end_date:
            messagebox.showerror(
                "Input Error", "Please fill up Date From and Date To")
            return

        self.export_btn.config(state=tk.DISABLED)

        filters = {
            "start_date": start_date,
            "end_date": end_date
        }

        # Run in background thread
        threading.Thread(
            target=self.run_export,
            args=(filters,),
            daemon=True
        ).start()

    def run_export(self, filters):
        try:
            print(filters)
            export_data_async_login_users(filters)

        except Exception as e:
            print("Error:", e)

        finally:
            print("Export process completed.")

            # Re-enable button safely in main thread
            self.frame.after(
                0,
                lambda: self.export_btn.config(state=tk.NORMAL)
            )
