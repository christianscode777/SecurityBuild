from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Mail, Message
from flask_login import login_user, current_user, login_required, LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Setting up the database URI to point to the 'users.db' file in the 'instance' folder
db_path = os.path.join(app.instance_path, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)

app.config['SECURITY_PASSWORD_SALT'] = 'your_security_salt'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_2fa_verified = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('login.html')   

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Send verification email logic here
        return redirect(url_for('index'))
    return render_template('register.html')  # Assuming you have a register.html template

   

@app.route('/verify_email/<token>')
def verify_email(token):
    # verification using ItsDangerous
    pass

@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    if request.method == 'POST':
        user_code = request.form.get('code')
        if verify_2fa(current_user.id, user_code):
            current_user.is_2fa_verified = True
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            return render_template('verify.html', error='Invalid 2FA code.')
    return render_template('verify.html')

@app.route('/puzzle')
@login_required
def puzzle():
    # Serve puzzle after 2FA is successful
    return render_template('puzzle.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Authentication and 2FA verification check before serving dashboard
    return render_template('dashboard.html')


def verify_2fa(user_id, user_code):
    # Placeholder logic to verify 2FA code
    # In real application, we would compare user_code with a stored 2FA code or use a 2FA library
    return True  # or False if verification fails

if __name__ == '__main__':
    # Ensure the 'instance' folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    with app.app_context():
        db.create_all()
    app.run(debug=True)