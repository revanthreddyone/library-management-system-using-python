import sqlite3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox

import admin_registration
import main_login


class AdminPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.title("Admin Page")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        # Create a menu bar
        menubar = tk.Menu(self)

        # Create a File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        # file_menu.add_command(label="New Admin Registration", command=self.open_admin_registration)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="New Admin Registration", command=self.open_admin_registration)

        # Set the menu bar
        self.config(menu=menubar)

        # Create tabs for admin functionalities
        self.tabControl = ttk.Notebook(self)

        # Add tab for Add Book
        self.tab_add_book = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_add_book, text='Add Book')

        # Add tab for Issue Book
        self.tab_issue_book = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_issue_book, text='Issue Book')

        # Add tab for Return Book
        self.tab_return_book = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_return_book, text='Return Book')

        # Add tab for Delete
        self.tab_delete_book = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_delete_book, text='Delete Book')

        # Add tab for Display
        self.tab_display_books = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_display_books, text='Display Books')

        # Add tab for Search
        self.tab_search_books = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_search_books, text='Search Books')

        # Add tab for Booking History
        self.tab_booking_history = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_booking_history, text='Booking History')

        self.tabControl.pack(expand=1, fill="both")

        # Add widgets and functionalities to the "Add Book" tab
        self.setup_add_book_tab()

        # Add widgets and functionalities to the "Issue Book" tab
        self.setup_issue_book_tab()
        # Add widgets and functionalities to the "Return Book" tab
        self.setup_return_book_tab()

        # Add widgets and functionalities to the "Delete book" tab
        self.setup_delete_books_tab()

        # Add widgets and functionalities to the "Display books" tab
        self.setup_display_books_tab()

        # Add widgets and functionalities to the "Search books" tab
        self.setup_search_books_tab()

        # Add widgets and functionalities to the "Booking History" tab
        self.setup_booking_history_tab()

    def open_admin_registration(self):
        admin_registration_page = admin_registration.AdminRegistrationPage(self)
        admin_registration_page.grab_set()

    def setup_add_book_tab(self):
        # Frame to hold entry fields
        self.entry_frame = tk.Frame(self.tab_add_book, bg="#f0f0f0")
        self.entry_frame.pack(fill="both", expand=True)

        # Title entry
        self.label_book_title = tk.Label(self.entry_frame, text="Title:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_book_title.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_book_title = tk.Entry(self.entry_frame, width=40, font=("Book Antiqua", 12))
        self.entry_book_title.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Author entry
        self.label_book_author = tk.Label(self.entry_frame, text="Author:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_book_author.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_book_author = tk.Entry(self.entry_frame, width=40, font=("Book Antiqua", 12))
        self.entry_book_author.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Category entry
        self.label_book_category = tk.Label(self.entry_frame, text="Category:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_book_category.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_book_category = tk.Entry(self.entry_frame, width=40, font=("Book Antiqua", 12))
        self.entry_book_category.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Genre entry
        self.label_book_genre = tk.Label(self.entry_frame, text="Genre:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_book_genre.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_book_genre = tk.Entry(self.entry_frame, width=40, font=("Book Antiqua", 12))
        self.entry_book_genre.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Quantity entry
        # self.label_book_quantity = tk.Label(self.entry_frame, text="Quantity:", bg="#f0f0f0", font=("Book Antiqua", 12))
        # self.label_book_quantity.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        # self.entry_book_quantity = tk.Entry(self.entry_frame, width=40, font=("Book Antiqua", 12))
        # self.entry_book_quantity.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Add book button
        self.button_add_book = tk.Button(self.entry_frame, text="Add Book", command=self.add_book,
                                         font=("Book Antiqua", 12), bg="#008CBA", fg="white")
        self.button_add_book.grid(row=5, columnspan=2, pady=20)

    def add_book(self):
        title = self.entry_book_title.get()
        author = self.entry_book_author.get()
        category = self.entry_book_category.get()
        genre = self.entry_book_genre.get()

        # Check if all fields are filled
        if not title or not author :
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if quantity is a positive integer
        # try:
        #     quantity = int(quantity)
        #     if quantity <= 0:
        #         raise ValueError
        # except ValueError:
        #     messagebox.showerror("Error", "Quantity must be a positive integer.")
        #     return

        # Add book to database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO books (title, author,  book_added_date,category_id,genre_id,is_borrowed) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, author,  current_datetime,category,genre,0))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Book added successfully.")

        # Clear the entry fields
        self.entry_book_title.delete(0, tk.END)
        self.entry_book_author.delete(0, tk.END)
        self.entry_book_category.delete(0, tk.END)
        self.entry_book_genre.delete(0, tk.END)

    def setup_issue_book_tab(self):
        # Frame to hold entry fields
        self.issue_frame = tk.Frame(self.tab_issue_book, bg="#f0f0f0")
        self.issue_frame.pack(fill="both", expand=True)

        # Add widgets and functionalities for issuing book
        # Book ID
        self.label_issue_book_id = tk.Label(self.issue_frame, text="Book ID:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_issue_book_id.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.issue_id_entry = tk.Entry(self.issue_frame, width=40, font=("Book Antiqua", 12))
        self.issue_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # # Title entry
        # self.label_issue_book_title = tk.Label(issue_frame, text="Title:", bg="#f0f0f0", font=("Book Antiqua", 12))
        # self.label_issue_book_title.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        # self.entry_issue_book_title = tk.Entry(issue_frame, width=40, font=("Book Antiqua", 12))
        # self.entry_issue_book_title.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        #
        # Member ID entry
        self.label_issue_member_id = tk.Label(self.issue_frame, text="Member ID:", bg="#f0f0f0", font=("Book Antiqua", 12))
        self.label_issue_member_id.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_issue_member_id = tk.Entry(self.issue_frame, width=40, font=("Book Antiqua", 12))
        self.entry_issue_member_id.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Issue book button
        self.button_issue_book = tk.Button(self.issue_frame, text="Issue Book", command=self.issue_book,
                                           font=("Book Antiqua", 12), bg="#008CBA", fg="white")
        self.button_issue_book.grid(row=3, columnspan=2, pady=20)

    def issue_book(self):
        book_id = self.issue_id_entry.get().strip()
        member_id = self.entry_issue_member_id.get().strip()

        if not book_id:
            messagebox.showerror("Error", "Book ID cannot be empty.")
            return

        if not member_id:
            messagebox.showerror("Error", "Member ID cannot be empty.")
            return

        # Check if the book exists
        self.cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id,))
        book = self.cursor.fetchone()
        if not book:
            messagebox.showerror("Error", "Book not found.")
            return

        if book[6]:
            messagebox.showerror("Error", "Book is already issued.")
            return

        # Check if the member exists
        self.cursor.execute('''SELECT * FROM users WHERE id = ?''', (member_id,))
        user = self.cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found.")
            return
        # Check the number of books already borrowed by the user
        self.cursor.execute('''SELECT COUNT(*) FROM user_booking_history WHERE user_id = ? AND return_date IS NULL''',
                            (member_id,))
        books_borrowed = self.cursor.fetchone()[0]
        print(books_borrowed)
        if books_borrowed >= 5:
            messagebox.showerror("Error", "Maximum limit (5 books) reached for borrowing.")
            return


        # Record borrowing history
        title = book[1]
        author = book[2]
        issued_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''INSERT INTO booking_history (book_id, user_id, issued_date, borrowed_date, due_date) 
                                   VALUES (?, ?, ?, ?, ?)''',
                            (book_id, member_id, issued_date, issued_date, due_date))
        self.cursor.execute('''INSERT INTO user_booking_history (book_id, user_id,title, Author, borrowed_date, due_date) 
                                           VALUES (?, ?, ?, ?,?,?)''',
                            (book_id, member_id, title, author, issued_date, due_date))
        self.conn.commit()

        # Update book status to borrowed
        self.cursor.execute('''UPDATE books SET is_borrowed = ? WHERE id = ?''', (1, book_id))
        self.conn.commit()

        messagebox.showinfo("Success", "Book Issued successfully!")
        self.issue_id_entry.delete(0, tk.END)
        self.entry_issue_member_id.delete(0, tk.END)

    def setup_return_book_tab(self):
        # Frame to hold entry fields
        self.return_frame = tk.Frame(self.tab_return_book, bg="#f0f0f0")
        self.return_frame.pack(fill="both", expand=True)

        # Add widgets and functionalities for returning book
        # Book ID entry
        self.id_label = tk.Label(self.return_frame, text="Book ID:")
        self.id_label.grid(row=0, column=0, padx=5, pady=5)
        self.return_id_entry = ttk.Entry(self.return_frame, width=30)
        self.return_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # # Title entry
        # self.label_return_book_title = tk.Label(self.return_frame, text="Title:", bg="#f0f0f0", font=("Book Antiqua", 12))
        # self.label_return_book_title.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        # self.entry_return_book_title = tk.Entry(self.return_frame, width=40, font=("Book Antiqua", 12))
        # self.entry_return_book_title.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Return book button
        self.button_return_book = tk.Button(self.return_frame, text="Return Book", command=self.return_book,
                                            font=("Book Antiqua", 12), bg="#008CBA", fg="white")
        self.button_return_book.grid(row=2, columnspan=2, pady=20)

    def return_book(self):
        book_id = self.return_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Book ID cannot be empty.")
            return

        try:
            # Check if the book exists
            self.cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id,))
            book = self.cursor.fetchone()
            if not book:
                messagebox.showerror("Error", "Book not found.")
                return

            if not book[6]:
                messagebox.showerror("Error", "Book is not borrowed.")
                return

            # Retrieve due date for the book
            self.cursor.execute('''SELECT due_date FROM booking_history WHERE book_id = ? AND return_date IS NULL''',
                                (book_id,))
            due_date_row = self.cursor.fetchone()
            if not due_date_row:
                messagebox.showerror("Error", "No record found for the given book ID.")
                return

            due_date_str = due_date_row[0]
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")

            # Calculate fine amount based on return date and due date
            fine_per_day = 10
            days_overdue = (datetime.now() - due_date).days
            if days_overdue > 0:
                total_fine = days_overdue * fine_per_day
                messagebox.showinfo("Fine", f"Total fine amount: Rs.{total_fine}")
                collected = messagebox.askyesno("Fine Collected",
                                                f"Is Total fine amount: Rs.{total_fine} Collected")
                if not collected:
                    messagebox.showinfo("Failure", f"Please collect the total fine amount: Rs.{total_fine}!")
                    return
            else:
                total_fine = 0


            # Update borrowing history with return date and total fine
            return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                '''UPDATE booking_history 
                   SET return_date = ?, total_fine_paid = ? 
                   WHERE book_id = ?  AND return_date IS NULL''',
                (return_date, total_fine, book_id))  # Assuming total_fine_paid is initially 0
            self.cursor.execute(
                '''UPDATE user_booking_history 
                   SET return_date = ?, total_fine_paid = ? 
                   WHERE book_id = ? AND return_date IS NULL''',
                (return_date, total_fine, book_id))
            self.conn.commit()

            # Update book status to available
            self.cursor.execute('''UPDATE books SET is_borrowed = ? WHERE id = ?''', (0, book_id))
            self.conn.commit()

            messagebox.showinfo("Success", "Book returned successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Clear entry field
        self.return_id_entry.delete(0, tk.END)

    def setup_display_books_tab(self):
        # Frame to hold displayed books
        self.display_frame = tk.Frame(self.tab_display_books, bg="#f0f0f0")
        self.display_frame.pack(fill="both", expand=True)

        # Display button
        display_button = ttk.Button(self.display_frame, text="Display Books", command=self.display_books)
        display_button.pack(pady=5)

        # Display books treeview
        self.treeview_display_books = ttk.Treeview(self.display_frame, columns=("ID", "Title", "Author", "Status"),
                                                   show="headings", style="Custom.Treeview")
        self.treeview_display_books.heading("ID", text="ID", anchor="w")  # Align left
        self.treeview_display_books.heading("Title", text="Title", anchor="w")  # Align left
        self.treeview_display_books.heading("Author", text="Author", anchor="w")  # Align left
        self.treeview_display_books.heading("Status", text="Status", anchor="w")  # Align left
        self.treeview_display_books.pack(padx=10, pady=(5, 0), fill="both", expand=True)

        # Configure style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Book Antiqua", 12))
        style.configure("Custom.Treeview.Heading", font=("Book Antiqua", 12, "bold"))

        style.configure("Treeview", background="#f0f0f0", foreground="black", fieldbackground="#f0f0f0")
        style.map("Treeview", background=[("selected", "#0078d4")])

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.treeview_display_books.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview_display_books.configure(yscrollcommand=scrollbar.set)

    def display_books(self):
        # Clear existing data
        for item in self.treeview_display_books.get_children():
            self.treeview_display_books.delete(item)

        # Connect to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Fetch data from the 'books' table
        cursor.execute("SELECT id, title, author, is_borrowed FROM books")
        books = cursor.fetchall()

        # Insert data into treeview
        if not books:
            self.treeview_display_books.insert("", "end", values=("No books available.", "", "", ""))
        else:
            for book in books:
                status = "Available" if not book[3] else "Borrowed"
                self.treeview_display_books.insert("", "end", values=(book[0], book[1], book[2], status))

        # Close the cursor and connection
        cursor.close()
        conn.close()

    def setup_delete_books_tab(self):
        # Frame to hold displayed books
        self.delete_frame = tk.Frame(self.tab_delete_book, bg="#f0f0f0")
        self.delete_frame.pack(fill="both", expand=True)
        delete_label = ttk.Label(self.delete_frame, text="Book ID:")
        delete_label.grid(row=0, column=0, padx=5, pady=5)
        self.delete_id_entry = ttk.Entry(self.delete_frame, width=30)
        self.delete_id_entry.grid(row=0, column=1, padx=5, pady=5)

        delete_button = ttk.Button(self.delete_frame, text="Delete", command=self.delete_book)
        delete_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def delete_book(self):
        book_id = self.delete_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Book ID cannot be empty.")
            return

        self.cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id,))
        book = self.cursor.fetchone()
        if book:
            if book[6]:  # Check if the book is borrowed
                messagebox.showerror("Error", "Cannot delete a borrowed book.")
                return
            self.cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", f"Book '{book[1]}' deleted successfully!")
            self.delete_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Book not found.")

    def setup_search_books_tab(self):
        self.search_frame = ttk.Frame(self.tab_search_books, padding=(10, 10, 10, 0))
        self.search_frame.pack(fill="both", expand=True)

        # Create labels and entry widgets
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

        # Create treeview widget
        self.tree = ttk.Treeview(self.search_frame, columns=("ID", "Title", "Author", "Status"), show="headings")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Add column headings
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Title", text="Title", anchor="w")
        self.tree.heading("Author", text="Author", anchor="w")
        self.tree.heading("Status", text="Status", anchor="w")

        # Set font for all columns
        self.tree.tag_configure("TreeviewFont", font=("Book Antiqua", 10))
        for col in ("ID", "Title", "Author", "Status"):
            self.tree.tag_configure(col, font=("Book Antiqua", 10))

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=4, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

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

        # Clear existing treeview items
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not books:
            messagebox.showinfo("Info", "No books found.")
        else:
            for book in books:
                status = "Available" if not book[6] else "Borrowed"
                self.tree.insert('', 'end', values=(book[0], book[1], book[2], status))

    def setup_booking_history_tab(self):
        self.history_frame = tk.Frame(self.tab_booking_history, bg="#f0f0f0")
        self.history_frame.pack(fill="both", expand=True)

        # Adjust row and column configuration
        self.history_frame.grid_rowconfigure(2, weight=0)
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(1, weight=0)
        self.history_frame.grid_columnconfigure(2, weight=0)

        # Dropdown menu for selecting search option
        self.search_option_label = ttk.Label(self.history_frame, text="Search by:", font=("Book Antiqua", 12))
        self.search_option_label.grid(row=0, column=0, padx=(5, 2), pady=5, sticky="e")

        self.search_option_var = tk.StringVar()
        self.search_option_dropdown = ttk.Combobox(self.history_frame, textvariable=self.search_option_var,
                                                   values=["Book ID", "User ID", "Date (YYYY-MM-DD)"])
        self.search_option_dropdown.grid(row=0, column=1, padx=(2, 5), pady=5, sticky="ew")

        search_history_button = ttk.Button(self.history_frame, text="Search", command=self.search_booking_history)
        search_history_button.grid(row=0, rowspan=2, column=2, padx=5, pady=5, sticky="w")

        self.history_result_label = ttk.Label(self.history_frame, text="Booking History:")
        self.history_result_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Input field for search query
        self.search_query_label = ttk.Label(self.history_frame, text="Search Query:", font=("Book Antiqua", 12))
        self.search_query_label.grid(row=1, column=0, padx=(5, 2), pady=5, sticky="e")

        self.search_query_text = ttk.Entry(self.history_frame, width=30)
        self.search_query_text.grid(row=1, column=1, padx=(2, 5), pady=5, sticky="ew")


        # Increase size of the Treeview area
        self.history_result_treeview = ttk.Treeview(self.history_frame,
                                                    columns=("Book ID", "Borrowed Date", "Return Date"),
                                                    show="headings", style="Custom.Treeview")
        self.history_result_treeview.heading("Book ID", text="Book ID", anchor="w")
        self.history_result_treeview.heading("Borrowed Date", text="Borrowed Date", anchor="w")
        self.history_result_treeview.heading("Return Date", text="Return Date", anchor="w")
        self.history_result_treeview.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Configure style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Book Antiqua", 12))
        style.configure("Custom.Treeview.Heading", font=("Book Antiqua", 12, "bold"))

        style.configure("Treeview", background="#f0f0f0", foreground="black", fieldbackground="#f0f0f0")
        style.map("Treeview", background=[("selected", "#0078d4")])

    def search_booking_history(self):
        search_option = self.search_option_dropdown.get()  # Retrieve selected option from dropdown
        search_query = self.search_query_text.get().strip()

        if not search_query:
            messagebox.showerror("Error", "Please enter a search query.")
            return

        try:
            if search_option == "Date (YYYY-MM-DD)":
                search_date = datetime.strptime(search_query, "%Y-%m-%d").date()
                next_date = search_date + timedelta(days=1)

                columns = ("Search_Date","Total No of books Issued", "Total No of books returned", "Total fine collected")
                self.cursor.execute('''SELECT
                                          ? AS Search_Date,
                                          COUNT(*) AS Total_Books_Issued,
                                          SUM(CASE WHEN return_date IS NOT NULL THEN 1 ELSE 0 END) AS Total_Books_Returned,
                                          IFNULL(SUM(total_fine_paid), 0.0) AS Total_Fine_Collected
                                      FROM booking_history
                                      WHERE borrowed_date >= ? AND borrowed_date < ?''',
                                    (search_date, search_date, next_date))

            elif search_option == "Book ID":
                columns = ("User ID", "Book ID", "Issued Date", "Due Date", "Returned Date")
                book_id = int(search_query)
                self.cursor.execute('''SELECT user_id, book_id, issued_date, due_date, return_date 
                                       FROM booking_history WHERE book_id = ?''', (book_id,))
            elif search_option == "User ID":
                columns = (
                "User ID", "Book ID", "Borrowed Date", "Due Date", "Returned Date", "Total Fine Due", "Total Fine Paid")
                user_id = int(search_query)
                self.cursor.execute('''SELECT user_id, book_id, borrowed_date, due_date, return_date, 
                                              total_fine_due, total_fine_paid 
                                       FROM booking_history WHERE user_id = ?''', (user_id,))
            else:
                raise ValueError("Invalid search option selected.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        history = self.cursor.fetchall()

        # Debug statements
        print("Search Option:", search_option)
        print("Columns:", columns)
        print("Retrieved Data:", history)

        # Clear the existing columns and set new columns
        self.history_result_treeview["columns"] = columns

        # Clear the existing contents of the Treeview
        for item in self.history_result_treeview.get_children():
            self.history_result_treeview.delete(item)

        # Set headings for the new columns
        for column_heading in columns:
            self.history_result_treeview.heading(column_heading, text=column_heading, anchor="w")

        # Insert data into the Treeview
        for entry in history:
            self.history_result_treeview.insert("", "end", values=entry)

    def logout(self):
        self.destroy()
        main_login.LoginPage().show_admin_login()

    def exit_application(self):
        self.cursor.close()  # Close the cursor
        self.conn.close()  # Close the connection
        self.master.destroy()