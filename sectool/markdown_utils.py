"""
Markdown helper functions.

"""


def pad_row(columns, max_col):
    """Pad a row to create a Markdown Table.
    """
    final_str = ""
    final_str += "|"

    for i in columns:
        final_str += " {0} | ".format(i.center(max_col))

    final_str += "\n"
    return final_str


def quote(quote_item):
    return "> {0} \n".format(quote_item)


def header_code_item(header, code, level=5):
    output = ""
    output += "{0} {1}\n".format(("#" * level), header)
    output += "```\n{0}\n```\n\n".format(code)
    return output


def header(header, level=1):
    return "" + ("#" * level) + header + "\n\n"
