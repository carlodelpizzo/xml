
with open('driver.xml', errors='ignore') as xml_file:
    xml_lines = xml_file.readlines()

xml_doc = ''
for line in xml_lines:
    new_line = line.replace('\n', '')
    new_line = new_line.replace('\t', '')
    xml_doc += new_line


def make_xml_tag(xml_string: str):
    name = ''
    parameters = ''
    value = ''
    children = []
    write_name = False
    check_for_close = False
    hold_tag = False
    get_params = False
    get_value = False
    running_string = ''
    held_tag = ''
    for char in xml_string:
        running_string += char
        if get_value:
            if char == '<':
                get_value = False
                hold_tag = True
                continue
            value += char
            continue
        if get_params:
            if char == '>':
                get_params = False
                get_value = True
            parameters += char
            continue
        if check_for_close:
            if hold_tag:
                if char == '>':
                    if '/' not in held_tag or held_tag.replace('/', '') != name:
                        if '/' not in held_tag:
                            children.append(make_xml_tag('<' + held_tag + '>' + xml_string.replace(running_string, '')))
                        held_tag = ''
                        hold_tag = False
                        continue
                    break
                held_tag += char
                continue
            if char == '<':
                hold_tag = True
                continue
            continue
        if write_name:
            if char == '>' or char == ' ':
                get_value = True
                write_name = False
                check_for_close = True
                if char == ' ':
                    get_params = True
                    get_value = False
                continue
            name += char
            continue
        if char == '<':
            write_name = True
            continue

    return [name, value, parameters, children]


print(make_xml_tag(xml_doc))
