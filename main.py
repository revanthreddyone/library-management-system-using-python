import database
import main_login
import welcome
if __name__ == "__main__":
    database.create_database()  # Create database and necessary tables
    welcome_page = welcome.WelcomePage()
    welcome_page.mainloop()
    