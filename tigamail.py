from __future__ import print_function

__author__ = 'Iplodman'

import cmd
import smtplib
import email.utils
from email.mime.text import MIMEText
import webbrowser


class Email(cmd.Cmd):
    intro = "Welcome to TigaMail Beta, the Gmail client! \nFor help: help|?\n"
    prompt = "TigaMail: "
    ruler = "~"

    port = 587
    cl_port = 465
    logged_in = False
    acc = None

    def preloop(self):
        self.con_types = self.load_smtps()
        print("TigaMail starting...\n")

    def emptyline(self):
        print("No command entered!")

    def default(self):
        print("Looks like you broke something!")

    def connect(self, smtp_type):
        self.server = smtplib.SMTP(smtp_type, self.port)
        self.server.ehlo()
        self.server.starttls()

    def do_login(self, line):
        """
        Log in to the server with an account. Usage:
            login
        """

        user_email = self.msg_in("Your email: ")

        for type in self.con_types:
            for variant in type.split("/"):
                if variant in user_email:
                    addr_type = self.con_types[type]
                    self.connect(addr_type)

        password = self.msg_in("Password: ")
        try:
            self.server.login(user_email, password)
            self.acc = user_email
        except smtplib.SMTPAuthenticationError:
            self.err_out("Email and password mis-match!")

    def do_sendmail(self, line):
        """
        Send an email. Usage:
            sendmail
        """
        if self.acc:
            try:
                to = self.msg_in("Recipient's email: ")
                subj = self.msg_in("Subject: ")

                msg = MIMEText(self.msg_in("Body: "))
                msg["To"] = email.utils.formataddr(("Recipient", to))
                msg["From"] = email.utils.formataddr(("Author", self.acc))
                msg["Subject"] = subj

                self.server.sendmail(self.acc, to, msg.as_string())
                self.msg_out("Email sent.")
            except Exception as e:
                self.err_out("Email not sent:\n" + str(e))
        else:
            self.err_out("Please log in first.")

    def do_register(self, acc_type):
        """
        Register for a supported account (googlemail|yahoo). Usage:
            register account_type
        """
        if acc_type in ("gmail", "googlemail", "gmail.com", "googlemail.com"):
            webbrowser.open("https://accounts.google.com/SignUp", new=True)
        elif acc_type in ("yahoo", "yahoo.com"):
            webbrowser.open("https://login.yahoo.com/config/login", new=True)
        else:
            self.msg_out("Invalid account type. For help: `help register`")

    def load_smtps(self):
        smtps = {}
        with open("smtpaddrs.txt", "r") as f:
            lines = f.readlines()
            print(lines)
            for line in lines:
                if line[0] != "#":
                    split_line = line.split(" ")
                    smtps[split_line[0].strip()] = split_line[1].strip()
        return smtps

    @staticmethod
    def msg_out(msg):
        print("  ~ " + msg)

    @staticmethod
    def msg_in(prompt):
        return raw_input("  ~ " + prompt)

    @staticmethod
    def err_out(err):
        print(err)

if __name__ == "__main__":
    cmdline = Email()
    cmdline.cmdloop()
