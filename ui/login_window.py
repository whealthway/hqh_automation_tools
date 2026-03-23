import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import login_user
from models import user
from ui.main_window import MainWindow


class LoginWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("1260x780")

        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()

        self.dummy_users = [
            {
                "username": "clarvin",
                "password": "password123",
                "roles": ["corp", "sbu"]
            },
            {
                "username": "dondie",
                "password": "password123",
                "roles": ["sbu"]
            }
        ]

    def login(self):
        # user = login_user(self.username.get(), self.password.get())
        user = {}
        # is_username_valid = self.username.get(
        # ) in [u["username"] for u in self.dummy_users]
        # is_password_valid = self.password.get(
        # ) in [u["password"] for u in self.dummy_users]
        for u in self.dummy_users:
            if u["username"] == self.username.get() and u["password"] == self.password.get():
                user = u
                break
        if user:
            self.root.destroy()
            # messagebox.showinfo("Success", "Login successful!")
            print(f"user: {user}")
            MainWindow(user).run()
        else:
            messagebox.showerror("Error", "Invalid login")

    def run(self):
        self.root.mainloop()
