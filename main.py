import smtplib
import random
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'your-email@gmail.com '
PASSWORD = 'your-password'


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    names, emails = get_contacts('mycontacts.txt')
    message_template = read_template('message.txt')
    receivers = names.copy()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(MY_ADDRESS, PASSWORD)

    for i in range(len(names) - 2):
        name = names[i]
        email = emails[i]

        randomnum = random.randint(0, len(receivers) - 1)
        while receivers[randomnum] == name:
            randomnum = random.randint(0, len(receivers) - 1)

        receiver = receivers.pop(randomnum)

        msg = MIMEMultipart()

        message = message_template.substitute(SECRET_SANTA=name.title(), GIFT_RECEIVER=receiver.title())

        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Secret Santa Email"

        msg.attach(MIMEText(message, 'plain'))

        server.send_message(msg)
        del msg

    receiver = ""
    index = len(names) - 2

    if receivers[0] == names[index]:
        receiver = receivers.pop(1)
    elif receivers[0] == names[index + 1]:
        receiver = receivers.pop(0)
    elif receivers[1] == names[index]:
        receiver = receivers.pop(0)
    elif receivers[1] == names[index + 1]:
        receiver = receivers.pop(1)
    else:
        randomnum = random.randint(0, len(receivers) - 1)
        receiver = receivers.pop(randomnum)

    msg = MIMEMultipart()

    message = message_template.substitute(SECRET_SANTA=names[index].title(), GIFT_RECEIVER=receiver.title())

    msg['From'] = MY_ADDRESS
    msg['To'] = emails[index]
    msg['Subject'] = "Secret Santa Email"

    msg.attach(MIMEText(message, 'plain'))

    server.send_message(msg)
    del msg

    name = names[index + 1]
    receiver = receivers.pop(0)
    email = emails[index + 1]
    msg = MIMEMultipart()

    message = message_template.substitute(SECRET_SANTA=name.title(), GIFT_RECEIVER=receiver.title())

    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Secret Santa Email"

    msg.attach(MIMEText(message, 'plain'))

    server.send_message(msg)

    server.close()


if __name__ == '__main__':
    main()
