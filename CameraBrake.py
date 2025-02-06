import os
import sys
import ctypes
import threading
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox

import win32serviceutil
from win10toast_click import ToastNotifier
import pystray
from pystray import MenuItem as item, Menu
from PIL import Image

# 常量定义
SERVICE_NAME = "FrameServer"
LOG_FILE = "camera_brake.log"
CONFIG_FILE = "config.ini"
ICON_PATH = "image/brake.ico"
WARNING_ICON = "image/warning.ico"


def require_admin():
    """检查是否有管理员权限，如果没有则尝试以管理员身份重启当前脚本"""

    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
    except Exception:
        pass

    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()


class ServiceManager:
    """服务管理模块，提供查询和停止服务功能"""

    @staticmethod
    def get_status(service_name):
        try:
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            return status == 4  # 4表示服务正在运行
        except Exception as e:
            raise RuntimeError(f"Service status query failed: {str(e)}") from e

    @staticmethod
    def stop_service(service_name):
        try:
            win32serviceutil.StopService(service_name)
            return True
        except Exception as e:
            raise RuntimeError(f"Service stop failed: {str(e)}") from e


class LogManager:
    """日志和配置管理模块"""

    @staticmethod
    def write_log(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    @staticmethod
    def read_config():
        config = {
            "logger_enabled": True,
            "toaster_enabled": True,
            "always_brake": False
        }
        try:
            with open(CONFIG_FILE, "r") as f:
                lines = f.read().splitlines()
                if len(lines) >= 1:
                    config["logger_enabled"] = lines[0] == "True"
                if len(lines) >= 2:
                    config["toaster_enabled"] = lines[1] == "True"
                if len(lines) >= 3:
                    config["always_brake"] = lines[2] == "True"
        except FileNotFoundError:
            with open(CONFIG_FILE, "w") as f:
                f.write("\n".join(["True", "True", "False"]))
        return config

    @staticmethod
    def update_config(key, value):
        config = LogManager.read_config()
        config[key] = value
        with open(CONFIG_FILE, "w") as f:
            f.write("\n".join([
                str(config["logger_enabled"]),
                str(config["toaster_enabled"]),
                str(config["always_brake"])
            ]))


class ToggleSwitch(ttk.Frame):
    """自定义开关组件"""

    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.state = tk.BooleanVar(value=False)
        self._create_widgets()

    def _create_widgets(self):
        self.canvas = tk.Canvas(self, width=50, height=26, bg='white', bd=0, highlightthickness=0)
        self.bg = self.canvas.create_rectangle(2, 2, 48, 24, fill='#cccccc', outline='')
        self.knob = self.canvas.create_rectangle(2, 2, 24, 24, fill='white', outline='#aaaaaa')
        self.canvas.tag_bind(self.knob, '<Button-1>', self.toggle)
        self.canvas.tag_bind(self.bg, '<Button-1>', self.toggle)
        self.canvas.pack()

    def toggle(self, event=None):
        new_state = not self.state.get()
        self.state.set(new_state)
        self._update_appearance()
        if self.command:
            self.command(new_state)

    def _update_appearance(self):
        if self.state.get():
            self.canvas.itemconfig(self.bg, fill='#fa6400')
            self.canvas.coords(self.knob, 26, 2, 48, 24)
        else:
            self.canvas.itemconfig(self.bg, fill='#cccccc')
            self.canvas.coords(self.knob, 2, 2, 24, 24)
        self.canvas.update()

    def set(self, value):
        self.state.set(value)
        self._update_appearance()


class TrayIcon:
    """托盘图标管理类，提供打开窗口和退出功能"""

    def __init__(self, gui):
        self.gui = gui
        self.icon = pystray.Icon("CameraBrake")
        try:
            self.icon.icon = Image.open(ICON_PATH)
        except Exception:
            self.icon.icon = Image.new('RGB', (64, 64), color=(255, 255, 255))
        self.icon.menu = Menu(
            item("Open", self.on_open),
            item("Exit", self.on_exit)
        )

    def on_open(self, icon, item):
        self.gui.root.deiconify()  # 恢复窗口
        self.icon.stop()
        self.gui.tray_icon = None  # 清除托盘图标对象

    def on_exit(self, icon, item):
        self.icon.stop()
        self.gui.root.quit()
        os._exit(0)


class CameraBrakeGUI:
    """GUI模块，构建主窗口和设置页面"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CameraBrake")
        try:
            self.root.iconbitmap(ICON_PATH)
        except Exception:
            pass
        self.root.geometry('300x160')
        self.root.resizable(False, False)
        self.tray_icon = None

        self._create_widgets()
        self._setup_protocols()
        self._load_initial_settings()

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self.root)

        self.main_frame = ttk.Frame(self.notebook)
        self._create_main_tab()

        self.settings_frame = ttk.Frame(self.notebook)
        self._create_settings_tab()

        self.notebook.add(self.main_frame, text='Main')
        self.notebook.add(self.settings_frame, text='Settings')
        self.notebook.pack(expand=True, fill='both')

    def _create_main_tab(self):
        self.cam_status = tk.StringVar(value="Camera: Checking...")
        ttk.Label(self.main_frame, textvariable=self.cam_status).pack(anchor='nw')

        ttk.Button(self.main_frame, text="Brake Camera!", command=self._brake_camera).pack(anchor='nw')

        ttk.Label(self.main_frame, text="Always Brake Camera").pack(anchor='nw')
        self.always_brake_switch = ToggleSwitch(
            self.main_frame,
            command=lambda s: self._update_setting("always_brake", s)
        )
        self.always_brake_switch.pack(anchor='nw')

    def _create_settings_tab(self):
        ttk.Label(self.settings_frame, text="Enable Logger").pack(anchor='nw')
        self.logger_switch = ToggleSwitch(
            self.settings_frame,
            command=lambda s: self._update_setting("logger_enabled", s)
        )
        self.logger_switch.pack(anchor='nw')

        ttk.Label(self.settings_frame, text="Enable Notifications").pack(anchor='nw')
        self.toaster_switch = ToggleSwitch(
            self.settings_frame,
            command=lambda s: self._update_setting("toaster_enabled", s)
        )
        self.toaster_switch.pack(anchor='nw')

    def _setup_protocols(self):
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

    def _load_initial_settings(self):
        config = LogManager.read_config()
        self.logger_switch.set(config["logger_enabled"])
        self.toaster_switch.set(config["toaster_enabled"])
        self.always_brake_switch.set(config["always_brake"])

    def _update_setting(self, key, value):
        LogManager.update_config(key, value)
        if key == "always_brake" and value:
            self._brake_camera()

    def _brake_camera(self):
        try:
            ServiceManager.stop_service(SERVICE_NAME)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop service: {str(e)}")

    def _on_close(self):
        # 弹出对话框，选择最小化到托盘或退出
        answer = messagebox.askyesno("Minimize to Tray",
                                     "Minimize to Tray? (Yes to minimize, No to exit)")
        if answer:
            self.root.withdraw()
            self._create_tray_icon()
        else:
            self.root.destroy()
            os._exit(0)

    def _create_tray_icon(self):
        if self.tray_icon is None:
            self.tray_icon = TrayIcon(self)
            t = threading.Thread(target=self.tray_icon.icon.run)
            t.daemon = True
            t.start()

    def run(self):
        self._update_status()
        self.root.mainloop()

    def _update_status(self):
        try:
            status = ServiceManager.get_status(SERVICE_NAME)
            self.cam_status.set(f"Camera: {'On' if status else 'Off'}")
        except RuntimeError:
            self.cam_status.set("Status: Unknown")
        self.root.after(500, self._update_status)


class BackgroundMonitor:
    """后台监控模块，监控服务状态并处理激活/关闭事件"""

    def __init__(self):
        self.running = threading.Event()
        self.running.set()
        self.toaster = ToastNotifier()
        self.last_state = None

    def start(self):
        thread = threading.Thread(target=self._monitor)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.running.clear()

    def _monitor(self):
        while self.running.is_set():
            try:
                config = LogManager.read_config()
                current_state = ServiceManager.get_status(SERVICE_NAME)
                if current_state != self.last_state:
                    if current_state:
                        self._handle_activation(config)
                    else:
                        self._handle_deactivation(config)
                    self.last_state = current_state
                if config["always_brake"] and current_state:
                    ServiceManager.stop_service(SERVICE_NAME)
            except Exception as e:
                LogManager.write_log(f"Monitoring error: {str(e)}")
            finally:
                time.sleep(0.5)

    def _handle_activation(self, config):
        if config["logger_enabled"]:
            LogManager.write_log("Camera activated")
        if config["toaster_enabled"]:
            self._show_notification()
        # 循环等待直到服务关闭或配置变更
        while ServiceManager.get_status(SERVICE_NAME) and not config["always_brake"]:
            time.sleep(0.5)

    def _handle_deactivation(self, config):
        if config["logger_enabled"]:
            LogManager.write_log("Camera deactivated")

    def _show_notification(self):
        try:
            self.toaster.show_toast(
                "Camera Activity Detected!",
                "Camera is in use. Open CameraBrake to control.",
                icon_path=WARNING_ICON,
                duration=5,
                threaded=True
            )
        except Exception as e:
            LogManager.write_log(f"Notification failed: {str(e)}")


def main():
    require_admin()
    gui = CameraBrakeGUI()
    monitor = BackgroundMonitor()
    monitor.start()
    gui.run()
    monitor.stop()


if __name__ == "__main__":
    main()
