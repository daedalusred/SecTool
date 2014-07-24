"""
SecTool

Send the output from the plugins in an email alert to the user
who triggered the job.

23/07/2014
"""

# https://docs.python.org/2/library/email-examples.html

import json
import smtplib
from email.mime.text import MIMEText


###############################################################################
# Members
###############################################################################

FROM_ADDRESS = "noreply@digital.cabinet-office.gov.uk"
SMTP_SERVER = "smtp.gmail.com"
GOOGLE_APP_PASSWORD = "fnunearexavcvklx"

command_line_args = None  # TODO: set by constructor
jsonOutputFromTool = None  # TODO: set by constructor
pluginName = "Wapiti"   # TODO: set by constructor
usersEmailAddress = "peter.mcnerny@digital.cabinet-office.gov.uk"  # TODO: set by constructor

###############################################################################
# Functions
###############################################################################

def parseWapitiOutput(json_data):
    # infos, vulnerabilities, classifications, anomalies

    data = json.loads(json_data)

    noOfVulns = len(data['vulnerabilities'].values())

    #for key, val in json.loads(json_data).items():
    #    print(key, val)
    output = None

    return output, noOfVulns


def getOutputFromJsonObject():
    #
    # TODO: parse the JSON object containing the output
    #
    json_data = open('wapitiOutput.json').read()

    #print(json_data)

    # output needs to be handled specific to each plugin
    if pluginName.lower() == "wapiti":
        parsedData = parseWapitiOutput(json_data)

    return parsedData[0], parsedData[1]  # output, numOfErrors


def createEmail():
    # create the contents of the email
    output = getOutputFromJsonObject()

    #message = MIMEText(output[0].read())  # TODO: use the JSON output
    message = MIMEText("This is a text message")  # TODO: this is test data - remove

    # how many issues the tool has found, with correct English :)
    numOfErrors = output[1]
    issues = "Issues Found"
    if numOfErrors == 1:
        issues = "Issue Found"

    # add addressing to the email
    message['Subject'] = "SecTool Results: {0} {1} [{2}]".format(
        numOfErrors, issues, pluginName)
    message['from'] = FROM_ADDRESS
    message['to'] = usersEmailAddress  # email address of user who ran the tool
    return message


def sendEmail(message):
    srv = smtplib.SMTP(SMTP_SERVER)
    srv.ehlo()
    srv.starttls()
    srv.ehlo()
    srv.login(usersEmailAddress, GOOGLE_APP_PASSWORD)
    srv.sendmail(FROM_ADDRESS, usersEmailAddress, message.as_string())
    srv.close()


###############################################################################
# Class
###############################################################################
class Email:
    pass



###############################################################################
# Testing
###############################################################################
msg = createEmail()
sendEmail(msg)



