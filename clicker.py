import threading
import time
import tkinter as tk
from tkinter import ttk

import pyautogui
from pynput import keyboard


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.interval = 0.05
        self.stop_event = threading.Event()
        self.hotkey_listener = None
        self.status_var = tk.StringVar(value="已停止")
        self.click_count_var = tk.StringVar(value="0")
        self.click_total = 0

        self.root.title("Auto Clicker")
        self.root.geometry("320x180")
        self.root.resizable(False, False)
        self.root.configure(bg="#f3f4f6")

        title = tk.Label(
            root,
            text="自动连点器",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#f3f4f6",
            fg="#1f2937",
        )
        title.pack(pady=(18, 8))

        panel = ttk.Frame(root, padding=(16, 8))
        panel.pack(fill="x", padx=16)

        ttk.Label(panel, text="状态:").grid(row=0, column=0, sticky="w")
        ttk.Label(panel, textvariable=self.status_var, foreground="#0f766e").grid(row=0, column=1, sticky="w", padx=(8, 0))

        ttk.Label(panel, text="点击次数:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Label(panel, textvariable=self.click_count_var, foreground="#7c3aed").grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))

        ttk.Label(panel, text="间隔: ").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.interval_var = tk.StringVar(value="0.05")
        ttk.Entry(panel, textvariable=self.interval_var, width=10).grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(8, 0))

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=(12, 8))
        self.toggle_btn = ttk.Button(button_frame, text="开始 / 停止", command=self.toggle)
        self.toggle_btn.grid(row=0, column=0, padx=(0, 8))

        ttk.Button(button_frame, text="退出", command=self.shutdown).grid(row=0, column=1)

        ttk.Label(
            root,
            text="快捷键: F6 开关 | F7 退出",
            foreground="#475569",
            font=("Microsoft YaHei", 9),
        ).pack(pady=(0, 12))

        self.worker_thread = threading.Thread(target=self.worker_loop, daemon=True)
        self.worker_thread.start()
        self.start_hotkeys()

    def set_running(self, is_running):
        self.running = is_running
        self.status_var.set("运行中" if self.running else "已停止")
        self.toggle_btn.configure(text="停止" if self.running else "开始")

    def toggle(self):
        try:
            value = float(self.interval_var.get())
            if value <= 0:
                raise ValueError
            self.interval = value
        except ValueError:
            self.interval_var.set("0.05")
            self.interval = 0.05
        self.set_running(not self.running)

    def worker_loop(self):
        while not self.stop_event.is_set():
            if self.running:
                pyautogui.click()
                self.click_total += 1
                self.click_count_var.set(str(self.click_total))
            time.sleep(self.interval)

    def shutdown(self):
        self.stop_event.set()
        if self.hotkey_listener is not None:
            self.hotkey_listener.stop()
        self.root.destroy()

    def start_hotkeys(self):
        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<f6>': self.on_hotkey_toggle,
            '<f7>': self.on_hotkey_exit,
        })
        self.hotkey_listener.start()

    def on_hotkey_toggle(self):
        self.toggle()

    def on_hotkey_exit(self):
        self.shutdown()


def main():
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
