from flask import Flask, render_template, request, redirect,flash,session,url_for,jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
from flask_session import Session
from flask_migrate import Migrate
import mysql.connector
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file  = "sqlite:///{}".format(os.path.join(project_dir, "esd.grp 13.db"))

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'redsfsfsfsfis'

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
migrate = Migrate()

class Expense(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    expenseName = db.Column(db.String(40), nullable=False)
    expenseDate = db.Column(db.String(40), nullable=False)
    expenseAmount = db.Column(db.Integer, nullable=False)
    expenseCategory = db.Column(db.String(40), nullable=False)
    expenseMethod = db.Column(db.String(40), nullable=False)
    
# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()

@app.route('/')
def homePage():
    return render_template('displayExpenses.html')


# Add expenses view
@app.route('/add')
def add():
    return render_template('add.html')

# Display expenses view
@app.route('/displayExpenses')
def displayExpenses():
    expenses = Expense.query.all()
    sum = 0
    sum_food = 0
    sum_entertainment = 0
    sum_groceries = 0
    sum_sports = 0
    sum_medicine = 0
    sum_trip = 0
    sum_other = 0
    
    for expense in expenses:
        sum += expense.expenseAmount
        
        if expense.expenseCategory == 'food':
            sum_food += expense.expenseAmount
        elif expense.expenseCategory == 'entertainment':
            sum_entertainment += expense.expenseAmount
        elif expense.expenseCategory == 'groceries':
            sum_groceries += expense.expenseAmount
        elif expense.expenseCategory == 'sports':
            sum_sports += expense.expenseAmount
        elif expense.expenseCategory == 'medicine':
            sum_medicine += expense.expenseAmount
        elif expense.expenseCategory == 'trip':
            sum_trip += expense.expenseAmount
        else:
            sum_other += expense.expenseAmount
    
    return render_template('displayExpenses.html', 
                           expenses=expenses, 
                           sum=sum, 
                           sum_food=sum_food,
                           sum_entertainment=sum_entertainment, 
                           sum_groceries=sum_groceries, 
                           sum_sports=sum_sports, 
                           sum_medicine=sum_medicine, 
                           sum_trip=sum_trip, 
                           sum_other=sum_other)

@app.route('/deleteExpense/<int:id>',methods=['DELETE', 'GET'])
def deleteExpense(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/displayExpenses')


@app.route('/updateExpense/<int:id>')
def updateExpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('updateExpense.html', expense = expense)

@app.route('/editExpense', methods=['POST'])
def editExpense():
    id = request.form['id']
    name = request.form['name']
    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']
    method=request.form['method']
    db.session.query(Expense).filter_by(id=id).update({"expenseName":name, "expenseDate":date, "expenseAmount":amount, "expenseCategory":category,"expenseMethod":method})
    
    db.session.commit()
    return redirect('/displayExpenses')

@app.route('/addExpense', methods=['GET', 'POST'])
def addExpense():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        method=request.form['method']
        expense = Expense(expenseName=name,expenseDate=date, expenseAmount=amount, expenseCategory=category,expenseMethod=method)
        db.session.add(expense)
        db.session.commit()
        return redirect('/displayExpenses')
    else:
        return render_template('addExpense.html')

if __name__ == '__main__':
    app.run(debug=True)
    