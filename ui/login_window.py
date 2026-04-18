import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import login_user, verify_code
from ui.main_window import MainWindow
from tkinter import Toplevel


class LoginWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("1260x780")

        # ===== TOP HEADER =====
        header = tk.Frame(self.root, bg="#3A59D1", height=50)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="HQMN Dev Tool",
            font=("Arial", 14, "bold"),
            bg=header.cget("bg"),
            fg='white'
        )
        title.pack(side="left", padx=10)

        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root, width=40)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*", width=40)
        self.password.pack()

        tk.Button(self.root, text="Login",
                  command=self.login, width=36, bg='#7AC6D2').pack(pady=20)

        self.logged_user = None
        self.modal = None

    def open_modal(self):
        self.modal = Toplevel(self.root)
        self.modal.title("User Verification")
        self.modal.geometry("300x150")

        tk.Label(self.modal, text="Verification Code").pack(pady=10)

        self.verification_code = tk.Entry(self.modal)
        self.verification_code.pack(pady=5)

        tk.Button(
            self.modal,
            text="Verify",
            command=self.verify_code,
            bg='#7AC6D2'
        ).pack(pady=10)

        self.modal.grab_set()
        self.modal.transient(self.root)
        self.modal.focus_set()

    def verify_code(self):
        result = verify_code(
            self.username.get(),
            self.verification_code.get()
        )

        if result:
            messagebox.showinfo("Success", "Verification successful!")

            if self.modal:
                self.modal.destroy()

            self.root.destroy()
            MainWindow(self.logged_user).run()
        else:
            messagebox.showerror("Error", "Invalid verification code")

    def login(self):
        result = login_user(self.username.get(), self.password.get())

        if result:
            self.logged_user = result  # store user info safely
            self.open_modal()
        else:
            messagebox.showerror("Error", "Invalid login")

    def run(self):
        self.root.mainloop()
