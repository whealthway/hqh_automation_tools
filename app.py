from core.task_queue import start_worker
from ui.login_window import LoginWindow

if __name__ == "__main__":
    # Start background worker (VERY IMPORTANT)
    start_worker()

    # Start app
    app = LoginWindow()
    app.run()
