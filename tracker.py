import math
from datetime import datetime
import customtkinter
import customtkinter as ctk
import json
import os

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

window = ctk.CTk()
window.geometry("915x412")
window.title("Money Tracker")



monthly_limit_var = ctk.IntVar()
fixed_expense_var = ctk.IntVar()
sonuc_var = ctk.StringVar()
harcadin_mi_var = ctk.IntVar()
para_girisi_var = ctk.IntVar()

one = [1, 3, 5, 7, 8, 10, 12]
zero = [4, 6, 9, 11]

days_in_month = 0
if datetime.now().month == 2 and datetime.now().year % 4 == 0:
    days_in_month = 29
elif datetime.now().month == 2 and datetime.now().year % 4 != 0:
    days_in_month = 28
elif datetime.now().month in one:
    days_in_month = 31
elif datetime.now().month in zero:
    days_in_month = 30

def calculate():
    global days_in_month

    monthly_limit = monthly_limit_var.get()
    fixed_expense = fixed_expense_var.get()

    data = {
        "month": datetime.now().month,
        "limit": monthly_limit,
        "expenses": fixed_expense
    }
    with open("limit_and_expenses.txt", "w") as file:
        json.dump(data, file)

    remaining_days = days_in_month - (datetime.now().day - 1)

    monthly = monthly_limit - fixed_expense
    daily_limit = math.trunc((monthly / remaining_days) * 100) / 100

    sonuc_var.set("Your current daily limit for the rest of the month: " + str(daily_limit))

    sonuc_label = ctk.CTkLabel(window, textvariable=sonuc_var,font=("helvetica", 18))
    sonuc_label.grid(row=6, column=1, pady=10)

    monthly_limit_label.destroy()
    monthly_limit_entry.destroy()
    fixed_expense_label.destroy()
    fixed_expense_entry.destroy()
    calc_button.destroy()

    window.update()
    submit()


def submit():
    global harcadin_mi_label, harcadin_mi_entry, para_girisi_label, para_girisi_entry, sub_button, edit_button, exit_button

    harcadin_mi_label = ctk.CTkLabel(
        window,
        text="Enter how much you spent today: ",
        font=("helvetica", 24)
    )
    harcadin_mi_entry = ctk.CTkEntry(
        window,
        textvariable=harcadin_mi_var,
        font=("helvetica", 18)
    )
    para_girisi_label = ctk.CTkLabel(
        window,
        text="Enter how much you received today: ",
        font=("helvetica", 24)
    )
    para_girisi_entry = ctk.CTkEntry(
        window,
        textvariable=para_girisi_var,
        font=("helvetica", 18)
    )
    sub_button = ctk.CTkButton(
        window,
        text="Submit",
        command=harcamis,
        font=("helvetica", 14)
    )
    exit_button = ctk.CTkButton(
        window,
        text="Exit",
        command=window.destroy,
        font=("helvetica", 14)
    )

    harcadin_mi_label.grid(row=4, column=0, pady=10, padx=10)
    harcadin_mi_entry.grid(row=4, column=1, pady=10)
    para_girisi_label.grid(row=5, column=0, pady=10, padx=10)
    para_girisi_entry.grid(row=5, column=1, pady=10)
    sub_button.grid(row=7, column=1, pady=10)
    exit_button.grid(row=8, column=1, pady=10)

def harcamis():
    with open("limit_and_expenses.txt", "r") as file:
        data = json.load(file)

    monthly_limit = data["limit"]
    fixed_expense = data["expenses"]
    daily_spent = harcadin_mi_var.get()
    daily_earned = para_girisi_var.get()

    remaining_days = days_in_month - datetime.now().day
    monthly = monthly_limit - fixed_expense

    new_monthly = monthly - (daily_spent-daily_earned)
    new_daily_limit = math.trunc((new_monthly / remaining_days) * 100) / 100

    sonuc_var.set("Your new daily limit for the rest of the month: " + str(new_daily_limit))
    sonuc_label = ctk.CTkLabel(window, textvariable=sonuc_var,font=("helvetica", 18))
    sonuc_label.grid(row=6, column=1, pady=10)

    file.close()
    data2 = {
        "month": datetime.now().month,
        "limit": new_monthly,
        "expenses": fixed_expense
    }
    with open("limit_and_expenses.txt", "w") as file:
        json.dump(data2, file)


monthly_limit_label = ctk.CTkLabel(
    window,
    text="Enter your monthly limit: ",
    font=("helvetica", 24))

monthly_limit_entry = ctk.CTkEntry(
    window,
    textvariable=monthly_limit_var,
    font=("helvetica", 18))

fixed_expense_label = ctk.CTkLabel(
    window,
    text="Enter your fixed monthly expenses (rent, memberships etc.): ",
    font=("helvetica", 24))

fixed_expense_entry = ctk.CTkEntry(
    window,
    textvariable=fixed_expense_var,
    font=("helvetica", 18))

calc_button = ctk.CTkButton(
    window,
    text="Calculate",
    command=calculate,
    font=("helvetica", 14))

exit_button = ctk.CTkButton(
        window,
        text="Exit",
        command=window.destroy,
        font=("helvetica", 14)
    )

def start():
    monthly_limit_label.grid(row=0, column=0, pady=10, padx=10)
    monthly_limit_entry.grid(row=0, column=1, pady=10)
    fixed_expense_label.grid(row=1, column=0, pady=10, padx=10)
    fixed_expense_entry.grid(row=1, column=1, pady=10)
    calc_button.grid(row=2, column=1, pady=10)
    exit_button.grid(row=3, column=1, pady=10)

    window.mainloop()

if os.stat("limit_and_expenses.txt").st_size == 0:
    monthly_limit_label.grid(row=0, column=0, pady=10, padx=10)
    monthly_limit_entry.grid(row=0, column=1, pady=10)
    fixed_expense_label.grid(row=1, column=0, pady=10, padx=10)
    fixed_expense_entry.grid(row=1, column=1, pady=10)
    calc_button.grid(row=2, column=1, pady=10)

    window.mainloop()
else:
    with open("limit_and_expenses.txt", "r") as file:
        data = json.load(file)
        if data["month"] != datetime.now().month:
            start()
        elif data["month"] == datetime.now().month:
            with open("limit_and_expenses.txt", "r") as file:
                y = json.load(file)

            monthly_limit = y["limit"]
            fixed_expense = y["expenses"]

            remaining_days = days_in_month - (datetime.now().day - 1)

            monthly = monthly_limit - fixed_expense
            daily_limit = math.trunc((monthly / remaining_days) * 100) / 100

            sonuc_var.set("Your current daily limit for the rest of the month: " + str(daily_limit))

            sonuc_label = ctk.CTkLabel(window, textvariable=sonuc_var, font=("helvetica", 18))
            sonuc_label.grid(row=6, column=1, pady=10)

            submit()
            window.mainloop()

