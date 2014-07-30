import unittest
from sectool.email_alert import Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getuser
from socket import gethostname
from datetime import datetime
from time import sleep
import mailbox
import json


class EmailTest(unittest.TestCase):

    def setUp(cls):
        cls.obj = Email(duration=0, users_email_address="",
                        plugin_name="wapiti",
                        input_file="tests/test_wapiti.json",
                        target_url="http://localhost:3000",
                        show_std_out=False)

    def test_send_email(self):
        """Test that we can send mail and verify that it arrives at the users
        inbox.
        """
        test = Email(0, 0, 0, 0, 0, 0)
        msg = MIMEMultipart()
        msg['From'] = "noreply@testing"
        msg["To"] = "{0}@{1}".format(getuser(), gethostname())
        check_txt = str(datetime.now())
        msg["Subject"] = check_txt
        msg["X-Test-ID"] = check_txt
        msg.attach(MIMEText(check_txt, 'plain'))
        test.send_email(msg)
        sleep(1)  # Wait for e-mail!
        mbox = mailbox.mbox("/var/mail/{0}".format(getuser()))

        for k, v in mbox.items():
            if v.get('X-Test-ID') == check_txt:
                break
        else:
            self.fail("Failed to find X-Test-ID in mailbox")
        mbox.close()

    def test_generate_report(self):
        """Test that a report is generated (check that the return is not none.
        """
        with open('tests/test_wapiti.json', 'r+') as f:
            data = json.loads(f.read())
            output = self.obj.parse_wapiti_output(data)
            self.assertIsNotNone(output)
