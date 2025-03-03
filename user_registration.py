import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class UserRegistrationPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("User Registration")
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")

        self.name_var = tk.StringVar()
        self.roll_var = tk.StringVar()
        self.user_type_var = tk.StringVar()

        # Creating labels and entry fields in two columns using grid layout
        self.label_user_type = tk.Label(self, text="Type of User:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_user_type.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.entry_user_type = ttk.Combobox(self, width=27, font=("Book Antiqua", 12), textvariable=self.user_type_var)
        self.entry_user_type['values'] = ('Student', 'Faculty')
        self.entry_user_type.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        self.label_name = tk.Label(self, text="Name:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_name.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.entry_name = tk.Entry(self, width=30, font=("Book Antiqua", 12), textvariable=self.name_var)
        self.entry_name.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.label_roll = tk.Label(self, text="Roll Number:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_roll.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        self.entry_roll = tk.Entry(self, width=30, font=("Book Antiqua", 12), textvariable=self.roll_var)
        self.entry_roll.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.label_username = tk.Label(self, text="Username:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_username.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        self.entry_username = tk.Entry(self, width=30, font=("Book Antiqua", 12))
        self.entry_username.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        self.label_password = tk.Label(self, text="Password:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_password.grid(row=4, column=0, pady=5, padx=10, sticky="w")

        self.entry_password = tk.Entry(self, show="*", width=30, font=("Book Antiqua", 12))
        self.entry_password.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        self.label_branch = tk.Label(self, text="Branch/Department:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_branch.grid(row=5, column=0, pady=5, padx=10, sticky="w")

        self.entry_branch = tk.Entry(self, width=30, font=("Book Antiqua", 12))
        self.entry_branch.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        self.button_register = tk.Button(self, text="Register", command=self.register_user,
                                         font=("Book Antiqua", 12), bg="#008CBA", fg="white")
        self.button_register.grid(row=6, columnspan=2, pady=10)

        self.button_back_to_login = tk.Button(self, text="Back to Login", command=self.back_to_login,
                                              font=("Book Antiqua", 12), bg="#FF5733", fg="white")
        self.button_back_to_login.grid(row=7, columnspan=2, pady=10)

        self.entry_name.bind("<KeyRelease>", self.update_username)
        self.entry_roll.bind("<KeyRelease>", self.update_username)

    def update_username(self, event):
        # Get the text from entry_name
        name = self.entry_name.get()
        # Update the name_var
        self.name_var.set(name)

        # Print the current value of name_var
        # print(f"Name: {self.name_var.get()}")

        # Get the text from entry_roll
        roll_number = self.entry_roll.get()
        # Update the roll_var
        self.roll_var.set(roll_number)

        # Print the current value of roll_var
        # print(f"Roll Number: {self.roll_var.get()}")

        # Concatenate name and roll number to generate username
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, name.replace(" ", "") + roll_number)

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        name = self.name_var.get()
        roll_number = self.roll_var.get()
        branch = self.entry_branch.get()
        user_type = self.user_type_var.get()


        if not username or not password or not name or not roll_number or not branch:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Connecting to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        try:
            # Inserting user details into the database
            cursor.execute(
                "INSERT INTO users (username, password, name, roll_number, branch, user_type) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password, name, roll_number, branch, user_type)
            )
            conn.commit()
            messagebox.showinfo("Registration Successful", "New user registered successfully!")
        except sqlite3.IntegrityError as e:
            print("SQLite error:", e)  # Print the specific SQLite error message
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", "Username already exists.")
            else:
                messagebox.showerror("Error", "An error occurred while registering the user.")
        finally:
            conn.close()
            self.destroy()

    def back_to_login(self):
        self.destroy()
        self.master.show_user_login()  # Assuming a method named show_login_page in the parent class to display Login page
