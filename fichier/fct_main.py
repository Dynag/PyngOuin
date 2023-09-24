import os
import threading
import fichier.design as design
import psutil

import fichier.var as var

def plug():
    for filename in os.listdir("plugin"):
        full_filename = os.path.join("plugin", filename)
        if os.path.isdir(full_filename):
            var.plugIn.append(filename)

def plugin(name):
    result = 0
    try:
        file=open("plugin/"+name+"/main.py")
        result = True
        file.close()
    except:
        pass
    return result

def maj():
    import fichier.thread_maj as maj1
    threading.Thread(target=maj1.main(), args=()).start()

def Intercepte():
    try:
        val = design.question_box("Attention", "Etes vous sur de vouloir quitter ?")
        if val == True:
            for process in (process for process in psutil.process_iter() if process.name() == "OpenHardwareMonitor.exe"):
                process.kill()
            os._exit(0)


    except Exception as e:
        design.logs("exit - " + str(e))