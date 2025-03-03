import sqlite3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox
import admin_login
import admin_registration
import user_login
import user_registration


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Page")
        self.geometry("450x300")
        self.configure(bg="#f0f0f0")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.admin_frame = ttk.Frame(self.notebook)
        self.user_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.admin_frame, text="Admin Login")
        self.notebook.add(self.user_frame, text="User Login")

        self.create_admin_widgets()
        self.create_user_widgets()

    def create_admin_widgets(self):
        admin_frame = self.admin_frame

        label_username = tk.Label(admin_frame, text="Username:", bg="#f0f0f0", font=("Book Antiqua", 12))
        label_username.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        entry_username = tk.Entry(admin_frame, width=30, font=("Book Antiqua", 12))
        entry_username.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        label_password = tk.Label(admin_frame, text="Password:", bg="#f0f0f0", font=("Book Antiqua", 12))
        label_password.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        entry_password = tk.Entry(admin_frame, show="*", width=30, font=("Book Antiqua", 12))
        entry_password.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        button_login = tk.Button(admin_frame, text="Login", command=self.admin_login, font=("Book Antiqua", 12),
                                 bg="#4CAF50",
                                 fg="white")
        button_login.grid(row=2, column=0, pady=10, padx=10, sticky="we")

        button_close = tk.Button(admin_frame, text="Close", command=self.close_application, font=("Book Antiqua", 12),
                                 bg="red", fg="white")
        button_close.grid(row=3, columnspan=2, pady=10, padx=10, sticky="we")

    def create_user_widgets(self):
        user_frame = self.user_frame

        label_username = tk.Label(user_frame, text="Username:", bg="#f0f0f0", font=("Book Antiqua", 12))
        label_username.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        entry_username = tk.Entry(user_frame, width=30, font=("Book Antiqua", 12))
        entry_username.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        label_password = tk.Label(user_frame, text="Password:", bg="#f0f0f0", font=("Book Antiqua", 12))
        label_password.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        entry_password = tk.Entry(user_frame, show="*", width=30, font=("Book Antiqua", 12))
        entry_password.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        button_login = tk.Button(user_frame, text="Login", command=self.user_login, font=("Book Antiqua", 12),
                                 bg="#4CAF50", fg="white")
        button_login.grid(row=2, column=0, pady=10, padx=10, sticky="we")

        button_register = tk.Button(user_frame, text="New User Registration", command=self.open_registration,
                                    font=("Book Antiqua", 12), bg="#008CBA", fg="white")
        button_register.grid(row=2, column=1, pady=10, padx=10, sticky="we")

        button_close = tk.Button(user_frame, text="Close", command=self.close_application, font=("Book Antiqua", 12),
                                 bg="red", fg="white")
        button_close.grid(row=3, columnspan=2, pady=10, padx=10, sticky="we")

    def close_application(self):
        self.destroy()
        # self.quit()

    def admin_login(self):
        username = self.admin_frame.winfo_children()[1].get()
        password = self.admin_frame.winfo_children()[3].get()

        # Connecting to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Query to fetch admin credentials from the database
        cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        admin = cursor.fetchone()

        if admin:
            messagebox.showinfo("Login Successful", "Logged in as Admin")
            self.admin_frame.winfo_children()[1].delete(0, tk.END)  # Clear username entry
            self.admin_frame.winfo_children()[3].delete(0, tk.END)  # Clear password entry
            self.withdraw()  # Hide the login page
            admin_login.AdminPage(self)  # Show the admin page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        conn.close()

    def user_login(self):
        username = self.user_frame.winfo_children()[1].get()
        password = self.user_frame.winfo_children()[3].get()

        # Connecting to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Query to fetch user credentials from the database
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Logged in as User")

            self.user_frame.winfo_children()[1].delete(0, tk.END)  # Clear username entry
            self.user_frame.winfo_children()[3].delete(0, tk.END)  # Clear password entry
            self.logged_in_username = username
            user_login.UserPage(self, self.logged_in_username)  # Pass the logged-in username
            self.withdraw()  # Close the login window
            # Add code to show the student page
            # user_login.UserPage(self,aA username)  # Open the main application window without calling mainloop

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        print(self.logged_in_username)
        conn.close()


    # def open_admin_registration(self):
    #     registration_window = admin_registration.AdminRegistrationPage(self)

    def open_registration(self):
        user_registration.UserRegistrationPage(self)

    def show_admin_login(self):
        self.notebook.select(self.admin_frame)

    def show_user_login(self):
        self.notebook.select(self.user_frame)