# main.py

import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class LoanManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Management System © hack_limitless")
        self.root.geometry("1350x720+0+0")
        self.root.configure(bg="#dbe9ff")

        # ===== TITLE =====
        title = Label(
            self.root,
            text="Loan Management System",
            font=("Comic Sans MS", 20),
            bd=8,
            bg='#0b1f3a',
            fg='white'
        )
        title.pack(side=TOP, fill=X)

        # ================= VARIABLES =================
        self.LoanId = StringVar()
        self.name = StringVar()
        self.mob = StringVar()
        self.aadhar = StringVar()
        self.add = StringVar()
        self.pin = StringVar()
        self.amount = StringVar()
        self.year = StringVar()
        self.rate = StringVar()
        self.mpay = StringVar()
        self.tpay = StringVar()

        self.search_var = StringVar()

        # ================= LEFT PANEL =================
        Detail_F = Frame(self.root, bd=4, relief=RIDGE, bg='#ffffff')
        Detail_F.place(x=10, y=90, width=520, height=620)

        fields = [
            ("Loan Id", self.LoanId),
            ("Full Name", self.name),
            ("Mobile No.", self.mob),
            ("Aadhar No.", self.aadhar),
            ("Address", self.add),
            ("PinCode", self.pin),
            ("Amount of Loan", self.amount),
            ("Number of years", self.year),
            ("Interest Rate/Year", self.rate),
        ]

        for i, (txt, var) in enumerate(fields):
            Label(Detail_F, text=txt,
                  font=("Comic Sans MS", 12),
                  bg="white", fg="#0b1f3a").grid(row=i, column=0, pady=10, padx=20, sticky="w")

            Entry(Detail_F, font=("Comic Sans MS", 10),
                  bd=3, bg="#f7fbff",
                  textvariable=var).grid(row=i, column=1, pady=10)

        # ================= AI FUNCTION =================
        Label(Detail_F, text="🤖 AI Suggestion:",
              font=("Comic Sans MS", 12),
              bg="white", fg="#0b1f3a").grid(row=9, column=0, sticky="w", padx=20)

        self.ai_label = Label(Detail_F, text="Waiting for input...",
                              font=("Comic Sans MS", 10),
                              bg="white", fg="green")
        self.ai_label.grid(row=9, column=1, sticky="w")

        Button(Detail_F, text="Run AI Check",
               bg="#0b1f3a", fg="white",
               command=self.ai_suggest).grid(row=10, column=1, pady=10)

        # ================= SEARCH =================
        searchFrame = Frame(self.root, bg="#dbe9ff")
        searchFrame.place(x=550, y=70)

        Entry(searchFrame, textvariable=self.search_var,
              font=("Arial", 12),
              width=30).grid(row=0, column=0, padx=5)

        Button(searchFrame, text="Search",
               bg="#0b1f3a", fg="white",
               command=self.search_data).grid(row=0, column=1)

        Button(searchFrame, text="Show All",
               bg="#1f3c88", fg="white",
               command=self.fetch_data).grid(row=0, column=2, padx=5)

        # ================= TABLE (FIXED) =================
        recordFrame = Frame(self.root, bd=5, relief=RIDGE, bg="#dbe9ff")
        recordFrame.place(x=535, y=120, width=810, height=530)

        yscroll = Scrollbar(recordFrame, orient=VERTICAL)

        self.employee_table = ttk.Treeview(
            recordFrame,
            columns=("Loan_Id","Name","Mobile","Aadhar","Address","Pincode",
                     "Amount","Year","Rate","Monthly","Total"),
            yscrollcommand=yscroll.set
        )

        self.employee_table["show"] = "headings"

        yscroll.pack(side=RIGHT, fill=Y)
        yscroll.config(command=self.employee_table.yview)

        headings = ["Loan ID","Name","Mobile","Aadhar","Address","Pincode",
                    "Amount","Years","Rate","Monthly Payment","Total Payment"]

        for col, head in zip(self.employee_table["columns"], headings):
            self.employee_table.heading(col, text=head)
            self.employee_table.column(col, width=100)

        self.employee_table.pack(fill=BOTH, expand=1)

        self.fetch_data()
        self.employee_table.bind("<ButtonRelease-1>", self.get_cursor)

        # ================= BUTTONS =================
        btnFrame = Frame(self.root, bd=5, relief=RIDGE, bg="#dbe9ff")
        btnFrame.place(x=700, y=650, width=480, height=50)

        Button(btnFrame, text='Add record', bg="#0b1f3a", fg="white",
               command=self.addrecord).grid(row=0, column=0, padx=10)

        Button(btnFrame, text='Update', bg="#0b1f3a", fg="white",
               command=self.update).grid(row=0, column=1, padx=10)

        Button(btnFrame, text='Delete', bg="#0b1f3a", fg="white",
               command=self.delete).grid(row=0, column=2, padx=10)

        Button(btnFrame, text='Reset', bg="#0b1f3a", fg="white",
               command=self.reset).grid(row=0, column=3, padx=10)

    # ================= REST SAME (NO CHANGE) =================
    def ai_suggest(self):
        try:
            amt = float(self.amount.get())
            rate = float(self.rate.get())

            if amt > 500000:
                self.ai_label.config(text="⚠ High loan risk detected")
            elif rate > 15:
                self.ai_label.config(text="⚠ High interest warning")
            else:
                self.ai_label.config(text="✅ Loan looks safe")
        except:
            self.ai_label.config(text="Enter valid values")

    def search_data(self):
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM customer WHERE Name LIKE ? OR Loan_Id LIKE ?",
                    ('%' + self.search_var.get() + '%',
                     '%' + self.search_var.get() + '%'))
        rows = cur.fetchall()

        self.employee_table.delete(*self.employee_table.get_children())

        for row in rows:
            self.employee_table.insert('', END, values=row)

        con.close()

    def total(self):
        p = int(self.amount.get())
        r = float(self.rate.get())
        n = int(self.year.get())
        t = (p * r * n) / 100
        m = t / (n * 12)
        self.mpay.set(str(round(m, 2)))
        self.tpay.set(str(t + p))

    def addrecord(self):
        if self.LoanId.get() == '':
            messagebox.showerror('Error', 'Please enter details ?')
        else:
            self.total()
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute("insert into customer values(?,?,?,?,?,?,?,?,?,?,?)", (
                self.LoanId.get(), self.name.get(), self.mob.get(),
                self.aadhar.get(), self.add.get(), self.pin.get(),
                self.amount.get(), self.year.get(), self.rate.get(),
                self.mpay.get(), self.tpay.get()
            ))
            con.commit()
            con.close()
            self.fetch_data()

    def fetch_data(self):
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute("select * from customer")
        rows = cur.fetchall()

        self.employee_table.delete(*self.employee_table.get_children())

        for row in rows:
            self.employee_table.insert('', END, values=row)

        con.close()

    def update(self):
        self.total()
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute("""update customer set Name=?, MobileNumber=?, AadharNumber=?,
                    Address=?, Pincode=?, Amount=?, Year=?, Rate=?,
                    Monthly_Payment=?, Total_Payment=? where Loan_Id=?""", (
            self.name.get(), self.mob.get(), self.aadhar.get(),
            self.add.get(), self.pin.get(), self.amount.get(),
            self.year.get(), self.rate.get(),
            self.mpay.get(), self.tpay.get(), self.LoanId.get()
        ))
        con.commit()
        con.close()
        self.fetch_data()

    def delete(self):
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute("delete from customer where Loan_Id=?", (self.LoanId.get(),))
        con.commit()
        con.close()
        self.fetch_data()

    def reset(self):
        for var in [self.LoanId, self.name, self.mob, self.aadhar,
                    self.add, self.pin, self.amount, self.year,
                    self.rate, self.mpay, self.tpay]:
            var.set("")

    def get_cursor(self, ev):
        row = self.employee_table.item(self.employee_table.focus())['values']
        self.LoanId.set(row[0])
        self.name.set(row[1])
        self.mob.set(row[2])
        self.aadhar.set(row[3])
        self.add.set(row[4])
        self.pin.set(row[5])
        self.amount.set(row[6])
        self.year.set(row[7])
        self.rate.set(row[8])
        self.mpay.set(row[9])
        self.tpay.set(row[10])


# ================= DATABASE =================
con = sqlite3.connect('loanDetails.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS customer(
Loan_Id varchar(20) primary key,
Name varchar(20),
MobileNumber varchar(20),
AadharNumber varchar(20),
Address varchar(20),
Pincode varchar(20),
Amount varchar(20),
Year varchar(20),
Rate varchar(20),
Monthly_Payment varchar(20),
Total_Payment varchar(20))''')
con.close()