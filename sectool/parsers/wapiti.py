from ..parser import Parser, BASE_JSON, BASE_VULN_ITEM
from .. import markdown_utils as mdu
import misaka
import json


class Wapiti(Parser):
    """Parser for Wapiti JSON output.
    """

    def __init__(self):
        super(Wapiti, self).__init__()

    def parse_to_markdown(self, data, **kwargs):
        output = ""
        vulns = dict((k, v) for k, v in data['vulnerabilities'].items()
                     if len(v) > 0)

        no_vulns = sum([len(x) for x in vulns.values()])

        if len(vulns) == 0 or no_vulns == 0:
            return ""

        max_key = max(len(v) for v in vulns.values())
        if 'max_key' in kwargs:
            max_key = kwargs['max_key']

        output += ''.join([mdu.pad_row((k, str(len(v))), max_key)
                           for k, v in data['vulnerabilities'].items()])
        output += '\n'
        output += mdu.header("Detailed Breakdown", 2)

        for vuln, vuln_data in vulns.items():
            counter = 1
            output += mdu.header(vuln, 3)
            resources = data['classifications'][vuln]
            output += "{0}\n\n".format(resources['desc'])

            for vuln_data_item in vuln_data:
                type_str = "[{0} of {1}] Anomaly found in {2}.\n\n"
                if vuln == "Internal Server Error":
                    type_str = "[{0} of {1}] Vulnerability found in {2}.\n\n"

                type_str = type_str.format(counter, len(vuln_data),
                                           vuln_data_item['path'])

                output += mdu.header(type_str, 4)
                output += mdu.header_code_item("Description",
                                               vuln_data_item['info'])
                output += mdu.header_code_item("HTTP Request",
                                               vuln_data_item['http_request'])
                output += mdu.header_code_item("cURL Command Line",
                                               vuln_data_item['curl_command'])

                output += "{0}\n\n".format("-" * 80)
                counter += 1

            output += mdu.header("Solutions", 4)
            output += "{0}\n\n".format(data['classifications'][vuln]['sol'])
            output += mdu.header("References\n", 4)

            for reference in data['classifications'][vuln]['ref'].values():
                output += "{0}\n".format(reference)

        return output

    def parse_to_html(self, data, **kwargs):
        if 'current_output' in kwargs:
            return misaka.html(kwargs['current_output'] +
                               self.parse_to_markdown(data),
                               extensions=misaka.EXT_TABLES |
                               misaka.EXT_FENCED_CODE)

    def parse_to_json(self, data, return_dict=False):
        vulns_list = list()
        for k, v in data['vulnerabilities'].items():
            vuln = BASE_JSON.copy()
            vuln['type'] = k
            vuln['sol'] = data['classifications'][k]['sol']
            vuln['refs'] = data['classifications'][k]['ref']

            total_items = len(v)
            counter = 1
            for vuln_data_item in v:
                item = BASE_VULN_ITEM.copy()
                item['number'] = counter
                item['total'] = total_items
                item['data']['description'] = vuln_data_item['info']
                item['data']['http_request'] = vuln_data_item['http_request']
                item['data']['cURL_string'] = vuln_data_item['curl_command']
                vuln['items'].append(item)
                counter += 1
            vulns_list.append(vuln)
        return json.dumps(vulns_list)
