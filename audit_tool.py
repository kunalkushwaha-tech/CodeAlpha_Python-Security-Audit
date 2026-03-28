import sqlite3
import os

# 1. Hardcoded Secret (Security Vulnerability)
# Hardcoding sensitive information like API keys or passwords is a severe security risk.
API_KEY = "12345-ABCDE-SUPER-SECRET-KEY"

def get_user_data(username):
    """
    Retrieves user data from the database based on the provided username.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 2. SQL Injection (Security Vulnerability)
    # Directly concatenating user input into a SQL query makes the application vulnerable to SQL Injection.
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def ping_host(ip_address):
    """
    Pings a specified network device to check its availability.
    """
    # 3. Command Injection (Security Vulnerability)
    # Passing unsanitized user input directly to the OS shell creates a Command Injection vulnerability.
    command = f"ping -c 1 {ip_address}"
    print(f"Executing: {command}")
    os.system(command)

if __name__ == "__main__":
    print("--- User Search ---")
    user_input = input("Enter username to search: ")
    print("Result:", get_user_data(user_input))
    
    print("\n--- Network Ping ---")
    ip_input = input("Enter IP to ping: ")
    ping_host(ip_input)
