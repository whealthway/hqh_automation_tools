import tkinter as tk
from tkinter import ttk


class SearchableCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._values = self["values"]
        self.bind("<KeyRelease>", self._on_keyrelease)

    def set_values(self, values):
        self._values = values
        self["values"] = values

    def _on_keyrelease(self, event):
        value = self.get().lower()

        if value == '':
            data = self._values
        else:
            data = [item for item in self._values if value in item.lower()]

        self["values"] = data


# Sample usage
root = tk.Tk()

tk.Label(root, text="Select Item").pack()

combo = SearchableCombobox(root)
combo.set_values([
    "Apple", "Banana", "Orange", "Grapes", "Mango", "Pineapple"
])
combo.pack(pady=10)

root.mainloop()
