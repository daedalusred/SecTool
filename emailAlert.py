"""
SecTool

Send the output from the plugins in an email alert to the user
who triggered the job.

23/07/2014
"""

import json
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

###############################################################################
# Members
###############################################################################

SENDMAIL = "/usr/sbin/sendmail"
FROM_ADDRESS = "noreply-sectool@digital.cabinet-office.gov.uk"
NO_REPLY = "> Do not reply to this email address as it is unmonitored.\n"
KNOWN_SENDERS = ">\n> Please add '{0}' to your list of known addresses.\n".format(FROM_ADDRESS)
MARKDOWN = ">\n> Use a markdown reader to view this message with nice formatting.{0}".format('\n'*3)

DEBUG = False

###############################################################################
# Class
###############################################################################


class Email:
    def __init__(self, plugin_name="Wapiti", json_output_filename="wapitiOutput.json",
                 users_email_address="peter.mcnerny@digital.cabinet-office.gov.uk",
                 target_url="http://localhost:3000"):
        self.pluginName = plugin_name
        self.jsonOutputFileName = json_output_filename
        self.usersEmailAddress = users_email_address
        self.targetUrl = target_url

    ###############################################################################
    # Functions
    ###############################################################################

    def parse_wapiti_output(self, json_data):
        # json contains infos, vulnerabilities, classifications, anomalies

        # output is what will be displayed in the email
        output = NO_REPLY
        output += KNOWN_SENDERS
        output += MARKDOWN

        title = "Summary"
        output += "{0}\n{1}\n\n**Category**\t\t\t\t**Number of Vulnerabilities Found**\n".format(title, '='*len(title))

        data = json.loads(json_data)

        no_of_vulns = 0  # total number of vulnerabilities wapiti found

        # SUMMARY: the first part of the output is a summary of the number of
        # vulnerabilities found for each category of vulnerability
        dict_of_vulns = {}

        # maintain count of vulns and append the parsed vuln data to the output
        for k, v in data['vulnerabilities'].items():
            no_of_vulns += len(v)

            if len(v) != 0:
                if v not in dict_of_vulns.items():
                    dict_of_vulns[k] = len(v)

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

            # an asterisk is used as the following is a bullet point list
            output += "\n* {0}{1}{2}\n".format(k, tabs, len(v))

        # ANOMALIES & VULNERABILITIES: the next part of the output describes
        # an identified attack, its location, the HTTP request and the cURL
        # command line command used to find the vuln
        title = "Detailed Vulnerability Information"
        output += "\n\n{0}\n".format(title)
        output += '='*len(title)

        for vuln in dict_of_vulns:
            output += "\n\n{0}\n{1}".format(vuln, '-'*len(vuln))
            output += "\n**Description**\n\t"

            for k, v in data['classifications'].items():
                if k == vuln:
                    output += "{0}\n\n\n".format(v['desc'])

                    for key, val in data['vulnerabilities'].items():
                        if key == vuln:
                            counter = 1

                            for listItem in val:
                                if vuln == "Internal Server Error":
                                    output += "**[{0} of {1}] Vulnerability found in {2}**\n\n".format(
                                        counter, dict_of_vulns[vuln], listItem['path'])
                                else:
                                    output += "**[{0} of {1}] Anomaly found in {2}**\n\n".format(
                                        counter, dict_of_vulns[vuln], listItem['path'])

                                output += "**Description**\n\t{0}\n".format(listItem['info'])
                                output += "\n**HTTP Request**\n\t{0}\n".format(listItem['http_request'])
                                output += "**cURL command line**\n\t{0}\n\n".format(listItem['curl_command'])
                                counter += 1

                    output += "**Solutions**\n\t{0}".format(v['sol'])
                    output += "\n\n**References**\n\t"

                    for element in v['ref'].items():
                        output += "{0}\n\t".format(element)

        return output, no_of_vulns

    def get_output_from_json_object(self):
        json_data = open(self.jsonOutputFileName, 'r+').read()

        # handling of output needs to be specific to each plugin
        parsed_data = None
        if self.pluginName.lower() == "wapiti":
            parsed_data = self.parse_wapiti_output(json_data)

        # TODO: add parsing for other vulnerability scanners here

        if DEBUG is True:
            print(parsed_data[0])

        return parsed_data[0], parsed_data[1]  # output, numOfErrors

    def create_email(self):
        # create the contents of the email
        output = self.get_output_from_json_object()

        message = MIMEText(output[0])

        # how many issues the tool has found
        num_or_errors = output[1]
        issues = "Issues Found"
        if num_or_errors == 1:
            issues = "Issue Found"

        # add addressing to the email
        message['Subject'] = "SecTool Results: {0} {1} [{2}]".format(
            num_or_errors, issues, self.pluginName)
        message['from'] = FROM_ADDRESS
        message['to'] = self.usersEmailAddress  # email address of user who ran the tool
        return message

    def send_email(self, message):
        p = Popen([SENDMAIL, "-t"], stdin=PIPE)
        p.communicate(bytes(message.as_string(), 'utf-8'))
        if p.returncode != 0:
            raise Exception("Oops")

    def trigger_email_alert(self):
        self.send_email(self.create_email())


###############################################################################
# Testing
###############################################################################
if __name__ == '__main__':
    e = Email()
    msg = e.create_email()

    if DEBUG is True:
        e.send_email(msg)
