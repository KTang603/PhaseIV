import tkinter as tk
from tkinter import ttk

import mysql.connector
from MySQLdb import connect


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        database= 'flight_tracking',
        user='root',
        password='737nnn'
    )


def make_procedure(root, proc_name, parameters):
    window = ttk.Frame(root)
    name = ttk.Label(window, text=proc_name, font = ("Comic Sans MS", 20))
    name.grid(row = 0, column = 0)

    row = 1
    entries = []
    for x in parameters:
        label = ttk.Label(window, text=x[0], font=("Comic Sans MS", 12))
        entry = ttk.Entry(window)
        label.grid(row = row, column = 0)
        entry.grid(row= row, column = 1)
        entries.append(entry)
        row += 1
    button = ttk.Button(window, text = "CALL", command = lambda: call_procedure(proc_name, entries, parameters))
    button.grid(row = row, column = 0)
    return window

def call_procedure(proc_name, entries, parameters):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        call_string = "Call " + proc_name + "("
        count = 0
        for entry in entries:
            if count > 0:
                call_string += ", "
            if not entry.get():
                raise Exception

            param = entry.get().strip()
            if "char" in parameters[count][1]:
                param = "\'" + param + "\'"
            call_string = call_string + param
            count += 1
        call_string += ")"
        print(call_string)
        cursor.execute(call_string)
        connection.close()
        print("Success (probably)")
    except Exception:
        print("Failure")

def make_view(root, view_name):
    window = ttk.Frame(root)
    name = ttk.Label(window, text=view_name, font=("Comic Sans MS", 20))
    name.grid(row=0, column=0)

    text = tk.Text(window, wrap = "none", width = 80, height = 20, font = ("Comic Sans MS", 10))
    text.grid(row = 1, column = 0)
    button = ttk.Button(window, text = "View", command=lambda: get_view(view_name, text))
    button.grid(row = 3, column = 0)

    scroll_vert = ttk.Scrollbar(window, orient='vertical')
    scroll_vert.grid(row = 1, column = 1)
    scroll_hori = ttk.Scrollbar(window, orient='horizontal')
    scroll_hori.grid(row=2, column=0)
    text.configure(xscrollcommand=scroll_hori.set)


    return window

def get_view(view_name, text):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("Select * from " + view_name)
        view = cursor.fetchall()
        # print(view[0])
        if text:
            print("Text is here")
        count = 1
        for row in view:
            bullet = str(count) + ". "
            line = ' | '.join(str(x) for x in row)

            text.insert("end", bullet + line + "\n")
            count += 1

    except Exception:
        print("Can't get View")


def main():


    root = tk.Tk()
    root.title("Airport Management System")
    root.geometry("800x500")


    master = ttk.Notebook(root)
    title = ttk.Label(root, text="Airport Management System", font=("bold")).pack()

    procedures = [
        ("add_airplane", [("Airline ID", "varchar(50)"), ("Tail Num", "varchar(50)"), ("Seat Cap.", "integer"), ("Speed", "integer"), ("Location ID", "varchar(50)"), ("Plane Type", "varchar(100)"), ("Maintenanced", "boolean"), ("Model", "integer"), ("Has Neo", "integer")]),
        ("add_airport", [("Airport ID", "char(3)"), ("Airport", "varchar(200)"), ("City", "varchar(100)"), ("State", "varchar(100)") , ("Country", "char(3)"), ("Location ID", "varchar(50)")]),
        ("add_person", [("Person ID", "varchar(50)"), ("First Name", "varchar(100)"), ("Last Name", "varchar(50)"), ("Location ID", "varchar(50)"), ("TaxID", "varchar(50)"), ("Experience", "integer") , ("Miles", "integer"), ("Funds", "integer")]),
        ("grant_or_revoke_pilot_license", [("Person ID", "varchar(50)"), ("License", "varchar(100)")]),
        ("offer_flight", [("Flight ID", "varchar(50)"), ("Route ID", "varchar(50)"), ("Supporting Airline", "varchar(50)"), ("Support Tail", "varchar(50)"), ("Progress", "integer"), ("Next Time", "time"), ("Cost", "integer")]),
        ("flight_landing", [("Flight ID", "varchar(50)")]),
        ("flight_takeoff", [("Flight ID", "varchar(50)")]),
        ("passengers_board", [("Flight ID", "varchar(50)")]),
        ("passengers_disembark", [("Flight ID", "varchar(50)")]),
        ("assign_pilot", [("Flight ID", "varchar(50)"), ("Person ID", "varchar(50)")]),
        ("recycle_crew", [("Flight ID", "varchar(50)")]),
        ("retire_flight", [("Flight ID", "varchar(50)")]),
        ("simulation_cycle", [])
    ]

    views = [
        "flights_in_the_air",
        "flights_on_the_ground",
        "people_in_the_air",
        "people_on_the_ground",
        "route_summary",
        "alternative_airports"
    ]

    for procedure, parameters in procedures:
        master.add(make_procedure(master, procedure, parameters), text=procedure)

    for view in views:
        master.add(make_view(master, view), text=view)

    master.pack(expand=1, fill='both')

    root.mainloop()

if __name__ == "__main__":
    main()
