import queue
import threading

task_queue = queue.Queue()
stop_event = threading.Event()
worker_thread = None


def worker():
    while not stop_event.is_set():
        try:
            func, args = task_queue.get(timeout=1)
            try:
                func(*args)
            except Exception as e:
                print("Task error:", e)
            finally:
                task_queue.task_done()
        except queue.Empty:
            continue


def start_worker():
    global worker_thread

    if worker_thread and worker_thread.is_alive():
        return

    stop_event.clear()

    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()


def stop_worker():
    print("Stopping worker thread...")
    stop_event.set()


def add_task(func, *args):
    task_queue.put((func, args))
