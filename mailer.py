import yagmail

class Mailer():

    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

        self.yag = yagmail.SMTP(sender_email, sender_password)


    def send(self, to, subject, body, attachments=None):
        self.yag.send(to=to,
                      subject=subject,
                      contents=body,
                      attachments=attachments)
