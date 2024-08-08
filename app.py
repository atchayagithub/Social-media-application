from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import pickle, os

app = Flask(__name__)
app.secret_key = '1234'

#User data file

USER_DATA_FILE = 'user_data.pkl'

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'wb') as file:
        pickle.dump([], file)

def load_user_data():
    try:
        with open(USER_DATA_FILE, 'rb') as file:
            return pickle.load(file)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as file:
        pickle.dump(user_data, file)

#Usernames file 
        
USERNAME_FILE = 'usernames.pkl'

if not os.path.exists(USERNAME_FILE):
    with open(USERNAME_FILE, 'wb') as file:
        pickle.dump([], file)

def load_username_file():
    try:
        with open(USERNAME_FILE, 'rb') as file:
            return pickle.load(file)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_username_file(user_data):
    with open(USERNAME_FILE, 'wb') as file:
        pickle.dump(user_data, file) 

@app.route("/")
def index():
    return render_template('first.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user_data = load_user_data()

        for data in user_data:
            if isinstance(data, dict) and (data.get('user_email') == user_email) and (data.get('user_password') == user_password):
                return redirect(url_for('my_feed'))
            
        flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']
        user_data = {'user_name': user_name, 'user_email': user_email, 'user_password': user_password}
        
        data = load_user_data()
        data.append(user_data)
        save_user_data(data)
        return redirect(url_for('create_account'))

    return render_template('signup.html')

@app.route("/home_page")
def home_page():
    return render_template('home_page.html')

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        id_name = request.form['name']
        id_uname = request.form['uname']
        id_phone = request.form['phnno']
        id_email = request.form['email']
        id_age = request.form['age']
        id_gender = request.form['gender']

        if not all([id_name, id_uname, id_phone, id_email, id_age, id_gender]):
            flash('Please fill in all the required fields.', 'error')
            return render_template('create_account.html')

        data = load_username_file()
        if any(username_data['username'] == id_uname for username_data in data):
            flash('Username already taken. Try another username.', 'error')
            return render_template('create_account.html')

        id_uname_data = {'username': id_uname}
        data.append(id_uname_data)
        save_username_file(data)

        user_data = load_user_data()
        user_details = {
            'name': id_name,
            'username': id_uname,
            'phone': id_phone,
            'email': id_email,
            'age': id_age,
            'gender': id_gender,
        }
        user_data.append(user_details)
        save_user_data(user_data)

        session['name'] = id_name
        session['username'] = id_uname
        session['user_details'] = user_details

        return redirect(url_for('my_feed'))

    return render_template('create_account.html')

@app.route('/check_username_availability/<username>')
def check_username_availability(username):
    data = load_username_file()
    if any(username_data['username'] == username for username_data in data):
        return jsonify({'available': False})
    else:
        return jsonify({'available': True})
       
@app.route("/my_feed",methods=['GET', 'POST'])
def my_feed():
    return render_template('my_feed.html')

@app.route("/my_profile",methods=['GET', 'POST'])
def my_profile():
    username = session.get('username')
    name = session.get('name')
    return render_template('my_profile.html', username=username, name=name)

@app.route("/social",methods=['GET', 'POST'])
def social():
    user_data = load_user_data() 
    return render_template('social.html', user_data=user_data)

@app.route("/add_post",methods=['GET', 'POST'])
def add_post():
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run(debug=True)