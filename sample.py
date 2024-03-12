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

# Route to get all reminders
@app.route('/get_all_reminders', methods=['GET'])
def get_all_reminders():
    reminders = Reminder.query.all()
    reminders_list = [{'id': reminder.id, 'date': reminder.date, 'time': reminder.time, 'message': reminder.message, 'remind_type': reminder.remind_type} for reminder in reminders]
    return jsonify({'reminders': reminders_list})

# Route to get a specific reminder
@app.route('/get_reminder/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        return jsonify({'id': reminder.id, 'date': reminder.date, 'time': reminder.time, 'message': reminder.message, 'remind_type': reminder.remind_type})
    else:
        return jsonify({'error': 'Reminder not found'}), 404

# Route to update a reminder
@app.route('/update_reminder/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    data = request.get_json()

    date = data.get('date')
    time = data.get('time')
    message = data.get('message')
    remind_type = data.get('remind_type')

    if not all([date, time, message, remind_type]):
        return jsonify({'error': 'Incomplete data'}), 400

    try:
        reminder = Reminder.query.get(reminder_id)
        if reminder:
            reminder.date = date
            reminder.time = time
            reminder.message = message
            reminder.remind_type = remind_type
            db.session.commit()
            return jsonify({'message': 'Reminder updated successfully'}), 200
        else:
            return jsonify({'error': 'Reminder not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a reminder
@app.route('/delete_reminder/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    try:
        reminder = Reminder.query.get(reminder_id)
        if reminder:
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({'message': 'Reminder deleted successfully'}), 200
        else:
            return jsonify({'error': 'Reminder not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
