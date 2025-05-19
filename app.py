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
    return render_template("index.html")

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    name = request.form.get("name","Anonymous")
    email = request.form.get("email","Not known")
    subject = request.form.get("subject", "No subject")
    message = request.form.get("message")

    # Apply default values if name or email are empty
    if not name:
        name = 'Anonymous'
    if not email:
        email = 'anonymous@example.com'
    if not subject:
        email = 'None'

    html_content = f"""
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Subject:</b> {subject}</p>
    <p><b>Message:</b><br>{message.replace('\n', '<br>')}</p>
    """

    msg = Message(
        subject=f"New Feedback from {name}",
        recipients=[os.getenv('MAIL_USERNAME')],  # You receive it yourself
        html = html_content
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
