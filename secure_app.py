import sqlite3
import os
import subprocess
import re

# 1. FIXED: Hardcoded Secret
# Use environment variables to safely load sensitive information instead of hardcoding them.
API_KEY = os.environ.get("API_KEY", "default-safe-key-if-not-set")

def get_user_data(username):
    """
    Retrieves user data from the database based on the provided username safely.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 2. FIXED: SQL Injection
    # Using parameterized queries (?) ensures user input is treated as data, not as an executable SQL command.
    query = "SELECT * FROM users WHERE username = ?"
    
    try:
        # Pass the user input as a tuple in the second argument
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        # Better security practice: Log the error internally, but don't show exact DB errors to the user.
        print(f"Internal Database Error: {e}")
        return "An error occurred while fetching user data."
    finally:
        conn.close()

def ping_host(ip_address):
    """
    Pings a specified network device safely to check its availability.
    """
    # 3. FIXED: Command Injection
    # First, validate the input to ensure it only contains allowed characters (alphanumeric, dots, hyphens).
    if not re.match(r"^[a-zA-Z0-9.\-]+$", ip_address):
        print("Invalid IP address or hostname format. Please try again.")
        return

    # Second, use subprocess.run with a list of arguments instead of a single string.
    # This prevents the OS shell from interpreting special characters like ';' or '&&'.
    command = ["ping", "-c", "1", ip_address]
    print(f"Executing: {' '.join(command)}")
    
    try:
        # capture_output=True grabs the terminal output, text=True makes it a string
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Ping successful!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Ping failed.")
        print(e.stderr)
    except FileNotFoundError:
        print("Ping utility is not installed or available on this system path.")

if __name__ == "__main__":
    print("--- User Search ---")
    user_input = input("Enter username to search: ")
    print("Result:", get_user_data(user_input))
    
    print("\n--- Network Ping ---")
    ip_input = input("Enter IP to ping: ")
    ping_host(ip_input)
