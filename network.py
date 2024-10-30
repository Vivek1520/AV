# import streamlit as st
# import sqlite3
# from cryptography.fernet import Fernet
# import os
#
# # Connect to SQLite database
# conn = sqlite3.connect('file_transfer.db')
# c = conn.cursor()
#
# # Create users table if it doesn't exist
# c.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY,
#     username TEXT UNIQUE,
#     password TEXT
# )
# ''')
#
# # Create files table if it doesn't exist
# c.execute('''
# CREATE TABLE IF NOT EXISTS files (
#     id INTEGER PRIMARY KEY,
#     filename TEXT,
#     recipient TEXT,
#     filepath TEXT
# )
# ''')
# conn.commit()
#
# # Function to generate a key for encryption
# def generate_key():
#     return Fernet.generate_key()
#
# # Function to encrypt the file
# def encrypt_file(file_path, key):
#     fernet = Fernet(key)
#     with open(file_path, 'rb') as file:
#         original = file.read()
#     encrypted = fernet.encrypt(original)
#
#     # Save the encrypted file
#     encrypted_file_path = file_path + '.enc'
#     with open(encrypted_file_path, 'wb') as encrypted_file:
#         encrypted_file.write(encrypted)
#     return encrypted_file_path
#
# # Function to register a user
# def register_user(username, password):
#     try:
#         c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
#
# # Function to authenticate a user
# def authenticate_user(username, password):
#     c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
#     return c.fetchone()
#
# # Streamlit user interface
# st.title("Secure File Transfer Application")
#
# # User authentication
# if 'user' not in st.session_state:
#     st.header("User Registration / Login")
#     option = st.selectbox("Select an option", ("Register", "Login"))
#
#     if option == "Register":
#         username = st.text_input("Username")
#         password = st.text_input("Password", type='password')
#         if st.button("Register"):
#             if register_user(username, password):
#                 st.success("User registered successfully!")
#             else:
#                 st.error("Username already exists!")
#
#     elif option == "Login":
#         username = st.text_input("Username")
#         password = st.text_input("Password", type='password')
#         if st.button("Login"):
#             user = authenticate_user(username, password)
#             if user:
#                 st.session_state.user = user[1]  # Save the username
#                 st.success("Logged in successfully!")
#             else:
#                 st.error("Invalid credentials!")
#
# # User dashboard after login
# if 'user' in st.session_state:
#     st.header(f"Welcome, {st.session_state.user}!")
#
#     # Generate a key
#     if st.button("Generate Encryption Key"):
#         key = generate_key()
#         st.session_state.key = key
#         st.success("Encryption key generated!")
#         st.write("Your encryption key is: **{}**".format(key.decode()))
#
#     # Ensure uploads directory exists
#     uploads_dir = "uploads"
#     if not os.path.exists(uploads_dir):
#         os.makedirs(uploads_dir)
#
#     # Upload file
#     uploaded_file = st.file_uploader("Choose a file to encrypt and send", type=['txt', 'pdf', 'jpg', 'png'])
#
#     # Select recipient
#     recipient = st.text_input("Recipient's username")
#
#     # Encrypt and send the file
#     if uploaded_file is not None and 'key' in st.session_state:
#         if st.button("Encrypt and Send"):
#             file_path = os.path.join(uploads_dir, uploaded_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#
#             encrypted_file_path = encrypt_file(file_path, st.session_state.key)
#             # Save file info to the database
#             c.execute("INSERT INTO files (filename, recipient, filepath) VALUES (?, ?, ?)",
#                       (uploaded_file.name, recipient, encrypted_file_path))
#             conn.commit()
#
#             st.success(f"File encrypted and sent to {recipient} successfully!")
#
#     # List files sent to the current user
#     st.header("Files Sent to You")
#     c.execute("SELECT id, filename, filepath FROM files WHERE recipient = ?", (st.session_state.user,))
#     files = c.fetchall()
#
#     if files:
#         for index, (file_id, filename, filepath) in enumerate(files):
#             st.write(filename)
#             # Use both the filename and index as a unique key
#             if st.button(f"Download {filename}", key=f"download_{file_id}_{index}"):
#                 with open(filepath, "rb") as f:
#                     st.download_button(
#                         label="Download Encrypted File",
#                         data=f,
#                         file_name=filename + '.enc',
#                         mime="application/octet-stream"
#                     )
#                 st.success(f"{filename} downloaded successfully!")
#     else:
#         st.write("No files sent to you.")

import streamlit as st
import sqlite3
from cryptography.fernet import Fernet
import os

# Connect to SQLite database
conn = sqlite3.connect('file_transfer.db')
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')

# Create files table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    recipient TEXT,
    filepath TEXT
)
''')
conn.commit()

# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to encrypt the file
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)

    # Save the encrypted file
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    return encrypted_file_path

# Function to decrypt the file
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)

    # Save the decrypted file
    decrypted_file_path = file_path.replace('.enc', '')  # Remove .enc extension
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    return decrypted_file_path

# Function to register a user
def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Function to authenticate a user
def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone()

# Streamlit user interface
st.title("Secure File Transfer Application")

# User authentication
if 'user' not in st.session_state:
    st.header("User Registration / Login")
    option = st.selectbox("Select an option", ("Register", "Login"))

    if option == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Register"):
            if register_user(username, password):
                st.success("User registered successfully!")
            else:
                st.error("Username already exists!")

    elif option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state.user = user[1]  # Save the username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials!")

# User dashboard after login
if 'user' in st.session_state:
    st.header(f"Welcome, {st.session_state.user}!")

    # Generate a key
    if 'key' not in st.session_state:
        if st.button("Generate Encryption Key"):
            key = generate_key()
            st.session_state.key = key
            st.success("Encryption key generated!")
            st.write("Your encryption key is: **{}**".format(key.decode()))

    # Ensure uploads directory exists
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    # Upload file
    uploaded_file = st.file_uploader("Choose a file to encrypt and send", type=['txt', 'pdf', 'jpg', 'png'])

    # Select recipient
    recipient = st.text_input("Recipient's username")

    # Encrypt and send the file
    if uploaded_file is not None and 'key' in st.session_state:
        if st.button("Encrypt and Send"):
            file_path = os.path.join(uploads_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            encrypted_file_path = encrypt_file(file_path, st.session_state.key)
            # Save file info to the database
            c.execute("INSERT INTO files (filename, recipient, filepath) VALUES (?, ?, ?)",
                      (uploaded_file.name, recipient, encrypted_file_path))
            conn.commit()

            st.success(f"File encrypted and sent to {recipient} successfully!")

    # List files sent to the current user
    st.header("Files Sent to You")
    c.execute("SELECT id, filename, filepath FROM files WHERE recipient = ?", (st.session_state.user,))
    files = c.fetchall()

    if files:
        for index, (file_id, filename, filepath) in enumerate(files):
            st.write(filename)

            # Button to download the original decrypted file
            if st.button(f"Download Original File {filename}", key=f"original_download_{file_id}_{index}"):
                if 'key' in st.session_state:
                    decrypted_file_path = decrypt_file(filepath, st.session_state.key)
                    with open(decrypted_file_path, "rb") as f:
                        st.download_button(
                            label="Download Original File",
                            data=f,
                            file_name=filename,
                            mime="application/octet-stream"
                        )
                    st.success(f"{filename} downloaded successfully!")
                else:
                    st.error("Encryption key not available.")

            # Button to download the encrypted file
            if st.button(f"Download Encrypted File {filename}", key=f"encrypted_download_{file_id}_{index}"):
                with open(filepath, "rb") as f:
                    st.download_button(
                        label="Download Encrypted File",
                        data=f,
                        file_name=filename + ".enc",
                        mime="application/octet-stream"
                    )
                st.success(f"{filename} (encrypted) downloaded successfully!")
