import re

def is_id_line(line):
    '''Takes a line and checks to see if it is a clang error message'''
    if len(re.findall(".*:[0-9]+:[0-9]+: (error|warning):.*", line)) == 1:
        return True
    return False

def parse_id_line(line):
    '''Parses a clang line and returns a dict containing the appropriate info'''
    #Todo: this will fail if the filename contains ":"
    elements = line.split(":",4)
    retval = {}
    retval['filename'] = elements[0]
    retval['line_no'] = elements[1]
    retval['char_no'] = elements[2]
    retval['error_type'] = elements[3].strip()
    retval['error_msg'] = elements[4].strip()
    return retval

def parse_clang_output(output):
    lines = output.split("\n")
    sections = []
    for i, line in enumerate(lines):
        if is_id_line(line):
            sections.append(i)
    errors = []
    print sections
    for i, line_pos in enumerate(sections):
        temp = parse_id_line(lines[line_pos])
        if i + 1 < len(sections):
            temp['full_msg'] = "\n".join(lines[line_pos:sections[i + 1]])
        else:
            temp['full_msg'] = "\n".join(lines[line_pos:])
        print temp['full_msg']
        errors.append(temp)
    return errors
