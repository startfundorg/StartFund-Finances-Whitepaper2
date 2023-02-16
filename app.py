from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    investment_amount = db.Column(db.Float, default=0)


companies = [
    Company(name='Company A', description='Description A', investment_amount=500),
    Company(name='Company B', description='Description B', investment_amount=1000),
    Company(name='Company C', description='Description C', investment_amount=2000),
]


@app.route('/')
def index():
    return render_template('index.html', companies=companies)


@app.route('/company/<int:company_id>', methods=['GET', 'POST'])
def company(company_id):
    company = next((c for c in companies if c.id == company_id), None)
    if company is None:
        return 'Company not found'
    if request.method == 'POST':
        amount = float(request.form['amount'])
        company.investment_amount += amount
        session.setdefault('investments', []).append((str(company.id), amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return 'Investment successful'
    return render_template('company.html', company=company)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
