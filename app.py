from flask import Flask, render_template, request, url_for, redirect
import smtplib
from email.message import EmailMessage
import toml

# File Paths
about_path = "static/content/about.txt"
contact_path = "static/content/contact.txt"
programming_path = "static/content/programming_skills.txt"
engineering_path = "static/content/engineering_skills.txt"
other_path = "static/content/other_skills.txt"
experience_path = "static/content/work_experience.toml"

# Repeated elements
linked_in = "https://www.linkedin.com/in/connor-rubin-58a98b7a/"


app = Flask(__name__)


def get_text_from_file(file_path: str, as_list: bool = False) -> str:
    with open(file_path, 'r') as pyf:
        if as_list:
            text_list = pyf.readlines()
            text = ', '.join(text_list)
        else:
            text = pyf.read()
    return text

def get_contact_info(file_path: str) -> tuple[str, str, str, str]:
    with open(file_path, 'r') as pyf:
        street = pyf.readline().strip()
        city_state = pyf.readline().strip()
        phone = pyf.readline().strip()
        email = pyf.readline().strip()
    return street, city_state, phone, email



def get_role_from_toml(file_path: str, company: str, role: str) -> list:
    with open(file_path, 'r') as tomlfile:
        data = toml.load(tomlfile)

    return data[company][role]


def get_responsbilities_from_role(file_path: str, company: str, role: str) -> list:
    with open(file_path, 'r') as tomlfile:
        data = toml.load(tomlfile)
        print(data[company][role]['responsibilities'])
    return data[company][role]["responsibilities"]

@app.route("/")
def index():
    about = get_text_from_file(about_path)
    street, city_state, phone, email = get_contact_info(contact_path)
    address = street + ', ' + city_state
    programming_skills = get_text_from_file(programming_path, as_list=True)
    engineering_skills = get_text_from_file(engineering_path, as_list=True)
    other_skills = get_text_from_file(other_path, as_list=True)

    tpm_list = get_responsbilities_from_role(experience_path, 'Superpedestrian', 'Product Manager')

    return render_template("index.html",
                           about=about,
                           email=email,
                           phone=phone,
                           address=address,
                           programming_skills=programming_skills,
                           engineering_skills=engineering_skills,
                           other_skills=other_skills,
                           tpm_list=tpm_list,
                           linked_in=linked_in)

@app.route("/send-email/", methods=['POST'])
def send_email():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']

        your_name = "Connor Rubin"
        your_email = "csrubin@gmail.com"
        your_password = ""  # TODO Hide password in config

        # Logging in to our email account
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(your_email, your_password)

        # Sender's and Receiver's email address
        sender_email = "csrubin@gmail.com"
        receiver_email = "csrubin@gmail.com"

        msg = EmailMessage()
        msg.set_content("First Name : "+str(name)+"\nEmail : "+str(email)+"\nSubject : "+str(subject)+"\nMessage : "+str(message))
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
    app.run(debug=False)
