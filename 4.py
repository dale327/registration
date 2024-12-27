import tkinter as tk
from tkinter import ttk
import sqlite3 as sl
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showwarning, showinfo
import hashlib
md5_hash = hashlib.new('md5')

def switch_to_registration():
    win.withdraw()
    win2.deiconify()

def switch_to_authorization():
    win2.withdraw()
    win.deiconify()


# функция регистрации
def add_account(con, cursor, login, password):
    if ent_var4.get() != password:
        showwarning(title='Ошибка', message='Введенные пароли не совпадают!')
    else:
        md5_hash.update(password.encode())
        md5_hex = md5_hash.hexdigest()
        password = md5_hex
        sql = 'INSERT INTO accounts (login, password) values (?,?)'
        data = [(login, password)]
        con.executemany(sql, data)
        showinfo(message='Вы успешно зарегистрировались!\n'
                         'Чтобы войти, перезапустите программу.')
        con.commit()
        win.destroy()


# функция показа-скрытия пароля
def show():
    if ent2['show'] == '*':
        ent2.config(show='')
    else:
        ent2.config(show='*')

def show2():
    if ent4['show'] == '*':
        ent4.config(show='')
    else:
        ent4.config(show='*')
    if ent5['show'] == '*':
        ent5.config(show='')
    else:
        ent5.config(show='*')


# функция авторизации
def auth(con, cursor, login, password):
    md5_hash.update(password.encode())
    md5_hex = md5_hash.hexdigest()
    password = md5_hex
    cursor.execute(f'SELECT login FROM accounts WHERE login=?', (login,))
    log = cursor.fetchone()
    if log is None:
        showwarning(message='Аккаунта с таким логином не существует!')
    else:
        cursor.execute(f'SELECT password FROM accounts WHERE login=?', (login,))
        passw = cursor.fetchone()
        if passw[0] == password:
            showinfo(message='Вы успешно вошли в аккаунт!')
            win.destroy()
        else:
            showerror(message='Неверный пароль!')


# подключение к дб
con = sl.connect('db.db')
cursor = con.cursor()


# создание окна авторизации
win = tk.Tk()
win.geometry('400x500')
win.resizable(False, False)
win.title('Авторизация')
eye_image = ImageTk.PhotoImage(image=Image.open('free-icon-open-eye-829117.jpg'))
lb = ttk.Label(win, text='Авторизация', font='TN 12')
lb.place(x=150, y=0)

lb2 = ttk.Label(win, text='Логин:', font='TN 12')
lb2.place(x=30, y=130)

lb3 = ttk.Label(win, text='Пароль:', font='TN 12')
lb3.place(x=25, y=230)

lb4 = ttk.Label(win, text='Нет аккаунта?', font='TN 12', cursor='hand2')
lb4.place(x=150, y=350)
lb4.bind('<Button-1>', lambda event: switch_to_registration())


ent_var = tk.StringVar()
ent = ttk.Entry(win, textvariable=ent_var, width=20)
ent.place(x=100, y=130)

ent_var2 = tk.StringVar()
ent2 = ttk.Entry(win, textvariable=ent_var2, width=20, show='*')
ent2.place(x=100, y=230)

btn = ttk.Button(win, text='Войти', command=lambda: auth(con, cursor, ent_var.get(), ent_var2.get()))
btn.place(x=163, y=450)

btn3 = ttk.Button(win, image=eye_image, command=show)
btn3.place(x=240, y=220)

# создание окна регистрации

win2 = tk.Toplevel()
win2.geometry('400x500')
win2.resizable(False, False)
win2.title('Регистрация')
win2.protocol("WM_DELETE_WINDOW", win2.withdraw)


lb5 = ttk.Label(win2, text='Регистрация', font='TN 12')
lb5.place(x=150, y=0)

lb6 = ttk.Label(win2, text='Логин:', font='TN 12')
lb6.place(x=30, y=130)

lb7 = ttk.Label(win2, text='Пароль:', font='TN 12')
lb7.place(x=25, y=220)

lb8 = ttk.Label(win2, text='Подтверждение пароля:', font='TN 12')
lb8.place(x=25, y=300)

lb9 = ttk.Label(win2, text='Есть аккаунт?', font='TN 12', cursor='hand2')
lb9.place(x=150, y=380)
lb9.bind('<Button-1>', lambda event: switch_to_authorization())


ent_var3 = tk.StringVar()
ent3 = ttk.Entry(win2, textvariable=ent_var3, width=20)
ent3.place(x=100, y=130)

ent_var4 = tk.StringVar()
ent4 = ttk.Entry(win2, textvariable=ent_var4, width=20,show='*')
ent4.place(x=100, y=220)

ent_var5 = tk.StringVar()
ent5 = ttk.Entry(win2, textvariable=ent_var5, width=20, show='*')
ent5.place(x=210, y=300)

btn2 = ttk.Button(win2, text='Зарегистрироваться', command=lambda: add_account(con, cursor, ent3.get(), ent_var5.get()))
btn2.place(x=140, y=450)


btn4 = ttk.Button(win2, image=eye_image, command=show2)
btn4.place(x=240, y=210)

win2.withdraw()

# запуск программы
win.mainloop()
