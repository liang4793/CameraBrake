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

    '''tk window'''
    def window_thread():
        def rewrite_log_loger(value):
            def changeline(line,content):
                log = open('log.txt','r+')
                flist = log.readlines()
                flist[int(line)] = str(content) + "\n"
                log = open('log.txt','w+')
                log.writelines(flist)
                log.close()
            if value == "1":
                changeline(1, "True")
                #print("Logwriter:True")
            else:
                changeline(1, "False")
                #print("Logwriter:False")
        def rewrite_log_toaster(value):
            def changeline(line,content):
                log = open('log.txt','r+')
                flist = log.readlines()
                flist[int(line)] = str(content) + "\n"
                log = open('log.txt','w+')
                log.writelines(flist)
                log.close()
            if value == "1":
                changeline(2, "True")
                #print("Toaster:True")
            else:
                changeline(2, "False")
                #print("Toaster:False")
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
        #setting_page
        loger_switch_label = tk.Label(setting_frame, text="Logger (left:Off; Right:On)")
        loger_switch_label.pack(anchor='nw')
        loger_switch = tk.Scale(setting_frame, from_=0, to=1,
                               orient='horizontal', length=50, width=20,
                               showvalue=0,
                               command=rewrite_log_loger)
        loger_switch.pack(anchor='nw')

        toaster_switch_label = tk.Label(setting_frame, text="Toaster (left:Off; Right:On)")
        toaster_switch_label.pack(anchor='nw')
        toaster_switch = tk.Scale(setting_frame, from_=0, to=1,
                               orient='horizontal', length=50, width=20,
                               showvalue=0,
                               command=rewrite_log_toaster)
        toaster_switch.pack(anchor='nw')
        #main_page
        cam_state_show = tk.StringVar()
        cam_state_show.set("Camera: Off")
        while True:
            if status_service("FrameServer") == True:
                cam_state_show.set("Camera: On")
            else:
                cam_state_show.set("Camera: Off")
            #tk.Label(main_frame, textvariable=cam_state_show).pack(anchor='nw')
            window.update()    
        # Todo: finish the window, minimize to tray

    '''detect'''
    def detect_thread():
        while True:
            '''read log'''
            log = open("log.txt", "r+")
            line = log.read().splitlines()
            list1 = line[1:2]
            list2 = line[2:3]
            logger_is_on = ''.join(list1)
            toaster_is_on = ''.join(list2)
            log.close()
            # Todo: Modification notification mechanism
            '''FrameServer => Camera'''
            if status_service("FrameServer") == True:
                if toaster_is_on == "True":
                    toaster.show_toast("E-B:Camera detected being used!",
                                       "If you aren't using it, open Emergency-Brakes and click 'Brake'.",
                                       icon_path="image/warning.ico",
                                       threaded=False)
                if logger_is_on == "True":
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
