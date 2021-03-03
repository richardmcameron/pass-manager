from SQL import PGL
import psycopg2
from tkinter import ttk, messagebox, Text
import tkinter as tk
from ttkthemes import *

root = ThemedTk(theme='adapta')
root.geometry('400x400')

ThemedStyle()

frame1 = ttk.Frame(root)

frame1.pack(side = 'top', expand = True, fill = 'both')
frame1.pack_propagate(0)

#Get the available themes
#print(root.get_themes())

logged_in = False
register_button = False

client = PGL()

def setup_user_window():

    def submit_callback():
        user = _user_entry.get()
        password = _password_entry.get()
        description = _app_description_entry.get()


        client.insert_user_db(user, password, description)

    def refresh_callback():
        client.get_database_entries()
        _text_box.delete('1.0', tk.END)
        index = 0
        for e in client.db_list:
            _text_box.insert(tk.END, str(e) + '\n')
            index += 1

    frame2 = ttk.Frame(root)
    frame2.pack(side='top', expand=True, fill='both')
    frame2.pack_propagate(0)

    _text_box = Text(master=frame2,height = 10, borderwidth = 3)
    _text_box.pack()

    _user_entry_label = ttk.Label(master = frame2, text = 'Username')
    _user_entry_label.pack()

    _user_entry = ttk.Entry(master = frame2, width = 50)
    _user_entry.pack()

    _password_entry_label = ttk.Label(master = frame2, text = 'Password')
    _password_entry_label.pack()

    _password_entry = ttk.Entry(master = frame2, width = 50)
    _password_entry.pack()

    _app_description_label = ttk.Label(master = frame2, text = 'Description')
    _app_description_label.pack()

    _app_description_entry = ttk.Entry(master = frame2, width = 50)
    _app_description_entry.pack()

    _submit_button = ttk.Button(master = frame2, text = "Submit", command = submit_callback)
    _submit_button.pack()

    _refresh_button = ttk.Button(master=frame2, text="Refresh", command=refresh_callback)
    _refresh_button.pack()

    _text_box.delete('1.0', tk.END)
    index = 0
    for e in client.db_list:
        _text_box.insert(tk.END, str(e) + '\n')
        index += 1

def create_entry_page():
    if logged_in:
        clear_window()

        client.get_database_entries()
        setup_user_window()



def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def clear_window():
    window = all_children(root)

    for item in window:
        item.forget()

def register_callback():
    username = username_entry.get()
    password = password_entry.get()

    if len(username) >= 3 and len(password) >= 3:
        if client.check_user_found(username):
            messagebox.showinfo("Message", f"Username {username} is already registered")
        else:
            if client.create_login(username, password):
                messagebox.showinfo("Message", f"Registered {username}")
            else:
                messagebox.showinfo("Message", f"Unable to register {username}")

def login_callback():
    global register_button, logged_in
    username = username_entry.get()
    password = password_entry.get()

    if len(username) >= 3 and len(password) >= 3:
        if client.search_login(username, password):
            client.connect_db(username)
            logged_in = True
            create_entry_page()
        else:
            messagebox.showinfo("Message", "Account Not Found")
    else:
        messagebox.showinfo("Message", "Username and password must be atleast 3 characters")

pad_label = ttk.Label(master = frame1)
pad_label.pack(pady = 40)

username_label = ttk.Label(master=frame1, text = "Username")
username_label.pack()

username_entry = ttk.Entry(master=frame1,width = 25)
username_entry.pack()

password_label = ttk.Label(master=frame1,text = "Password")
password_label.pack()

password_entry = ttk.Entry(master=frame1,width = 25, show="*")
password_entry.pack(pady = 5)

login_button = ttk.Button(master=frame1,text = "Login", command = login_callback)
login_button.pack(pady = 10)

create_button = ttk.Button(master=frame1,text="Register", command = register_callback)
create_button.pack(pady = 10)

root.mainloop()
