import threading
import win32serviceutil
import tkinter as tk
import tkinter.ttk
from win10toast_click import ToastNotifier
import datetime
toaster = ToastNotifier()

def main():
    '''Define module'''
    #  0: "UNKNOWN"
    #  1: "STOPPED"
    #  2: "START_PENDING"
    #  3: "STOP_PENDING"
    #  4: "RUNNING"
    def is_iterable(source):
        if source is not None:
            try:
                iter(source)
            except TypeError:
                return False
            return True
        else:
            raise RuntimeError("argument cannot be None")

    def status_service(service_name):
        try:
            result = win32serviceutil.QueryServiceStatus(service_name)[1]
            if result == 4:  # running!
                return True
            elif result == 1:  # braked!
                return False
            else:
                return result
        except Exception as e:
            if e.args:
                args = list()
                for arg in e.args:
                    if is_iterable(arg):
                        args.append(str(eval(repr(arg)), 'gbk'))
                    else:
                        args.append(arg)
                raise RuntimeError("Error:", args[-1], tuple(args))
            else:
                raise RuntimeError(
                    "Uncaught exception, maybe it is a 'Access Denied'")

    def stop_service(service_name):
        status = status_service(service_name)
        if status == True:
            try:
                win32serviceutil.StopService(service_name)
            except Exception as e:
                if e.args:
                    args = list()
                    for arg in e.args:
                        if is_iterable(arg):
                            args.append(str(eval(repr(arg)), 'gbk'))
                        else:
                            args.append(arg)
                    print("Error:", args[-1], tuple(args))
                    raise RuntimeError
                else:
                    raise RuntimeError(
                        "Uncaught exception, maybe it is a 'Access Denied'")

    '''write log'''
    def writelog(device):
        log = open('log.txt', 'a')
        time = datetime.datetime.now()
        log.writelines("[" + str(time) + "] " + str(device) +
                       " detected being used." + "\n")
        log.close()

    def window_thread():
        window = tk.Tk()
        notebook = tk.ttk.Notebook(window)
        window.title("Emergency-Brakes")
        window.geometry('300x200')
        window.resizable(False, False)
        main_frame = tk.Frame()
        setting_frame = tk.Frame()
        notebook.add(main_frame, text='main')
        notebook.add(setting_frame, text='setting')
        notebook.pack(padx=0, pady=0, fill=tkinter.BOTH, expand=True)
        # Todo: finish the window, minimize to tray
        window.mainloop()

    def detect_thread():
        while True:
            '''read log'''
            log = open("log.txt", "r+")
            line = log.read().splitlines()
            list1 = line[1:2]
            logger = ''.join(list1)
            log.close()
            # Todo: Modification notification mechanism
            '''FrameServer => Camera'''
            if status_service("FrameServer") == True:
                toaster.show_toast("E-B:Camera detected being used!",
                                   "If you aren't using it, open Emergency-Brakes and click 'Brake'.",
                                   icon_path="image/warning.ico",
                                   threaded=False)
                if logger == "True":
                    writelog("Camera")

    '''thread'''
    thread1 = threading.Thread(target=window_thread)
    thread2 = threading.Thread(target=detect_thread)
    try:
        thread1.start()
        thread2.start()
    except:
        print("Error: unable to start thread")

if __name__ == "__main__":
    main()
