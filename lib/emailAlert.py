"""
SecTool

Send an email alert to the user which triggered the job containing the output from the SecTool run.

23/07/2014
"""

# https://docs.python.org/2/library/email-examples.html

import smtplib
from email.mime.text import MIMEText


def getCommandLineOptions():
    # TODO: get the command line options
    me = "peter.mcnerny@digital.cabinet-office.gov.uk"  # TODO: set this value
    you = "peter.mcnerny@digital.cabinet-office.gov.uk"  # TODO: get this from the cmd line options
    pluginName = None  # TODO: get this from the cmd line options
    return pluginName, me, you


def getOutputFromJsonObject():
    #
    # TODO: parse the JSON object containing the output
    #

    #
    # TODO: update the output variable which is a placeholder for the parsed JSON output
    #
    output = None
    return output


def createEmail(output):
    # Create a text/plain message
    msg = MIMEText(getOutputFromJsonObject().read())

    # get the command line options
    options = getCommandLineOptions()

    msg['Subject'] = "SecTool Results: %s" % options[0]
    msg['From'] = options[1]  # sender's address
    msg['To'] = options[2]  # user's email address


def sendEmail(me, you, msg):
    # Send the email via the SMTP server
    s = smtplib.SMTP('smtp.gmail.com')
    s.sendmail(me, [you], msg)
    s.quit


class Email:
    pass


#
# TESTING
#
addr = "peter.mcnerny@digital.cabinet-office.gov.uk"
message = MIMEText("This is a text message")
message['Subject'] = "Test"
message['from'] = "noreply@digital.cabinet-office.gov.uk"
message['to'] = addr

srv = smtplib.SMTP("smtp.gmail.com")
srv.ehlo()
srv.starttls()
srv.ehlo()
srv.login(addr, "fnunearexavcvklx")
srv.sendmail(addr, addr, message.as_string())
srv.close()