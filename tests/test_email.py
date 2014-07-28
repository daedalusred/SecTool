import unittest
from sectool.emailAlert import Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getuser
from socket import gethostname
from datetime import datetime
from time import sleep
import mailbox


class EmailTest(unittest.TestCase):

    def test_send_email(self):
        test = Email()
        msg = MIMEMultipart()
        msg['From'] = "noreply@testing"
        msg["To"] = "{0}@{1}".format(getuser(), gethostname())
        check_txt = str(datetime.now())
        msg["Subject"] = check_txt
        msg["X-Test-ID"] = check_txt
        msg.attach(MIMEText(check_txt, 'plain'))
        test.send_email(msg)
        sleep(1) # Wait for e-mail!
        mbox = mailbox.mbox("/var/mail/{0}".format(getuser()))

        for k, v in mbox.items():
            if v.get('X-Test-ID') == check_txt:
                break
        else:
            self.fail("Failed to find X-Test-ID in mailbox")
        mbox.close()
