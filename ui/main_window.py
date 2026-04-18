import os
import sys

import tkinter as tk
from tkinter import ttk

from core.auth import has_permission
from core.plugin_loader import load_plugins

# Built-in Tabs
from ui.export_tab import ExportTab
# from ui.dashboard_tab import DashboardTab
from ui.export_login_users import ExportLoginUsersTab
# from ui.user_tab import UserTab  # Uncomment when ready


class MainWindow:

    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Automation Tool")
        self.root.geometry("1260x780")

        self._build_ui()

    def _build_ui(self):
        # ✅ APPLY STYLE HERE (after root, before widgets)
        style = ttk.Style(self.root)
        style.theme_use("clam")  # better for color control

        style.configure(
            "TNotebook.Tab",
            background="lightgray",
            foreground="black",
            padding=[10, 5]
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", "#3D90D7")],
            foreground=[("selected", "white")]
        )

        # ===== TOP HEADER =====
        header = tk.Frame(self.root, bg="#3A59D1", height=50)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Dev Tool Dashboard",
            font=("Arial", 14, "bold"),
            bg=header.cget("bg"),
            fg='white'
        )
        title.pack(side="left", padx=10)

        self.export_btn = tk.Button(
            header,
            text="Logout",
            command=self.handle_logout,
            width=10,
            bg="#3A59FF",
            fg='white'
        )
        self.export_btn.pack(side="right", padx=10)

        user_label = tk.Label(
            header,
            text=f"Logged in as: {self.user['username']}",
            bg=header.cget("bg"),
            fg='white'
        )
        user_label.pack(side="right", padx=10)

        # ===== MAIN CONTENT (TABS) =====
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(container, height=25)
        self.notebook.pack(fill="both", expand=True)

        # ===== BUILT-IN TABS =====
        self._load_builtin_tabs()

        # ===== PLUGINS =====
        self._load_plugins()

    # -----------------------------------
    # Built-in Tabs (Role-based)
    # -----------------------------------
    def _load_builtin_tabs(self):

        # Export Tab
        if has_permission(self.user, "export"):
            frame = tk.Frame(self.notebook)
            frame.pack(fill="x", pady=10)
            ExportTab(frame, self.user['organisations'])
            self.notebook.add(
                frame, text="Export Patient Orders")

        if has_permission(self.user, "sbu_export"):
            frame = tk.Frame(self.notebook)
            frame.pack(fill="x", pady=10)
            ExportLoginUsersTab(frame, self.user['organisations'])
            self.notebook.add(frame, text="Export Login Users")

        # # Dashboard Tab
        # if has_permission(self.user, "dashboard"):
        #     frame = tk.Frame(self.notebook)
        #     DashboardTab(frame)
        #     self.notebook.add(frame, text="Dashboard")

        # # Users Tab (optional future)
        # # if has_permission(self.user, "users"):
        # try:
        #     from ui.user_tab import UserTab
        #     frame = tk.Frame(self.notebook)
        #     UserTab(frame)
        #     self.notebook.add(frame, text="Users")
        # except ImportError:
        #     print("UserTab not implemented yet")

    # -----------------------------------
    # Plugin Tabs (Dynamic)
    # -----------------------------------
    def _load_plugins(self):
        try:
            plugins = load_plugins()

            for plugin in plugins:
                try:
                    name = plugin.get("name")
                    permission = plugin.get("permission")
                    ui_class = plugin.get("ui")

                    # Check permission
                    if permission and not has_permission(self.user, permission):
                        continue

                    frame = tk.Frame(self.notebook)
                    ui_class(frame)  # Initialize plugin UI
                    self.notebook.add(frame, text=name)

                except Exception as e:
                    print(f"Error loading plugin {plugin}: {e}")

        except Exception as e:
            print("Plugin loading failed:", e)

    def handle_logout(self):
        self.root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    # -----------------------------------
    # Run App
    # -----------------------------------
    def run(self):
        self.root.mainloop()
