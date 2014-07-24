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

###############################################################################
# Class
###############################################################################
class Email:
    def __init__(self, pluginName = "Wapiti", jsonOutputFileName = "wapitiOutput.json", usersEmailAddress = "peter.mcnerny@digital.cabinet-office.gov.uk", targetUrl = "http://localhost:3000"):
        self.pluginName = pluginName
        self.jsonOutputFileName = jsonOutputFileName
        self.usersEmailAddress = usersEmailAddress
        self.targetUrl = targetUrl

    ###############################################################################
    # Functions
    ###############################################################################

    def parseWapitiOutput(self, json_data):
        # infos, vulnerabilities, classifications, anomalies

        # output is what will be displayed in the email
        output = "Summary\n=======\n\n**Category**\t\t\t\t**Number of Vulnerabilities Found**\n"

        data = json.loads(json_data)

        noOfVulns = 0  # total number of vulnerabilities wapiti found

        # SUMMARY: the first part of the output is a summary of the number of
        # vulnerabilities found for each category of vulnerability

        listOfVulns = []

        # maintain count of vulns and append the parsed vuln data to the output
        for k, v in data['vulnerabilities'].items():
            noOfVulns += len(v)

            if len(v) != 0:
                listOfVulns.append(v)

            # TODO: nicely format output for email (console will look bad)
            # set an appropriate number of tabs for tidy output
            tabs = "\t\t\t\t"
            if len(k) > 15:
                tabs = "\t\t\t"
            if "Backup" in k:
                tabs = "\t\t\t\t"
            if "Cross" in k:
                tabs = "\t\t\t"
            if "Potentially" in k:
                tabs = "\t\t"

            output += "{0}{1}{2}\n".format(k, tabs, len(v))

        # ANOMALIES: the next part of the output describes a found attack, its
        # location, the HTTP request and the cURL command line command used to find
        # the vuln
        #for vuln in listOfVulns:
        #    data['classifications']

        for k, v in data['classifications'].items():
            print(k, v)

        print (output)  # TODO: DEBUG - remove
        #noOfVulns = len(data['vulnerabilities'].values()) # wrong

        ### DEBUG ###
        #for key, val in json.loads(json_data).items():
         #   print(key, val)



        return output, noOfVulns


    def getOutputFromJsonObject(self, json_data):
        #
        # TODO: parse the JSON object containing the output
        #
        json_data = open(self.jsonOutputFileName).read()

        #print(json_data)

        # output needs to be handled specific to each plugin
        if self.pluginName.lower() == "wapiti":
            parsedData = self.parseWapitiOutput(json_data)

        return parsedData[0], parsedData[1]  # output, numOfErrors


    def createEmail(self):
        # create the contents of the email
        output = self.getOutputFromJsonObject(self)

        message = MIMEText(output[0])

        # how many issues the tool has found
        numOfErrors = output[1]
        issues = "Issues Found"
        if numOfErrors == 1:
            issues = "Issue Found"

        # add addressing to the email
        message['Subject'] = "SecTool Results: {0} {1} [{2}]".format(
            numOfErrors, issues, self.pluginName)
        message['from'] = FROM_ADDRESS
        message['to'] = self.usersEmailAddress  # email address of user who ran the tool
        return message


    def sendEmail(self, message):
        srv = smtplib.SMTP(SMTP_SERVER)
        srv.ehlo()
        srv.starttls()
        srv.ehlo()
        srv.login(self.usersEmailAddress, GOOGLE_APP_PASSWORD)
        srv.sendmail(FROM_ADDRESS, self.usersEmailAddress, message.as_string())
        srv.close()

    def triggerEmailAlert(self):
        emailMessage = self.createEmail()
        self.sendEmail(emailMessage)


###############################################################################
# Testing
###############################################################################

e = Email()
msg = e.createEmail()
e.sendEmail(msg)




