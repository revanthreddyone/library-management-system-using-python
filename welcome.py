import tkinter as tk
import main_login


class WelcomePage(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Welcome")
        self.geometry("800x600")

        # Load background image
        self.background_image = tk.PhotoImage(file="img.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create and place the title label
        title_label = tk.Label(self, text="Library Management System", font=("Book Antiqua", 28, "bold"),foreground="blue")
        title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Create LOGIN button
        self.login_button = tk.Button(self, text="LOGIN", command=self.open_login_window, bg="#4CAF50", fg="white", font=("Book Antiqua", 10, "bold"))
        self.login_button.place(relx=0.1, rely=0.09, anchor="w")

        # Create Close button
        self.close_button = tk.Button(self, text="Close", command=self.close_welcome, bg="red", fg="white", font=("Book Antiqua", 10, "bold"))
        self.close_button.place(relx=0.9, rely=0.09, anchor="e")

    def open_login_window(self):
        # Function to open the login window
        login_window = main_login.LoginPage()
        self.withdraw()

    def close_welcome(self):
        self.destroy()
