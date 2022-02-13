

def get_xml_data(xml_path=None, xml_string=None):
    if xml_path:
        with open(xml_path, errors='ignore') as xml_file:
            xml_lines = xml_file.readlines()

        xml_string = ''
        for line in xml_lines:
            new_line = line.replace('\n', '')
            new_line = new_line.replace('\t', '')
            xml_string += new_line

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
                            children.append(get_xml_data(xml_string='<' + held_tag + '>' +
                                                                    xml_string.replace(running_string, '')))
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


# [name, value, parameters, children]
class XMLObject:
    def __init__(self, xml_path=None, xml_data=None, parent=None):
        if xml_path:
            xml_data = get_xml_data(xml_path)

        self.parent = parent
        self.name = xml_data[0]
        self.value = xml_data[1]
        self.parameters = []
        self.children = []

        param_name = ''
        param_value = ''
        get_name = False
        get_value = False
        # Parse parameters
        for char in xml_data[2]:
            if get_value:
                if char == '"' or char == "'":
                    if param_value == '':
                        continue
                    get_value = False
                    self.parameters.append([param_name, param_value])
                    param_name = ''
                    param_value = ''
                    continue
                param_value += char
                continue
            if get_name:
                if char == '=':
                    get_value = True
                    get_name = False
                    continue
                param_name += char
                continue
            if char != ' ':
                get_name = True
                param_name += char

        # Make children
        for child in xml_data[3]:
            self.children.append(XMLObject(xml_data=child, parent=self))

    def get_lines(self, layer=0):
        lines = []
        line = ''
        tabs = ''
        for _ in range(layer):
            tabs += '\t'
        line += tabs + '<' + self.name
        if len(self.parameters) != 0:
            line += ' '
            for param in self.parameters[:-1]:
                line += param[0] + '="' + param[1] + '" '
            line += self.parameters[-1][0] + '="' + self.parameters[-1][1] + '"'
        line += '>' + self.value
        if len(self.children) == 0:
            line += '</' + self.name + '>'
            return [line]
        lines.append(line)
        children_lines = []
        for child in self.children:
            children_lines.append(child.get_lines(layer=layer+1))
        for line_list in children_lines:
            for string in line_list:
                lines.append(string)
        lines.append(tabs + '</' + self.name + '>')
        return lines


xml_object = XMLObject('test.xml')

output_list = xml_object.get_lines()
for text in output_list:
    print(text)
