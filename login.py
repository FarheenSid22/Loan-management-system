#login.py
from tkinter import *
from tkinter import messagebox
from main import LoanManager
import time


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Loan System - Login")
        self.root.geometry("650x450+350+150")
        self.root.configure(bg="#dbeafe")  # LIGHT BLUE BACKGROUND
        self.root.resizable(False, False)

        # ===== CENTER CARD =====
        self.card = Frame(
            self.root,
            bg="#ffffff",
            bd=0,
            highlightthickness=2,
            highlightbackground="#1e3a8a"
        )
        self.card.place(relx=0.5, rely=0.5, anchor=CENTER, width=380, height=360)

        # ===== TITLE =====
        Label(
            self.card,
            text="Loan System LOGIN",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg="#1e3a8a"
        ).pack(pady=15)

        # ===== AI HINT LABEL =====
        self.ai_text = Label(
            self.card,
            text="🤖 Secure AI Authentication Active...",
            font=("Arial", 9),
            bg="white",
            fg="#3b82f6"
        )
        self.ai_text.pack()
        self.blink_ai()

        # ===== VARIABLES =====
        self.username = StringVar()
        self.password = StringVar()

        # ===== USERNAME =====
        Label(
            self.card,
            text="Username",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#1e3a8a"
        ).pack(pady=(20, 5))

        self.user_entry = Entry(
            self.card,
            textvariable=self.username,
            font=("Arial", 12),
            bg="#eff6ff",
            fg="#1e3a8a",
            insertbackground="#1e3a8a",
            relief=FLAT,
            highlightthickness=1,
            highlightbackground="#3b82f6"
        )
        self.user_entry.pack(ipady=6, ipadx=10)

        # ===== PASSWORD =====
        Label(
            self.card,
            text="Password",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#1e3a8a"
        ).pack(pady=(15, 5))

        self.pass_entry = Entry(
            self.card,
            textvariable=self.password,
            show="*",
            font=("Arial", 12),
            bg="#eff6ff",
            fg="#1e3a8a",
            insertbackground="#1e3a8a",
            relief=FLAT,
            highlightthickness=1,
            highlightbackground="#3b82f6"
        )
        self.pass_entry.pack(ipady=6, ipadx=10)

        # ===== LOGIN BUTTON =====
        self.login_btn = Button(
            self.card,
            text="LOGIN SECURELY",
            font=("Arial", 12, "bold"),
            bg="#1e3a8a",
            fg="white",
            activebackground="#3b82f6",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.login
        )
        self.login_btn.pack(pady=25, ipadx=10, ipady=6)

        # Hover effect
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#2563eb"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#1e3a8a"))

        # Fade-in animation
        self.fade_in()

    # ===== AI BLINK EFFECT =====
    def blink_ai(self):
        current = self.ai_text.cget("fg")
        new_color = "#60a5fa" if current == "#3b82f6" else "#3b82f6"
        self.ai_text.config(fg=new_color)
        self.root.after(600, self.blink_ai)

    # ===== FADE IN =====
    def fade_in(self):
        for i in range(0, 11):
            self.root.attributes("-alpha", i / 10)
            self.root.update()
            time.sleep(0.03)

    # ===== LOGIN FUNCTION =====
    def login(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.root.destroy()
            new_root = Tk()
            LoanManager(new_root)
        else:
            messagebox.showerror("Error", "Invalid username or password")


# ===== RUN =====
root = Tk()
Login(root)
root.mainloop()