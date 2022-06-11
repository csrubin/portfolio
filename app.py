from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
import toml
import os

from helper import get_text_from_file, get_experience

# File Paths
contact_path = "static/content/contact.txt"
about_path = "static/content/about.toml"
programming_path = "static/content/programming_skills.txt"
engineering_path = "static/content/engineering_skills.txt"
other_path = "static/content/other_skills.txt"
experience_path = "static/content/work_experience.toml"

with open(about_path, 'r') as ct:
    about = toml.load(ct)
    name = about.get('name')
    title = about.get('title')
    about_me = about.get('about_me')
    street = about.get('street')
    city = about.get('city')
    state = about.get('state')
    zipcode = about.get('zipcode')
    email = about.get('email')
    phone = about.get('phone')
    address = street + ', ' + city + ', ' + state + ' ' + zipcode

DEBUG = (os.getenv('DEBUG', 'False') == 'True')

research_link = "https://ieeexplore.ieee.org/document/9000312"  # Todo upload to site

app = Flask(__name__)


@app.route("/")
def index():
    programming_skills = get_text_from_file(programming_path, as_list=True)
    engineering_skills = get_text_from_file(engineering_path, as_list=True)
    other_skills = get_text_from_file(other_path, as_list=True)
    experience = get_experience(experience_path)

    return render_template("index.html",
                           name=name,
                           title=title,
                           about_me=about_me,
                           email=email,
                           phone=phone,
                           street=street,
                           city=city,
                           state=state,
                           zipcode=zipcode,
                           address=address,
                           programming_skills=programming_skills,
                           engineering_skills=engineering_skills,
                           other_skills=other_skills,
                           experience=experience,
                           linked_in=about.get('linked_in'))


@app.route("/send-email/", methods=['POST'])
def send_email():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']

        your_name = about.get('name')
        your_email = about.get('email')
        your_password = os.getenv('EMAIL_PASSWORD')  # TODO Hide password in config

        # Logging in to our email account
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
        # Send the message via our own SMTP server.
        try:
            # sending an email
            server.send_message(msg)
        except:
            pass
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=DEBUG)
