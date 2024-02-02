from flask import Flask, render_template, request, redirect, url_for
import json
import hashlib

app = Flask(__name__)

# File to store user registration details in JSON format
USERS_FILE = 'users.txt'

def read_users_file():
    try:
        with open(USERS_FILE, 'r') as file:
            users_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users_data = {}
    return users_data

def write_to_users_file(users_data):
    with open(USERS_FILE, 'w') as file:
        json.dump(users_data, file, indent=2)

@app.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        md5_hash = hashlib.md5(password.encode())
        password = md5_hash.hexdigest()
        # Read existing user data
        users_data = read_users_file()

    
        users_data[email] = {'name': name, 'email': email, 'password': password}

        
        write_to_users_file(users_data)

        return f"Registration successful for {email}"

    # Render the registration form for GET requests
    return render_template('registration.html')

@app.route('/user/<user_id>')
def display_user(user_id):
    # Read existing user data
    users_data = read_users_file()

    # Check if the user ID exists
    if user_id in users_data:
        user_details = users_data[user_id]
        return render_template('user_details.html', user_details=user_details)
    else:
        return "User not found."

if __name__ == '__main__':
    app.run(debug=True)
