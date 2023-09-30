from flask import Flask, render_template, request, redirect, send_from_directory, send_file
import smtplib
from email.message import EmailMessage
import toml
import os
import datetime

# Flask instance
app = Flask(__name__)

# Environment vars to differentiate between local/testing/production
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# File Paths
about_path = "static/content/about.toml"
education_path = "static/content/education.toml"
experience_path = "static/content/work_experience.toml"
skill_path = "static/content/skills.toml"

# Read in data to apply to templates
with open(about_path, 'r') as tomlfile:
    about = toml.load(tomlfile)

with open(education_path, 'r') as tomlfile:
    edu = toml.load(tomlfile)

with open(skill_path, 'r') as tomlfile:
    skills = toml.load(tomlfile)

with open(experience_path, 'r') as tomlfile:
    exp_dict = toml.load(tomlfile)

    experience = []
    for exp in exp_dict.values():
        experience.append(exp)

    experience.sort(key=lambda e: e['end'], reverse=True)


@app.route("/")
def index():
    return render_template("homepage.html",
                           title=f"{about['name']} - Home",
                           about=about,
                           edu=edu,
                           experience=experience,
                           skills=skills)


@app.route("/resume")
def download_resume():
    date = datetime.date.today()
    return send_file('static/content/resume.pdf',
                     mimetype='application/pdf',
                     download_name=f"Rubin_Connor_{date.year}-{date.month}-{date.day}.pdf")


@app.route("/contact", methods=['POST'])
def send_email():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']

        your_name = about.get('name')
        your_email = about.get('email')
        your_password = os.getenv('GMAIL_APP_PASSWORD')  # TODO Hide password in config -- add to heroku config

        # Logging in to our email account
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(your_email, your_password)

            # Sender's and Receiver's email address
            sender_email = "csrubin+portfolio-contact@gmail.com"
            receiver_email = "csrubin@gmail.com"

            msg = EmailMessage()
            msg.set_content("First Name : " + str(name) + "\nEmail : " + str(email) + "\nSubject : " + str(
                subject) + "\nMessage : " + str(message))
            msg['Subject'] = 'New Response on Personal Website'
            msg['From'] = sender_email
            msg['To'] = receiver_email

        except:
            pass
        redirect('/')
        # Send the message via our own SMTP server.
        try:
            # sending an email
            server.send_message(msg)
        except:
            pass
    return redirect('/')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Placeholder routes #
@app.route("/work-history")
def work_history():
    return "MORE EXPERIENCE"


@app.route('/personal')
def personal():
    return "PERSONAL"


@app.route('/projects')
def projects():
    return render_template("project.html",
                           title=f"{about['name']} - Projects",
                           about=about)


if __name__ == "__main__":
    app.run(debug=DEBUG)
