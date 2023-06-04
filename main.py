#!/usr/bin/python
# encoding: utf-8
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

import pyautogui
import tkinter as tk
from tkinter import messagebox

MAX_TIMES = 10000


class RunningStatus(Enum):
    STOPPED = "Not Running"
    RUNNING = "Running"


class ButtonStatus(Enum):
    START = "Start"
    STOP = "Stop"


class KeyPressAuto:
    def __init__(self):
        self.root = tk.Tk()
        self.messagebox = tk.messagebox
        self.input_label = tk.Label(self.root, text="Press:")
        self.input_var = tk.StringVar()
        self.input_var.set("0")

        self.interval_var = tk.StringVar()
        self.interval_var.set("3")
        self.input_entry = tk.Entry(self.root, textvariable=self.input_var)
        self.interval_label = tk.Label(self.root, text="Interval")
        self.interval_entry = tk.Entry(self.root, textvariable=self.interval_var)
        self.tips_label = tk.Label(self.root)
        self.btn_start_stop = tk.Button(self.root)
        self.running_status = RunningStatus.STOPPED.value
        self.btn_text_var = tk.StringVar()
        self.btn_text_var.set(ButtonStatus.START.value)

        self.running_status_var = tk.StringVar()
        self.running_status_var.set(RunningStatus.STOPPED.value)

        self.kp = None

    class KeyPress(threading.Thread):
        def __init__(self):
            super().__init__()
            self.running_status = RunningStatus.STOPPED.value
            self.interval = 3
            self.cnt = MAX_TIMES
            self.key = ""
            self.callback = None

        def calc_counter(self):
            self.cnt -= 1
            print(f"counter={self.cnt}")

        def set_counter(self, cnt):
            self.cnt = cnt

        def reset_counter(self):
            self.set_counter(MAX_TIMES)

        def set_key(self, key):
            self.key = key

        def set_running_status(self, status):
            self.running_status = status

        def set_call_back(self, callback):
            self.callback = callback

        def run(self) -> None:
            try:
                while self.running_status == RunningStatus.RUNNING.value and self.cnt > 0:
                    time.sleep(self.interval)
                    pyautogui.press(self.key)
                    print(f"pressed {self.key}")
                    self.calc_counter()
            except Exception as err:
                print(err)
            finally:
                self.reset_counter()
                print(f"press key stop")
                if self.callback:
                    self.callback()

        def set_interval(self, interval):
            try:
                interval = int(interval)
            except Exception as err:
                print(f"{err}, invalid interval: {interval}")
                interval = 3
            self.interval = interval

    def is_running(self):
        return self.running_status == RunningStatus.RUNNING.value

    def print_running_status(self):
        print(f"running status = {self.running_status}")

    def press_key(self, key='0', interval='3'):
        if key:
            self.kp = self.KeyPress()
            self.kp.set_key(key)
            self.kp.set_interval(interval)
            self.kp.set_running_status(self.running_status)
            self.kp.set_call_back(self.set_status_stop)
            self.kp.start()
        print("press key end")

    def click_btn_start_stop(self):
        self.switch_state()
        self.start()

    def switch_state(self):
        if self.running_status == RunningStatus.STOPPED.value:
            self.set_status_start()
        else:
            self.set_status_stop()

    def set_status_stop(self):
        self.running_status = RunningStatus.STOPPED.value
        self.running_status_var.set(RunningStatus.STOPPED.value)
        self.btn_text_var.set(ButtonStatus.START.value)
        if self.kp:
            self.kp.set_running_status(RunningStatus.STOPPED.value)

    def set_status_start(self):
        self.running_status = RunningStatus.RUNNING.value
        self.running_status_var.set(RunningStatus.RUNNING.value)
        self.btn_text_var.set(ButtonStatus.STOP.value)

    def validate_input(self):
        return bool(self.input_var.get())

    def validate_interval(self):
        interval = self.interval_var.get()
        return interval.isdigit()

    def msg_err_input(self):
        self.messagebox.showerror(title="Error", message="Key to press cannot be empty!")
        self.set_status_stop()

    def msg_err_interval(self):
        self.messagebox.showerror(title="Error", message="Interval is invalid!")
        self.set_status_stop()

    def start(self):
        entry = self.input_entry.get()
        interval = self.interval_entry.get()
        if not entry:
            self.msg_err_input()
            return
        if not interval.isdigit():
            self.msg_err_interval()
            return
        if self.is_running() and entry:
            self.press_key(entry, interval)
        self.print_running_status()

    def main(self):
        self.root.title("Key Press Auto")
        self.root.wm_iconbitmap("frog_icon.ico")
        self.root.geometry("300x100")
        self.input_label.grid(row=0, column=0)
        self.input_entry.grid(row=0, column=1)
        self.interval_label.grid(row=0, column=2)
        self.interval_entry.grid(row=0, column=3)

        self.btn_start_stop = tk.Button(self.root, textvariable=self.btn_text_var, command=self.click_btn_start_stop)
        self.btn_start_stop.grid(row=1, column=1)
        self.tips_label = tk.Label(self.root, textvariable=self.running_status_var)
        self.tips_label.grid(row=1, column=2)
        self.root.mainloop()


if __name__ == '__main__':
    k = KeyPressAuto()
    k.main()
