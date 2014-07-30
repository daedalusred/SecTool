class Parser(object):

    def __init__(self):
        self.supported_formats = ["json", "html", "markdown"]

    def parse(self, data, data_format):
        if data_format == 'html':
            self.parse_to_html(data)
        elif data_format == 'markdown':
            self.parse_to_markdown()
        elif data_format == 'json':
            self.parse_to_json()
        else:
            raise Exception("Unknown data_format specified")

    def parse_to_markdown(self, data):
        raise NotImplementedError("Parse has not been implemented")

    def parse_to_html(self, data):
        raise NotImplementedError("Parse has not been implemented")

    def parse_to_json(self, data):
        raise NotImplementedError("Parse has not been implemented")
