import requests
from flask import Flask, render_template, flash, request, redirect

app = Flask(__name__)
app.secret_key = 'some_secret'
base_url = 'http://127.0.0.1:5000/users'


@app.route('/')
def hello_world():  # put application's code here
    response = requests.get(base_url)

    if response.status_code == 200:
        users = response.json()
        return render_template('user.html', users=users)
    else:
        flash('Something went wrong')
    return render_template('user.html')


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']

        if all([username, user_email, user_password]):
            response = requests.post(base_url, json={'name': username, 'email': user_email, 'password': user_password})

            if response.status_code == 200:
                flash('User added successfully')
                return redirect('/')
            else:
                # Display an error message
                flash('Something went wrong. Please try again later.')
                return render_template('add.html')
        else:
            flash('User name, email and password are required. ')
            return render_template('add.html')
    else:
        return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        username = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']

        if all([username, user_email, user_password]):
            response = requests.put(f'{base_url}/{id}',
                                    json={'username': username, 'email': user_email, 'password': user_password})

            if response.status_code == 200:
                flash(f'User {id} updated successfully')
                return redirect('/')
            else:
                # Display an error message
                flash('Something went wrong. Please try again later.')
                return render_template('edit.html')
        else:
            flash('User name, email and password are required. ')
            return render_template('edit.html')
    else:
        # Send a GET request to the web api to get the user by id
        response = requests.get(f'{base_url}/{id}')
        # Check if the response is successful
        if response.status_code == 200:
            # Parse the response as a JSON object
            user = response.json()
            # Render the edit.html template with the user data
            return render_template('edit.html', user=user)
        else:
            # Display an error message
            flash('User not found.')
            return render_template('edit.html')


@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    if request.method == 'POST':
        response = requests.delete(f'{base_url}/{id}')
        if response.status_code == 200:
            # Display an error message
            flash('Something went wrong. Please try again later.')
            return render_template('edit.html')
        else:
            flash('User name, email and password are required. ')
            return render_template('edit.html')
    else:
        # Send a GET request to the web api to get the user by id
        response = requests.get(f'{base_url}/{id}')
        # Check if the response is successful
        if response.status_code == 200:
            # Parse the response as a JSON object
            user = response.json()
            # Render the edit.html template with the user data
            return render_template('edit.html', user=user)
        else:
            # Display an error message
            flash('User not found.')
            return render_template('edit.html')


if __name__ == '__main__':
    app.run()
