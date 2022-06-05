import os
import threading
import win32serviceutil
import tkinter as tk
import tkinter.ttk
from tkinter import messagebox
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

    def brake_service(service_name):
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

    '''about log'''
    def write_log(device):
        log = open('log.txt', 'a')
        time = datetime.datetime.now()
        log.writelines("[" + str(time) + "] " + str(device) +
                       " detected being used." + "\n")
        log.close()

    def read_log(l):
        log = open("log.txt", "r+")
        line = log.read().splitlines()
        list1 = line[int(l)-1:int(l)]
        result = ''.join(list1)
        log.close()
        return(result)

    '''tk window'''
    def window_thread():
        '''read log'''
        logger_is_on = read_log(2)
        toaster_is_on = read_log(3)
        always_brake = read_log(4)
        '''rewrite log'''
        def rewrite_log_loger(value):
            def changeline(line, content):
                log = open('log.txt', 'r+')
                flist = log.readlines()
                flist[int(line)] = str(content) + "\n"
                log = open('log.txt', 'w+')
                log.writelines(flist)
                log.close()
            if value == "1":
                changeline(1, "True")
                # print("Logwriter:True")
            else:
                changeline(1, "False")
                # print("Logwriter:False")

        def rewrite_log_toaster(value):
            def changeline(line, content):
                log = open('log.txt', 'r+')
                flist = log.readlines()
                flist[int(line)] = str(content) + "\n"
                log = open('log.txt', 'w+')
                log.writelines(flist)
                log.close()
            if value == "1":
                changeline(2, "True")
                # print("Toaster:True")
            else:
                changeline(2, "False")
                # print("Toaster:False")

        def rewrite_log_brake(value):
            def changeline(line, content):
                log = open('log.txt', 'r+')
                flist = log.readlines()
                flist[int(line)] = str(content) + "\n"
                log = open('log.txt', 'w+')
                log.writelines(flist)
                log.close()
            if value == "1":
                brake_service("FrameServer")
                changeline(3, "True")
                # print("Always_brake_cam:True")
            else:
                changeline(3, "False")
                # print("Always_brake_cam:False")
        '''window'''
        window = tk.Tk()
        notebook = tk.ttk.Notebook(window)
        window.title("Emergency-Brakes")
        window.iconbitmap('image/brake.ico')
        window.geometry('300x160')
        window.resizable(False, False)

        def close():
            if messagebox.askokcancel("Quit", "Quit Emergency-Brakes?"):
                window.destroy()
                os._exit(0)
        window.protocol('WM_DELETE_WINDOW', close)
        main_frame = tk.Frame()
        setting_frame = tk.Frame()
        notebook.add(main_frame, text='main')
        notebook.add(setting_frame, text='setting')
        notebook.pack(padx=0, pady=0, fill=tkinter.BOTH, expand=True)

        # setting_page
        loger_switch_label = tk.Label(
            setting_frame, text="Logger (left:Off; Right:On)")
        loger_switch_label.pack(anchor='nw')
        loger_switch = tk.Scale(setting_frame, from_=0, to=1,
                                orient='horizontal', length=50, width=20,
                                showvalue=0,
                                command=rewrite_log_loger)
        loger_switch.pack(anchor='nw')

        toaster_switch_label = tk.Label(
            setting_frame, text="Toaster (left:Off; Right:On)")
        toaster_switch_label.pack(anchor='nw')
        toaster_switch = tk.Scale(setting_frame, from_=0, to=1,
                                  orient='horizontal', length=50, width=20,
                                  showvalue=0,
                                  command=rewrite_log_toaster)
        toaster_switch.pack(anchor='nw')
        # initial switch status
        if logger_is_on == "True":
            loger_switch.set(1)
        else:
            loger_switch.set(0)
        if toaster_is_on == "True":
            toaster_switch.set(1)
        else:
            toaster_switch.set(0)
        
        # main_page
        def brake_camera():
            brake_service("FrameServer")
        cam_state_show = tk.StringVar()
        cam_state_show.set("Camera: Off")
        cam_brake_button = tk.Button(
            main_frame, text=" brake camera! ", command=brake_camera)
        cam_brake_button.pack(anchor='se')
        cam_brake_switch_lable = tk.Label(
            main_frame, text="Always brake camera (left:Off; Right:On)")
        cam_brake_switch_lable.pack(anchor='nw')
        cam_brake_switch = tk.Scale(main_frame, from_=0, to=1, 
                                    orient='horizontal', length=50, width=20,   
                                    showvalue=0, 
                                    command=rewrite_log_brake)
        cam_brake_switch.pack(anchor='nw')
        # initial switch status
        if always_brake == "True":
            cam_brake_switch.set(1)
        else:
            cam_brake_switch.set(0)

        while True:
            # main_page
            if status_service("FrameServer") == True:
                cam_state_show.set("Camera: On")
            else:
                cam_state_show.set("Camera: Off")
            tk.Label(main_frame, textvariable=cam_state_show).place(anchor='nw')
            window.update()
        # Todo: minimize to tray

    '''detect'''
    def detect_thread():
        while True:
            '''read log'''
            logger_is_on = read_log(2)
            toaster_is_on = read_log(3)
            always_brake = read_log(4)
            '''FrameServer => Camera'''
            if always_brake != "True":
                if status_service("FrameServer") == True:
                    if toaster_is_on == "True":
                        toaster.show_toast("E-B:Camera detected being used!",
                                           "If you aren't using it, open    Emergency-Brakes and click 'Brake'.",
                                           icon_path="image/warning.ico",
                                           threaded=False)
                    if logger_is_on == "True":
                        write_log("Camera")
                    #print("!!!cam on!!!")
                    while True:
                        if status_service("FrameServer") == False:
                            #print("...cam off...")
                            break
            elif always_brake == "True":
                if status_service("FrameServer") == True:
                    brake_service("FrameServer")


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
