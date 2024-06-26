import csv
import os
import threading
from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox, filedialog
import fichier.param_mail as param_mail
import fichier.param_db_quit as db_quit
import fichier.param_gene as param_gene
import fichier.param_db as param_db
import fichier.param_mail_recap as param_mail_recap
import fichier.var as var
import fichier.thread_xls as thread_xls
import fichier.fct_ping as fct_ping
import logging.config
import logging


def logs(log):
    logging.config.fileConfig('fichier/logger.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.error(log, exc_info=True)


def question_box(title, message):
    var = messagebox.askquestion(title, message)
    resp = False
    if var == "yes":
        resp = True
    else:
        resp = False
    return resp

def affilogs():
    path = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    print(path + "/log.log")
    os.startfile(path + "/log.log")

def effalogs():
    path = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    if os.path.exists(path+ "/log.log"):
        os.remove(path+ "/log.log")

def rac_s(ev=None):
    try:
        save_csv()
    except Exception as e:
        logs("design - " + str(e))

def rac_o(ev=None):
    try:
        load_csv()
    except Exception as e:
        logs("design - " + str(e))

def rac_x(ev=None):
    try:
        xlsExport()
    except Exception as e:
        logs("design - " + str(e))


def rac_w(ev=None):
    try:
        xlsImport()
    except Exception as e:
        logs("design - " + str(e))


def rac_f(ev=None):
    try:
        pluginSnyf()
    except Exception as e:
        logs("design - " + str(e))


def fenAPropos():
    try:
        import fichier.fen_a_propos as apropos
        apropos.main()
    except Exception as e:
        logs("design - " + str(e))


def fenAChangelog():
    try:
        import fichier.fen_changelog as apropos
        apropos.main()
    except Exception as e:
        logs("design - " + str(e))


def xlsImport():
    # try:
    thread_xls.openExcel()


# except Exception as e:
#	logs("design - " + str(e))

def xlsExport():
    # try:
    thread_xls.saveExcel()


# except Exception as e:
#	logs("design - " + str(e))



def test():
    try:
        import fichier.MySql as test
        t = threading.Thread(target=test.create_table(test)).start()
    except Exception as e:
        logs("design - " + str(e))


def alert(message):
    showinfo("alerte", message)


def lire_nom(ip):
    try:
        nom1 = var.tab_ip.item(ip, 'values')
        nom = nom1[1]
        return nom
    except Exception as e:
        # logs("design - " + str(e))
        pass


def save_csv():
    try:

        Tk().withdraw()
        doss = os.getcwd()+"\\bd\\"
        filename = filedialog.asksaveasfilename(initialdir=doss, title="Select file", filetypes=(
            ("Pin", "*.pin"), ("all files", "*.*")))
        filename = filename.split(".")
        filename = filename[0]
        with open(filename+".pin", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')

            for row_id in var.tab_ip.get_children():
                row = var.tab_ip.item(row_id)['values']
                csvwriter.writerow(row)

        threading.Thread(target=alert, args=("Votre plage IP à été enregistré",)).start()
    except Exception as e:
        logs("design - " + str(e))
        return


def load_csv():
    try:
        doss = os.getcwd() + "\\bd\\"
        filename = filedialog.askopenfilename(initialdir=doss, title="Select File", filetypes=(
            ("Pin", "*.pin"), ("all files", "*.*")))
        with open(filename) as myfile:
            csvread = csv.reader(myfile, delimiter=',')
            i = 0
            for row in csvread:
                var.tab_ip.insert(parent='', index=i, tag=row[0], iid=row[0], values=row)
                var.tab_ip.tag_configure(tagname=row[0])
                i = i + 1
    except Exception as e:
        logs("design - " + str(e))
        return


def paramGene():
    threading.Thread(target=param_gene.main).start()


def paramDb():
    threading.Thread(target=param_db.main).start()


def paramMail():
    threading.Thread(target=param_mail.main).start()


def paramMailRecap():
    threading.Thread(target=param_mail_recap.main).start()

def quit_db():
    db_quit.save_param_db()

def pluginGest():
    try:
        import os
        import subprocess
        path = os.path.abspath(os.getcwd())+"\\plugin"
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        path = os.path.normpath(path)
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
    except Exception as e:
        print(e)
        logs("design - " + str(e))

def plugIn(x):
    print(x)
    try:
        import os
        import sys
        import importlib

        module = None
        full_path_to_module = 'plugin/'+x+'/main.py'
        print(full_path_to_module)
        try:
            module_dir, module_file = os.path.split(full_path_to_module)
            module_name, module_ext = os.path.splitext(module_file)
            spec = importlib.util.spec_from_file_location(module_name, full_path_to_module)
            print(spec)
            module = spec.loader.load_module()
        except Exception as e:
            logs("design - " + str(e))
            print(e)
        module.main()

    except Exception as e:
        print(e)
        logs("design - " + str(e))


"""    try:
        import os
        import sys
        pyfilepath = 'plugin/'+x+'/main.py'


        import importlib

        dirname, basename = os.path.split(pyfilepath)  # pyfilepath: '/my/path/mymodule.py'
        sys.path.append(dirname)  # only directories should be added to PYTHONPATH
        module_name = os.path.splitext(basename)[0]  # '/my/path/mymodule.py' --> 'mymodule'
        module = importlib.import_module(
            module_name)  # name space of defined module (otherwise we would literally look for "module_name")
        print(module)
        module.main()

        p = 'plugin/'+x+'/main/main.py'
        module = __import__(p)
        module.main()

    except Exception as e:
        print(e)
        logs("design - " + str(e))"""

def pluginSnyf():
    try:
        import plugin.Snyf.main as apropos
        apropos.main()
    except Exception as e:
        print(e)
        logs("design - " + str(e))
#  Menu
def create_menu(fenetre, frame_haut):
    menubar = Menu(fenetre)



    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Sauvegarder  ctrl+s", command=save_csv)
    menu1.add_command(label="Ouvrir  ctrl+o", command=load_csv)
    menu1.add_command(label="Charger", command=load_csv)
    menu1.add_command(label="Tout effacer", command=tab_erase)
    menu1.add_separator()
    menu1.add_command(label="Test", command=test)
    menu1.add_command(label="Sauvegarder les réglages", command=quit_db)
    menubar.add_cascade(label="Fichier", menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label="Général", command=paramGene)
    menu2.add_command(label="Envoies", command=paramMail)
    menu2.add_command(label="Mail Recap", command=paramMailRecap)
    menu2.add_command(label="DB", command=paramDb)
    menubar.add_cascade(label="Paramètres", menu=menu2)

    menu4 = Menu(menubar, tearoff=0)
    menu4.add_command(label="Export xls ctrl+x", command=xlsExport)
    menu4.add_command(label="Import xls ctrl+w", command=xlsImport)
    menu4.add_separator()
    menubar.add_cascade(label="Fonctions", menu=menu4)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label="A propos", command=fenAPropos)
    menu3.add_command(label="Changelog", command=fenAChangelog)
    menu3.add_command(label="Logs", command=affilogs)
    menu3.add_command(label="Effacer Logs", command=effalogs)
    menu3.add_separator()

    menu5 = Menu(menubar, tearoff=0)
    menu5.add_command(label="Gestion", command=pluginGest)
    menu5.add_separator()
    for plug in var.plugIn:
        menu5.add_command(label=plug, command=lambda plug1=plug: plugIn(plug1))


    menubar.add_cascade(label="Plugins", menu=menu5)

    menubar.add_cascade(label="?", menu=menu3)
    menubar.bind_all('<Control-s>', rac_s)
    menubar.bind_all('<Control-l>', lambda ev: fct_ping.lancerping(frame_haut))
    menubar.bind_all('<Control-x>', rac_x)
    menubar.bind_all('<Control-w>', rac_w)
    menubar.bind_all('<Control-o>', rac_o)
    menubar.bind_all('<Control-f>', rac_f)
    return menubar


def tab_erase():
    try:
        val = question_box("Attention", "Etes vous sur de vouloir effacer la liste ?")
        if val == True:
            for i in var.tab_ip.get_children():
                var.tab_ip.delete(i)
    except Exception as e:
        logs("design - " + str(e))


def center_window(w):
    try:
        eval_ = w.nametowidget('.').eval
        eval_('tk::PlaceWindow %s center' % w)
    except Exception as e:
        logs("design - " + str(e))
