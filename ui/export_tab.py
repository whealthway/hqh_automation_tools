import tkinter as tk
from controllers.export_controller import export_data_async
from core.db import get_organisations
from tkinter import ttk
from tkinter import messagebox
import threading


class ExportTab:

    def __init__(self, parent):
        self.frame = parent

        tk.Label(self.frame, text="VisitID").grid(
            row=0, column=0, padx=5, pady=20)
        self.visit_id = tk.Entry(self.frame, width=50)
        self.visit_id.grid(row=0, column=1, padx=5, pady=20)

        tk.Label(self.frame, text="Organisation").grid(
            row=0, column=2, padx=5, pady=20)
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
        combo.grid(row=0, column=3, padx=5, pady=20)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.export_btn = tk.Button(
            self.frame,
            text="Export",
            command=self.handle_export,
            width=50
        )
        self.export_btn.grid(row=0, column=4, padx=5, pady=20)

        # self.progress = ttk.Progressbar(
        #     self.frame,
        #     orient="horizontal",
        #     length=300,
        #     mode="indeterminate"
        # )
        # self.progress.pack(pady=10)

    # def handle_export(self):
    #     self.export_btn.config(state=tk.DISABLED)

    #     try:
    #         filters = {
    #             "visitid": self.visit_id.get(),
    #             "orguid": self.selected_code
    #         }
    #         print(filters)

    #         if not filters["visitid"] and not filters["orguid"]:
    #             messagebox.showerror(
    #                 "Input Error", "Please fill in both VisitID and Organisation.")
    #         else:
    #             export_data_async(filters)

    #     except Exception as e:
    #         print("Error:", e)

    #     finally:
    #         print("Export process completed.")
    #         self.export_btn.config(state=tk.NORMAL)

    def stop_ui(self):
        self.progress.stop()
        self.export_btn.config(state=tk.NORMAL)

    def handle_export(self):
        # Validate first before disabling
        visitid = self.visit_id.get()
        orguid = getattr(self, "selected_code", None)

        if not visitid or not orguid:
            messagebox.showerror(
                "Input Error", "Please fill in both VisitID and Organisation.")
            return

        # Disable button
        self.export_btn.config(state=tk.DISABLED)

        # Start loading animation
        self.progress.start(10)

        filters = {
            "visitid": visitid,
            "orguid": orguid
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
            export_data_async(filters)

        except Exception as e:
            print("Error:", e)

        finally:
            print("Export process completed.")
            # Stop progress bar safely in main thread
            self.frame.after(0, self.stop_ui)

            # Re-enable button safely in main thread
            self.frame.after(
                0,
                lambda: self.export_btn.config(state=tk.NORMAL)
            )
