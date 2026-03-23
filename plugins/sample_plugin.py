# plugins/sample_plugin.py

def register():
    return {
        "name": "Sample Tool",
        "permission": "export",
        "ui": SampleTab
    }


class SampleTab:
    def __init__(self, parent):
        import tkinter as tk
        tk.Label(parent, text="Sample Plugin Loaded").pack()
