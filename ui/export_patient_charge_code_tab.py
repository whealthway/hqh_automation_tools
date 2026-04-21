import tkinter as tk
from controllers.export_controller import export_data_async_patient_charges
from core.db import get_organisations
from tkinter import ttk
from tkinter import messagebox
import math


class ExportPatientChargesTab:

    def __init__(self, parent, organisations):
        self.frame = parent
        self.frame.grid_rowconfigure(2, weight=1)  # table row expands
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        tk.Label(self.frame, text="VisitID").grid(
            row=0, column=0, padx=5, pady=20)
        self.visit_id = tk.Entry(self.frame, width=50)
        self.visit_id.grid(row=0, column=1, padx=5, pady=20)

        tk.Label(self.frame, text="Organisation").grid(
            row=0, column=2, padx=5, pady=20)
        # Organisations for the dropdown
        options = {org["name"]: org["_id"] for org in organisations}

        def on_select(event):
            # Get selected name
            selected_name = combo.get()
            # Get corresponding code
            self.selected_code = options[selected_name]

        combo = ttk.Combobox(self.frame, values=list(options.keys()), width=50)
        combo.grid(row=0, column=3, padx=5, pady=20)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.export_btn = tk.Button(
            self.frame,
            text="Export",
            command=self.handle_export,
            width=50,
            bg='#7AC6D2'
        )
        self.export_btn.grid(row=0, column=4, padx=5, pady=20)

        self.search_entry = tk.Entry(self.frame, width=50)
        self.search_entry.grid(row=1, column=1)

        self.search_btn = tk.Button(
            self.frame, text="Apply", command=self.apply_filter)
        self.search_btn.grid(row=1, column=2)

        self.reset_btn = tk.Button(
            self.frame, text="Reset", command=self.reset_filter)
        self.reset_btn.grid(row=1, column=3)

        self.prev_btn = tk.Button(
            self.frame, text="<< Prev", command=self.prev_page)
        self.prev_btn.grid(row=5, column=1)

        self.next_btn = tk.Button(
            self.frame, text="Next >>", command=self.next_page)
        self.next_btn.grid(row=5, column=3)

        tk.Label(self.frame, text="Search").grid(row=1, column=0)

        self.page_size = 100
        self.current_page = 0

    def handle_export(self):
        visitid = self.visit_id.get()
        orguid = getattr(self, "selected_code", None)

        if not visitid or not orguid:
            messagebox.showerror(
                "Input Error", "Please fill in both VisitID and Organisation.")
            return

        self.export_btn.config(state=tk.DISABLED, bg='#d3d3d3')

        filters = {
            "visitid": visitid,
            "orguid": orguid
        }

        export_data_async_patient_charges(filters, self.on_export_done)

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

        df = result["data"]

        # ✅ STORE ORIGINAL + LIMITED VIEW
        self.original_df = df
        self.full_df = df.head(500)  # limit UI load

        self.current_page = 0  # reset pagination

        # ✅ Render table (uses self.full_df)
        self.render_table()

        # ✅ Show summary (use FULL dataset, not limited)
        self.display_summary(
            result["total_netamount"],
            result["df_billed_amount"],
            result["df_unbilled_amount"]
        )

        messagebox.showinfo(
            "Export Successful",
            f"Data exported to {result['file']}"
        )

    def display_table(self, df):
        # Store full dataset
        self.full_df = df
        self.current_page = 0
        self.page_size = 100  # adjustable

        self.render_table()

    def render_table(self):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        if hasattr(self, "scrollbar_x"):
            self.scrollbar_x.destroy()
            del self.scrollbar_x

        self.table_frame = tk.Frame(self.frame)
        self.table_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")

        # ✅ Configure expansion
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        start = self.current_page * self.page_size
        end = start + self.page_size
        df_page = self.full_df.iloc[start:end]

        # Treeview
        self.tree = ttk.Treeview(self.table_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar
        scrollbar_y = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar (parent frame is OK to use grid)
        if not hasattr(self, "scrollbar_x"):
            self.scrollbar_x = ttk.Scrollbar(
                self.frame, orient="horizontal", command=self.tree.xview
            )
            self.scrollbar_x.grid(row=3, column=0, columnspan=5, sticky="ew")

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        # Columns
        self.tree["columns"] = list(df_page.columns)
        self.tree["show"] = "headings"

        for col in df_page.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="w", stretch=False)

        self.tree.tag_configure("odd", background="#f2f2f2")
        self.tree.tag_configure("even", background="white")

        for i, (_, row) in enumerate(df_page.iterrows()):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=list(row), tags=(tag,))

    def render_table_old(self):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        self.table_frame = tk.Frame(self.frame)
        self.table_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        start = self.current_page * self.page_size
        end = start + self.page_size
        df_page = self.full_df.iloc[start:end]

        self.tree = ttk.Treeview(self.table_frame)
        # self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        if not hasattr(self, "scrollbar_x"):
            self.scrollbar_x = ttk.Scrollbar(
                self.frame, orient="horizontal", command=self.tree.xview)
            self.scrollbar_x.grid(row=3, column=0, columnspan=5, sticky="ew")

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        self.tree["columns"] = list(df_page.columns)
        self.tree["show"] = "headings"

        for col in df_page.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w", stretch=True)

        self.tree.tag_configure("odd", background="#f2f2f2")
        self.tree.tag_configure("even", background="white")

        for i, (_, row) in enumerate(df_page.iterrows()):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=list(row), tags=(tag,))

        # ✅ FIX: correct total pages
        total_pages = max(1, math.ceil(len(self.full_df) / self.page_size))

        if hasattr(self, "page_label"):
            self.page_label.destroy()

        self.page_label = tk.Label(
            self.frame,
            text=f"Page {self.current_page + 1} of {total_pages}"
        )
        self.page_label.grid(row=5, column=2)

    def display_summary(self, total_netamount, df_billed_amount, df_unbilled_amount):
        if hasattr(self, "summary_label"):
            self.summary_label.destroy()

        text = (
            f"Total Net Amount: {total_netamount:,.2f}\n"
            f"Billed Amount: {df_billed_amount:,.2f}\n"
            f"Unbilled Amount: {df_unbilled_amount:,.2f}"
        )

        self.summary_label = tk.Label(
            self.frame,
            text=text,
            fg="blue",
            justify="left",
            font=("Arial", 10, "bold")
        )
        self.summary_label.grid(row=4, column=0, columnspan=5, pady=10)

    def next_page(self):
        import math
        total_pages = math.ceil(len(self.full_df) / self.page_size)

        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.render_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_table()

    def apply_filter(self):
        keyword = self.search_entry.get().lower()

        if not keyword:
            return

        df = self.original_df  # ✅ FIX: always use original

        filtered = df[df.apply(
            lambda row: row.astype(
                str).str.lower().str.contains(keyword).any(),
            axis=1
        )]

        self.full_df = filtered.head(500)  # ✅ keep UI safe
        self.current_page = 0

        self.render_table()

    def reset_filter(self):
        self.full_df = self.original_df.head(500)  # ✅ reapply limit
        self.current_page = 0
        self.render_table()
