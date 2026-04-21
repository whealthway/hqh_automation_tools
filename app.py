from core.task_queue import start_worker
from ui.login_window import LoginWindow
import sys
from datetime import datetime
from tkinter import messagebox

if __name__ == "__main__":
    # App expiry
    expiration_date = datetime(2026, 4, 30, 00, 00, 00, 000)
    if datetime.now() > expiration_date:
        messagebox.showwarning("App Expired", "Contact the developer")
        sys.exit()  # ✅ STOP the app
    else:
        # Start background worker (VERY IMPORTANT)
        start_worker()

        # Start app
        app = LoginWindow()
        app.run()
