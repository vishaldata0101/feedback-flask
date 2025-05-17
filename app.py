from flask import Flask, request, render_template, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

@app.route("/")
def index():
    return redirect("/feedback")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    msg = Message(
        subject=f"New Feedback from {name}",
        recipients=[os.getenv('MAIL_USERNAME')],  # You receive it yourself
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )

    try:
        mail.send(msg)
        flash("Thanks! Your feedback has been sent.", "success")
    except Exception as e:
        print("Error:", e)
        flash("Something went wrong. Please try again later.", "error")

    return redirect("/feedback")

if __name__ == "__main__":
    app.run(debug=True)
