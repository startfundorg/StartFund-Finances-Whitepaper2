from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
app.app_context().push()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    location = db.Column(db.String(50))
    building = db.Column(db.String(50))

db.create_all()

company1 = Company(name='Company A', description='A description of Company A', location='New York', building='Building 1')
company2 = Company(name='Company B', description='A description of Company B', location='London', building='Building 2')
company3 = Company(name='Company C', description='A description of Company C', location='Tokyo', building='Building 3')
companies = [company1, company2, company3]
db.session.add(company1)
db.session.add(company2)
db.session.add(company3)
db.session.commit()

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

@app.route('/company-details/<int:company_id>')
def company_details(company_id):
    company = Company.query.get(company_id)
    if company is None:
        return jsonify({'error': 'Company not found'})

    data = {
        'id': company.id,
        'name': company.name,
        'description': company.description,
        'funding_goal': company.funding_goal,
        'funding_raised': company.funding_raised,
        'investors': [
            {
                'name': investor.name,
                'invested_amount': investment.amount,
            }
            for investment in company.investments
            for investor in investment.investors
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
