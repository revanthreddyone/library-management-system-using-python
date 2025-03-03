import sqlite3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

import main_login


class UserPage(tk.Toplevel):
    def __init__(self, master, username):
        super().__init__(master)
        self.title("User Page")
        self.geometry("1300x600")
        self.configure(bg="#f0f0f0")
        self.username = username  # Store the username

        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()



        # Create a menu bar
        menubar = tk.Menu(self)

        # Create a File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        # Set the menu bar
        self.config(menu=menubar)

        # Create tabs for admin functionalities
        self.tabControl = ttk.Notebook(self)


        #Tab for Borrowed Books
        self.tab_borrowed_books = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_borrowed_books, text='Borrowed Book')

        #Tab for Returned Books
        self.tab_returned_books = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_returned_books, text='Returned Books')

        # Tab to Search books
        self.tab_search_books = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_search_books, text='Search Books')

        # Tab to see Booking History
        self.tab_booking_history = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_booking_history, text='Booking History')

        self.tabControl.pack(expand=1, fill="both")

        # Add widgets and functionalities to the "Borrowed Books" tab
        self.setup_borrowed_book_tab()

        # Add widgets and functionalities to the "Returned Book" tab
        self.setup_returned_book_tab()


        # Add widgets and functionalities to the "Search books" tab
        self.setup_search_books_tab()

        # Add widgets and functionalities to the "Booking History" tab
        self.setup_booking_history_tab()

    def setup_borrowed_book_tab(self):
        self.borrowed_frame = tk.Frame(self.tab_borrowed_books, bg="#f0f0f0")
        self.borrowed_frame.pack(fill="both", expand=True)

        self.borrowed_books_label = ttk.Label(self.borrowed_frame, text="Borrowed Books:", font=("Book Antiqua", 14))
        self.borrowed_books_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.borrowed_books_treeview = ttk.Treeview(self.borrowed_frame,
                                                    columns=("Book ID", "Title", "Author", "Due Date","Total_Fine_Due"),
                                                    show="headings", style="Custom.Treeview")
        self.borrowed_books_treeview.heading("Book ID", text="Book ID", anchor="w")
        self.borrowed_books_treeview.heading("Title", text="Title", anchor="w")
        self.borrowed_books_treeview.heading("Author", text="Author", anchor="w")
        self.borrowed_books_treeview.heading("Due Date", text="Due Date", anchor="w")
        self.borrowed_books_treeview.heading("Total_Fine_Due", text="Total_Fine_Due", anchor="w")
        self.borrowed_books_treeview.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.borrowed_frame, orient="vertical", command=self.borrowed_books_treeview.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.borrowed_books_treeview.configure(yscrollcommand=scrollbar.set)

        # Fetch and display borrowed books
        self.display_borrowed_books()

    def display_borrowed_books(self):
        self.borrowed_books_treeview.delete(*self.borrowed_books_treeview.get_children())  # Clear existing data

        try:
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
            user_row = self.cursor.fetchone()
            user_id = user_row[0]

            # Fetch borrowed books for the logged-in user from the database
            self.cursor.execute('''SELECT b.id, b.title, b.author, bh.due_date, bh.total_fine_due 
                                              FROM books b 
                                              INNER JOIN booking_history bh ON b.id = bh.book_id 
                                              WHERE bh.user_id = ? AND bh.return_date IS NULL''', (user_id,))
            borrowed_books = self.cursor.fetchall()


            # Display borrowed books in the Treeview
            for book in borrowed_books:
                self.borrowed_books_treeview.insert("", "end", values=book)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching borrowed books: {str(e)}")

    def setup_returned_book_tab(self):
        self.returned_frame = tk.Frame(self.tab_returned_books, bg="#f0f0f0")
        self.returned_frame.pack(fill="both", expand=True)

        self.returned_books_label = ttk.Label(self.returned_frame, text="Returned Books:", font=("Book Antiqua", 14))
        self.returned_books_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.returned_books_treeview = ttk.Treeview(self.returned_frame, columns=(
        "Book ID", "Title", "Borrowed Date", "Due Date", "Returned Date", "Total_Fine_Paid"),
                                                    show="headings", style="Custom.Treeview")
        self.returned_books_treeview.heading("Book ID", text="Book ID", anchor="w")
        self.returned_books_treeview.heading("Title", text="Title", anchor="w")
        self.returned_books_treeview.heading("Borrowed Date", text="Borrowed Date", anchor="w")
        self.returned_books_treeview.heading("Due Date", text="Due Date", anchor="w")
        self.returned_books_treeview.heading("Returned Date", text="Returned Date", anchor="w")
        self.returned_books_treeview.heading("Total_Fine_Paid", text="Total_Fine_Paid", anchor="w")
        self.returned_books_treeview.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.returned_frame, orient="vertical", command=self.returned_books_treeview.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.returned_books_treeview.configure(yscrollcommand=scrollbar.set)

        # Fetch and display returned books
        self.display_returned_books()

    def display_returned_books(self):
        self.returned_books_treeview.delete(*self.returned_books_treeview.get_children())  # Clear existing data

        try:
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
            user_row = self.cursor.fetchone()
            user_id = user_row[0]
            # Fetch returned books for the logged-in user from the database
            self.cursor.execute('''SELECT b.id, b.title, bh.borrowed_date, bh.due_date, bh.return_date , bh.total_fine_paid
                                   FROM books b 
                                   INNER JOIN booking_history bh ON b.id = bh.book_id 
                                   WHERE bh.user_id = ? AND bh.return_date IS NOT NULL''', (user_id,))
            returned_books = self.cursor.fetchall()

            # Display returned books in the Treeview
            for book in returned_books:
                self.returned_books_treeview.insert("", "end", values=book)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching returned books: {str(e)}")

    def setup_search_books_tab(self):
        self.search_frame = tk.Frame(self.tab_search_books, bg="#f0f0f0")
        self.search_frame.pack(fill="both", expand=True)
        title_label = ttk.Label(self.search_frame, text="Search by Title:")
        title_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_title_entry = ttk.Entry(self.search_frame, width=30)
        self.search_title_entry.grid(row=0, column=1, padx=5, pady=5)

        author_label = ttk.Label(self.search_frame, text="Search by Author:")
        author_label.grid(row=1, column=0, padx=5, pady=5)
        self.search_author_entry = ttk.Entry(self.search_frame, width=30)
        self.search_author_entry.grid(row=1, column=1, padx=5, pady=5)

        id_label = ttk.Label(self.search_frame, text="Search by ID:")
        id_label.grid(row=2, column=0, padx=5, pady=5)
        self.search_id_entry = ttk.Entry(self.search_frame, width=30)
        self.search_id_entry.grid(row=2, column=1, padx=5, pady=5)

        search_button = ttk.Button(self.search_frame, text="Search", command=self.search_books)
        search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.search_result_text = tk.Text(self.search_frame, wrap=tk.WORD, width=60, height=15)
        self.search_result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def search_books(self):
        title = self.search_title_entry.get().strip()
        author = self.search_author_entry.get().strip()
        book_id = self.search_id_entry.get().strip()

        # Check if none of the search fields are provided
        if not any([title, author, book_id]):
            messagebox.showwarning("Warning", "Please enter at least one search field value.")
            return

        search_query = '''SELECT * FROM books WHERE 1=1'''  # Start with always true condition

        params = []  # List to hold parameter values

        if title:
            search_query += " AND title LIKE ?"
            params.append(f"%{title}%")
        if author:
            search_query += " AND author LIKE ?"
            params.append(f"%{author}%")
        if book_id:
            search_query += " AND id = ?"
            params.append(book_id)

        self.cursor.execute(search_query, params)
        books = self.cursor.fetchall()

        self.search_result_text.delete(1.0, tk.END)

        if not books:
            self.search_result_text.insert(tk.END, "No books found.")
        else:
            for book in books:
                status = "Available" if not book[6] else "Borrowed"
                self.search_result_text.insert(tk.END,
                                               f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}\n")

    def setup_booking_history_tab(self):
        self.history_frame = tk.Frame(self.tab_booking_history, bg="#f0f0f0")
        self.history_frame.pack(fill="both", expand=True)

        # Create and configure the search criteria dropdown menu
        search_criteria_label = ttk.Label(self.history_frame, text="Search Criteria:")
        search_criteria_label.grid(row=0, column=0, padx=(5, 2), pady=1, sticky="w")

        search_options = ["Book ID", "Dates"]

        self.search_criteria_combo = ttk.Combobox(self.history_frame, values=search_options, state="readonly")
        self.search_criteria_combo.grid(row=0, column=1, padx=(5, 2), pady=1, sticky="w")
        self.search_criteria_combo.current(0)  # Set default value

        # Initially hide all input fields
        self.book_id_label = ttk.Label(self.history_frame, text="Book ID:")
        self.book_id_entry = ttk.Entry(self.history_frame, width=15)

        self.from_date_label = ttk.Label(self.history_frame, text="From:")
        self.from_date_entry = DateEntry(self.history_frame, width=12, background='darkblue',
                                         foreground='white', borderwidth=2, year=2024)

        self.to_date_label = ttk.Label(self.history_frame, text="To:")
        self.to_date_entry = DateEntry(self.history_frame, width=12, background='darkblue',
                                       foreground='white', borderwidth=2, year=2024)

        self.search_criteria_combo.bind("<<ComboboxSelected>>", self.on_search_criteria_select)

        # Create search button
        search_button = ttk.Button(self.history_frame, text="Search", command=self.search_booking_history)
        search_button.grid(row=0, column=2, padx=(5, 2), pady=1, sticky="w")

        # Adjust grid positions for input fields
        self.book_id_label.grid(row=1, column=0, padx=(5, 2), pady=1, sticky="e")
        self.book_id_entry.grid(row=1, column=1, padx=(0, 2), pady=1, sticky="w")

        self.from_date_label.grid(row=1, column=2, padx=(5, 2), pady=1, sticky="e")
        self.from_date_entry.grid(row=1, column=3, padx=(0, 2), pady=1, sticky="w")

        self.to_date_label.grid(row=1, column=4, padx=(5, 2), pady=1, sticky="e")
        self.to_date_entry.grid(row=1, column=5, padx=(0, 2), pady=1, sticky="w")

        # Create Treeview to display search results
        self.history_result_treeview = ttk.Treeview(self.history_frame,
                                                    columns=("SNo","User_Id","Book_id", "Title", "Author", "Borrowed Date",
                                                             "Due Date", "Return Date", "Total Fine Due",
                                                             "Total Fine Paid"),
                                                    show="headings", style="Custom.Treeview")
        # Define column headings
        self.history_result_treeview.heading("SNo", text="SNo", anchor="w")
        self.history_result_treeview.heading("User_Id", text="User_Id", anchor="w")
        self.history_result_treeview.heading("Book_id", text="Book ID", anchor="w")
        self.history_result_treeview.heading("Title", text="Title", anchor="w")
        self.history_result_treeview.heading("Author", text="Author", anchor="w")
        self.history_result_treeview.heading("Borrowed Date", text="Borrowed Date", anchor="w")
        self.history_result_treeview.heading("Due Date", text="Due Date", anchor="w")
        self.history_result_treeview.heading("Return Date", text="Return Date", anchor="w")
        self.history_result_treeview.heading("Total Fine Due", text="Total Fine Due", anchor="w")
        self.history_result_treeview.heading("Total Fine Paid", text="Total Fine Paid", anchor="w")

        # Set column widths
        self.history_result_treeview.column("SNo", width=100)
        self.history_result_treeview.column("User_Id", width=100)
        self.history_result_treeview.column("Book_id", width=100)
        self.history_result_treeview.column("Title", width=150)
        self.history_result_treeview.column("Author", width=150)
        self.history_result_treeview.column("Borrowed Date", width=120)
        self.history_result_treeview.column("Due Date", width=120)
        self.history_result_treeview.column("Return Date", width=120)
        self.history_result_treeview.column("Total Fine Due", width=120)
        self.history_result_treeview.column("Total Fine Paid", width=120)

        # Display Treeview
        self.history_result_treeview.grid(row=2, column=0, columnspan=6, padx=1, pady=1, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_result_treeview.yview)
        scrollbar.grid(row=2, column=6, sticky="ns")
        self.history_result_treeview.configure(yscrollcommand=scrollbar.set)

    def on_search_criteria_select(self, event):
        selected_criteria = self.search_criteria_combo.get()

        if selected_criteria == "Book ID":
            self.hide_date_fields()
            self.show_book_id_fields()
        elif selected_criteria == "Dates":
            self.hide_book_id_fields()
            self.show_date_fields()

    def hide_date_fields(self):
        self.from_date_label.grid_forget()
        self.from_date_entry.grid_forget()
        self.to_date_label.grid_forget()
        self.to_date_entry.grid_forget()

    def show_date_fields(self):
        self.from_date_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.from_date_entry.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.to_date_label.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.to_date_entry.grid(row=1, column=4, padx=5, pady=5, sticky="w")

    def hide_book_id_fields(self):
        self.book_id_label.grid_forget()
        self.book_id_entry.grid_forget()

    def show_book_id_fields(self):
        self.book_id_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.book_id_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    def search_booking_history(self):
        selected_criteria = self.search_criteria_combo.get()

        if selected_criteria == "Book ID":
            book_id = self.book_id_entry.get().strip()
            if not book_id:
                messagebox.showerror("Error", "Please enter a book ID.")
                return

            # Fetch book interactions for the specified book ID

            self.cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
            user_row = self.cursor.fetchone()
            user_id = user_row[0]


            query = f"SELECT * FROM user_booking_history WHERE book_id = ? and user_id = ?"
            self.cursor.execute(query, (book_id,user_id,))
            results = self.cursor.fetchall()
        elif selected_criteria == "Dates":
            from_date = self.from_date_entry.get_date()
            to_date = self.to_date_entry.get_date()

            if not (from_date and to_date):
                messagebox.showerror("Error", "Please enter both start and end dates.")
                return

            # Fetch book interactions within the specified date range
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
            user_row = self.cursor.fetchone()
            user_id = user_row[0]

            query = f"SELECT * FROM user_booking_history WHERE borrowed_date BETWEEN ? AND ? and user_id = ?"
            self.cursor.execute(query, (from_date, to_date,user_id,))
            results = self.cursor.fetchall()

        # Populate the Treeview with the search results
        self.history_result_treeview.delete(*self.history_result_treeview.get_children())
        for entry in results:
            self.history_result_treeview.insert("", "end", values=entry)

    def logout(self):
        self.destroy()
        main_login.LoginPage().show_admin_login()

    def exit_application(self):
        self.cursor.close()  # Close the cursor
        self.conn.close()  # Close the connection
        self.master.destroy()