import sqlite3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox



class AdminRegistrationPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Admin Registration")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

        self.label_username = tk.Label(self, text="Username:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_username.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.entry_username = tk.Entry(self, width=30, font=("Book Antiqua", 12))
        self.entry_username.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        self.label_password = tk.Label(self, text="Password:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_password.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.entry_password = tk.Entry(self, show="*", width=30, font=("Book Antiqua", 12))
        self.entry_password.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.button_register = tk.Button(self, text="Register", command=self.register_admin, font=("Book Antiqua", 12),
                                         bg="#008CBA", fg="white")
        self.button_register.grid(row=2, columnspan=2, pady=10)

        self.button_back_to_login = tk.Button(self, text="Back to Login", command=self.back_to_login,
                                              font=("Book Antiqua", 12), bg="#FF5733", fg="white")
        self.button_back_to_login.grid(row=3, columnspan=2, pady=10)

    def register_admin(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Connecting to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        try:
            # Inserting admin details into the database
            cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Registration Successful", "New admin registered successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()
            self.destroy()

    def back_to_login(self):
        self.destroy()
        # self.master.show_admin_login()  # Assuming a method named show_admin_login in the parent class to display Admin Login page