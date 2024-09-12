from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector as mysql

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pavan%4012@localhost/registration'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a random secret key for session management

db = SQLAlchemy(app)
db_config={
    'user': 'root',
    'password': 'Pavan%4012',
    'host': 'localhost',
    'database': 'registration' 
}

# Define the Candidate model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Add an ID column as a primary key
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Route for the home page
@app.route('/')
def home():
    return render_template('welcome.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Check if the email already exists
        existing_candidate = Candidate.query.filter_by(email=email).first()
        if existing_candidate:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))
        
        # Create a new candidate record
        new_candidate = Candidate(name=name, email=email)
        db.session.add(new_candidate)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html')
@app.route('/data')
def data():
    candidates = Candidate.query.all()  # Use SQLAlchemy to get all candidates
    return render_template('data.html', candidates=candidates)

    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)