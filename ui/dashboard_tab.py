import tkinter as tk
from services.dashboard_service import get_export_count


class DashboardTab:

    def __init__(self, parent):
        self.frame = parent

        self.label = tk.Label(self.frame, text="Loading...")
        self.label.pack(pady=20)

        self.refresh()

    def refresh(self):
        count = get_export_count()
        self.label.config(text=f"Total Exports: {count}")
