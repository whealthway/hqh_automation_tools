import queue
import threading

task_queue = queue.Queue()


def worker():
    while True:
        func, args = task_queue.get()
        try:
            func(*args)
        except Exception as e:
            print("Task error:", e)
        task_queue.task_done()


def start_worker():
    t = threading.Thread(target=worker, daemon=True)
    t.start()


def add_task(func, *args):
    task_queue.put((func, args))
