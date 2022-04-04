import json
from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox

import clipboard


# ---------------------------- PASSWORD SEARCH ------------------------------- #
def find_password():
    search = website.get().title()
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title='Missing Data', message='No Data File Found!')
    else:
        for key, value in data.items():
            if search == key:
                email = value['Email']
                password = value['Password']

                use = messagebox.askokcancel(title='Account Found',
                                             message=f'Do you want to load these details?\n\nEmail: {email}\n'
                                                     f'Password: {password}'
                                                     f'\n\nFor {search}')

                if use:
                    email_input.delete(0, END)
                    passwords.delete(0, END)
                    email_input.insert(0, email)
                    passwords.insert(0, password)
                    clipboard.copy(password)
                else:
                    website.focus()
                break

        else:
            messagebox.showinfo(title=f'{search}', message='No Details for the website exist!')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_password():
    # Password Generator Project
    passwords.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = ''.join(password_list)
    passwords.insert(0, password)
    clipboard.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website_entry = website.get()
    email_entry = email_input.get()
    password_entry = passwords.get()

    new_data = {
        website_entry: {
            'Email': email_entry,
            'Password': password_entry
        }

    }

    if len(website_entry) == 0 or len(password_entry) == 0:
        messagebox.showinfo(title='Oops!', message='No field should be left empty')
    else:
        save = messagebox.askokcancel(title=f'{website_entry}',
                                      message=f'Do you want to save these details?\n\nEmail: {email_entry}\n'
                                              f'Password: {password_entry}')
        if save:
            try:
                with open('data.json', 'r') as file:
                    # Reading Old data
                    data = json.load(file)
                    # Updating Old data
                    data.update(new_data)

            except FileNotFoundError:
                with open('data.json', 'w') as new_json:
                    json.dump(new_data, new_json, indent=4)
            else:
                with open('data.json', 'w') as json_file:
                    # Saving new json file
                    json.dump(data, json_file, indent=4)
            finally:
                clipboard.copy(password_entry)

                website.delete(0, END)
                passwords.delete(0, END)
                passwords.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)
window.minsize(480, 300)

canvas = Canvas(width=200, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels ----------------------------------------------
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)
password_label = Label(text='Password:')
password_label.grid(row=3, column=0)
# Labels ----------------------------------------------

# Entries ---------------------------------------------

passwords = Entry(width=35)
passwords.grid(row=3, column=1)

website = Entry(width=35)
website.focus()
website.grid(row=1, column=1)

email_input = Entry(width=35)
email_input.insert(0, 'myemail@email.com')
email_input.grid(row=2, column=1)

# Entries ---------------------------------------------

# Buttons ---------------------------------------------
generate_password = Button(text='Generate Password', width=14, command=gen_password)
generate_password.grid(row=3, column=3)

add = Button(text='Add', width=30, command=add_password)
add.grid(row=4, column=1, columnspan=2)

search_btn = Button(text='Search', width=14, command=find_password)
search_btn.grid(row=1, column=3)
# Buttons ---------------------------------------------

window.mainloop()
