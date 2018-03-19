"""
Welcome to very simple notepad application
"""

import os
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox as tkm

APP_NAME = 'NoteNote'
is_open = None

root = Tk()
root.title(APP_NAME)
root.geometry('400x400')

# Adding widget commands
def copy():
    main_text.event_generate('<<Copy>>')

def paste():
    main_text.event_generate('<<Paste>>')

def undo():
    main_text.event_generate('<<Undo>>')

def redo(x=None):
    main_text.event_generate('<<Redo>>')

def cut():
    main_text.event_generate('<<Cut>>')

def select(x=None):
    main_text.tag_add('sel', '1.0', 'end')


def file_new(x=None):
    root.title('Untitled')
    global is_open
    is_open = None
    main_text.delete(1.0, END)


def file_open(x=None):
    input_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_name:
        global is_open
        is_open = input_name
        root.title('{} - {}'.format(os.path.basename(is_open), APP_NAME))
        main_text.delete(1.0, END)
        with open(is_open) as _file:
            main_text.insert(1.0, _file.read())


def file_write(fname):
    try:
        file_content = main_text.get(1.0, 'end')
        with open(fname, 'w') as file_name:
            file_name.write(file_content)
    except IOError:
        pass  


def file_save_as(x=None):
    file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if file_name:
        global is_open
        is_open = file_name
        file_write(is_open)
        root.title('{} - {}'.format(os.path.basename(is_open), APP_NAME))
    return "break"
    

def file_save(x=None):
    global is_open
    if not is_open:
        file_save_as()
    else:
        file_write(is_open)
    return "break"

def find(x=None):
    search_window = Toplevel(root)
    search_window.title('What are you looking for?')
    search_window.transient(root)
    Label(search_window, text="Find:").grid(row=0, column=0, sticky='e')
    entry_search = Entry(
        search_window, width=25)
    entry_search.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    entry_search.focus_set()
    Button(search_window, text="Find", underline=0,
           command=lambda: find_results(
               entry_search.get(), main_text, search_window, entry_search)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_find():
        main_text.tag_remove('match', '1.0', END)
        search_window.destroy()
    search_window.protocol('WM_DELETE_WINDOW', close_find)
    return "break"


def find_results(needle, main_text,
                  search_toplevel, search_box):
    main_text.tag_remove('match', '1.0', END)
    found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = main_text.search(needle, start_pos,
                                         stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            main_text.tag_add('match', start_pos, end_pos)
            found += 1
            start_pos = end_pos
        main_text.tag_config(
            'match', foreground='white', background='gray')
    search_box.focus_set()

def about_window(x=None):
    tkm.showinfo("About", "NoteNote 2018"
                 "\nWojtek Balaban \nwojciechbalaban@gmail.com")


def help_window(x=None):
   tkm.showinfo(
        "Help", "Oh, come on... It's really simple.",
        icon='question')


def exit_program(x=None):
    if tkm.askokcancel("Quitting...", "Do you really want to quit?"):
        root.destroy()


# Adding application menu
my_menu = Menu(root)

# Menu icons
new_icon = PhotoImage(file="new.png")
open_icon = PhotoImage(file="open.png")
save_icon = PhotoImage(file="save.png")
undo_icon = PhotoImage(file="undo.gif")
redo_icon = PhotoImage(file="redo.gif")
smile_icon = PhotoImage(file="smile.gif")


menu_file = Menu(my_menu, tearoff=0)
menu_file.add_command(label='New', accelerator='Ctrl+N', compound='left',
                      image=new_icon, underline=0, command=file_new)
menu_file.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                      image=open_icon, underline=0, command=file_open)
menu_file.add_command(label='Save', accelerator='Ctrl+S',
                      image=save_icon, compound='left', underline=0, command=file_save)
menu_file.add_command(
    label='Save as', accelerator='Shift+Ctrl+S', command=file_save_as)
menu_file.add_separator()
menu_file.add_command(label='Exit', accelerator='Alt+F4', command=exit_program)
my_menu.add_cascade(label='File', menu=menu_file)

menu_edit = Menu(my_menu, tearoff=0)
menu_edit.add_command(label='Undo', accelerator='Ctrl+Z',
                      compound='left', image=undo_icon, command=undo)
menu_edit.add_command(label='Redo', accelerator='Ctrl+Y',
                      compound='left', image=redo_icon, command=redo)
menu_edit.add_separator()
menu_edit.add_command(label='Cut', accelerator='Ctrl+X',
                      compound='left', command=cut)
menu_edit.add_command(label='Copy', accelerator='Ctrl+C',
                      compound='left', command=copy)
menu_edit.add_command(label='Paste', accelerator='Ctrl+V',
                      compound='left', command=paste)
menu_edit.add_separator()
menu_edit.add_command(label='Find', underline=0,
                      accelerator='Ctrl+F', command=find)
menu_edit.add_command(label='Select All', underline=7,
                      accelerator='Ctrl+A', command=select)
my_menu.add_cascade(label='Edit', menu=menu_edit)

menu_about = Menu(my_menu, tearoff=0)
menu_about.add_command(label='About', compound='left',
                       image=smile_icon, command=about_window)
menu_about.add_command(label='Help', command=help_window)
my_menu.add_cascade(label='About',  menu=menu_about)

root.config(menu=my_menu)

# Adding quick buttons
quickbuttons = Frame(root, height=18, background = 'azure3')
quickbuttons.pack(expand='no', fill = 'x')

qb1 = Button(quickbuttons, image=new_icon, command = file_new).pack(side='left')
qb2 = Button(quickbuttons, image=open_icon, command = file_open).pack(side='left')
qb3 = Button(quickbuttons, image=save_icon, command = file_save).pack(side='left')
qb4 = Button(quickbuttons, image=undo_icon, command = undo).pack(side='left')
qb5 = Button(quickbuttons, image=redo_icon, command = redo).pack(side='left')


# adding text and scrollbar widgets
main_text = Text(root, wrap ='word')
main_text.pack(expand='yes', fill = 'both')

scrollbar=Scrollbar(main_text)
main_text.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=main_text.yview)
scrollbar.pack(side='right', fill='y')


# adding additional key bidings
main_text.bind('<Control-N>', file_new)
main_text.bind('<Control-n>', file_new)
main_text.bind('<Control-O>', file_open)
main_text.bind('<Control-o>', file_open)
main_text.bind('<Control-S>', file_save)
main_text.bind('<Control-s>', file_save)
main_text.bind('<Control-A>', select)
main_text.bind('<Control-a>', select)
main_text.bind('<Control-y>', redo)
main_text.bind('<Control-Y>', redo)
main_text.bind('<Control-f>', find)
main_text.bind('<Control-F>', find)
main_text.bind('<KeyPress-F1>', help_window)

root.protocol('WM_DELETE_WINDOW', exit_program)
root.mainloop()