from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'

db = SQLAlchemy(app)
app.app_context().push()
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    investment_amount = db.Column(db.Float, default=0)

    def __repr__(self):
        return f'<Company {self.name}>'

@app.route('/')
def index():
    companies = Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/company/<int:id>')
def company(id):
    company = Company.query.get(id)
    return render_template('company.html', company=company)

@app.route('/invest', methods=['POST'])
def invest():
    company_id = request.form['company_id']
    amount = request.form['amount']
    company = Company.query.get(company_id)
    company.investment_amount += float(amount)
    db.session.commit()
    session['investments'] = session.get('investments', []) + [(company_id, amount)]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
