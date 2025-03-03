import sqlite3


def create_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Execute the SQL command to create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL,
                branch TEXT NOT NULL,
                user_type TEXT NOT NULL
                )""")

    # Create admins table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                    )''')

    # Check if admin user exists in the table
    cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
    result = cursor.fetchone()

    # If admin user doesn't exist, insert it
    if result[0] == 0:
        cursor.execute("INSERT INTO admins (username, password) VALUES ('admin', 'admin')")
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")


    # Create books table if not exists

    cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           title TEXT NOT NULL, 
                           author TEXT NOT NULL, 
                           category_id INTEGER,
                           genre_id INTEGER,
                           book_added_date DATE,
                           is_borrowed INTEGER
                           )''')

    # Create the user_booking_history table
    create_user_booking_history_sql = '''
        CREATE TABLE IF NOT EXISTS user_booking_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        Title Text,
        Author Text,
        borrowed_date DATE,
        due_date DATE,
        return_date DATE,
        total_fine_due REAL,
        total_fine_paid REAL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    '''
    cursor.execute(create_user_booking_history_sql)

    # Create the trigger for user_booking_history
    create_user_booking_history_trigger_sql = '''
    -- Trigger for AFTER INSERT
        CREATE TRIGGER IF NOT EXISTS calculate_user_booking_fine_due_insert
    AFTER INSERT ON user_booking_history
    FOR EACH ROW
    BEGIN
        UPDATE user_booking_history 
        SET total_fine_due = CASE
                        WHEN NEW.due_date > CURRENT_TIMESTAMP  -- Check if new due_date is greater than current date
                            THEN 0  -- Set total_fine_due to 0 if new due_date is greater than current date
                        ELSE
                            ROUND(julianday('now') - julianday(NEW.due_date)) * 10  -- Calculate total_fine_due
                     END
        WHERE id = NEW.id;
    END;
    
    -- Trigger for AFTER UPDATE
    CREATE TRIGGER IF NOT EXISTS calculate_user_booking_fine_due_update
    AFTER UPDATE ON user_booking_history
    FOR EACH ROW
    BEGIN
        UPDATE user_booking_history 
        SET total_fine_due = CASE
                        WHEN NEW.due_date > CURRENT_TIMESTAMP  -- Check if new due_date is greater than current date
                            THEN 0  -- Set total_fine_due to 0 if new due_date is greater than current date
                        ELSE
                            ROUND(julianday('now') - julianday(NEW.due_date)) * 10  -- Calculate total_fine_due
                     END
        WHERE id = NEW.id;
    END;

    '''
    cursor.executescript(create_user_booking_history_trigger_sql)

    # Create the booking_history table
    create_booking_history_sql = '''
    CREATE TABLE IF NOT EXISTS booking_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        issued_date DATE,
        borrowed_Date DATE,
        due_date DATE,
        return_date DATE,
        total_fine_due REAL,
        total_fine_paid REAL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    '''
    cursor.execute(create_booking_history_sql)

    # Create the trigger for booking_history
    create_booking_history_trigger_sql = '''
            -- Trigger for AFTER INSERT
    CREATE TRIGGER IF NOT EXISTS calculate_booking_fine_due_insert
    AFTER INSERT ON booking_history
    FOR EACH ROW
    BEGIN
        UPDATE booking_history 
        SET total_fine_due = CASE
                        WHEN NEW.due_date > CURRENT_TIMESTAMP  -- Check if new due_date is greater than current date
                            THEN 0  -- Set total_fine_due to 0 if new due_date is greater than current date
                        ELSE
                            ROUND(julianday('now') - julianday(NEW.due_date)) * 10  -- Calculate total_fine_due
                     END
        WHERE id = NEW.id;
    END;
    
    -- Trigger for AFTER UPDATE
    CREATE TRIGGER IF NOT EXISTS calculate_booking_fine_due_update
    AFTER UPDATE ON booking_history
    FOR EACH ROW
    BEGIN
        UPDATE booking_history 
        SET total_fine_due = CASE
                        WHEN NEW.due_date > CURRENT_TIMESTAMP  -- Check if new due_date is greater than current date
                            THEN 0  -- Set total_fine_due to 0 if new due_date is greater than current date
                        ELSE
                            ROUND(julianday('now') - julianday(NEW.due_date)) * 10  -- Calculate total_fine_due
                     END
        WHERE id = NEW.id;
    END;
      
    '''
    cursor.executescript(create_booking_history_trigger_sql)

    conn.commit()
    conn.close()
