from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
db = SQLAlchemy(app)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(8), nullable=False)
    message = db.Column(db.Text, nullable=False)
    remind_type = db.Column(db.String(10), nullable=False)

# Create the application context
with app.app_context():
    # Create the database tables
    db.create_all()

# Route to create a reminder
@app.route('/create_reminder', methods=['POST'])
def create_reminder():
    data = request.get_json()

    date = data.get('date')
    time = data.get('time')
    message = data.get('message')
    remind_type = data.get('remind_type')

    if not all([date, time, message, remind_type]):
        return jsonify({'error': 'Incomplete data'}), 400

    try:
        new_reminder = Reminder(date=date, time=time, message=message, remind_type=remind_type)
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify({'message': 'Reminder created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
