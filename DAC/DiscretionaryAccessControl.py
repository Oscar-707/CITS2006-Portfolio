import sqlite3

class AccessControl:
    def __init__(self):
        # Access control structure: {resource: {user: [permissions]}}
        self.users = {}

    def add_resource(self, resource):
        if resource not in self.users:
            self.users[resource] = {}

    def add_user_to_users(self, admin, resource, user, permissions):
        if not self.is_admin(admin):
            print("Permission denied: Only admins can modify access control.")
            return False

        if resource not in self.users:
            print(f"Resource '{resource}' does not exist.")
            return False

        self.users[resource][user] = permissions
        print(f"User '{user}' added to resource '{resource}' with permissions {permissions}.")
        return True

    def remove_user_from_users(self, admin, resource, user):
        if not self.is_admin(admin):
            print("Permission denied: Only admins can modify access control.")
            return False

        if resource in self.users and user in self.users[resource]:
            del self.users[resource][user]
            print(f"User '{user}' removed from resource '{resource}'.")
            return True

        print(f"User '{user}' not found in resource '{resource}'.")
        return False

    def check_access(self, user, resource, permission):
        if resource in self.users and user in self.users[resource]:
            return permission in self.users[resource][user]
        return False

    def is_admin(self, user):
        return user == "admin"

    def read_database(self, user, resource):
        if self.check_access(user, resource, "read"):
            try:
                conn = sqlite3.connect("test.db")
                cursor = conn.cursor()
                print(f"\nUser '{user}' is reading data from 'important_information':")
                cursor.execute("SELECT * FROM important_information;")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                conn.close()
            except Exception as e:
                print(f"Error reading database: {e}")
        else:
            print(f"Access denied: User '{user}' does not have read permission on '{resource}'.")

    def write_to_database(self, user, resource, staff_id, full_name, position):
        if self.check_access(user, resource, "write"):
            try:
                conn = sqlite3.connect("test.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO important_information (staff_id, full_name, position)
                    VALUES (?, ?, ?);
                """, (staff_id, full_name, position))
                conn.commit()
                conn.close()
                print(f"User '{user}' successfully wrote to the database.")
            except sqlite3.IntegrityError:
                print(f"Write failed: Staff ID {staff_id} already exists.")
            except Exception as e:
                print(f"Error writing to database: {e}")
        else:
            print(f"Access denied: User '{user}' does not have write permission on '{resource}'.")


def create_staff_table_and_insert_data():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS important_information (
            staff_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            position TEXT NOT NULL
        );
    """)

    # Insert 3 example rows if table is empty
    cursor.execute("SELECT COUNT(*) FROM important_information;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO important_information (staff_id, full_name, position)
            VALUES (?, ?, ?);
        """, [
            (1, "Alice Johnson", "Manager"),
            (2, "Bob Smith", "Security Analyst"),
            (3, "Charlie Lee", "Systems Administrator")
        ])
        print("Inserted 3 example rows into 'important_information'.")
    else:
        print("Table already has data. Skipping insert.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Setup database and table
    create_staff_table_and_insert_data()

    # Setup access control
    users = AccessControl()
    users.add_resource("database_1")
    users.add_user_to_users("admin", "database_1", "admin", ["read", "write"])
    users.add_user_to_users("admin", "database_1", "user1", ["write"])
    users.add_user_to_users("admin", "database_1", "user2", ["read"])

    # Read access tests, change the database row test data in order to avoid adding duplicate fields

    # Admin has read and write privelages so they can read and write
    print("\n-- Admin Reading --")
    users.read_database("admin", "database_1")

    # User1 only has write access but no read access
    print("\n-- User1 Attempting Read (Should Fail) --")
    users.read_database("user1", "database_1")

    # User2 has read access but no write access
    print("\n-- User2 Reading (Should Succeed) --")
    users.read_database("user2", "database_1")

    # Write access tests
    print("\n-- User1 Writing (Should Succeed) --")
    users.write_to_database("user1", "database_1", 8, "Om Patel", "Intern")

    print("\n-- User2 Writing (Should Fail) --")
    users.write_to_database("user2", "database_1", 5, "Eva Brown", "Consultant")

    print("\n-- Admin Writing (Should Succeed) --")
    users.write_to_database("admin", "database_1", 10, "Dev Patel", "Director")

    # Final read to verify insertions
    print("\n-- Final Admin Read --")
    users.read_database("admin", "database_1")
