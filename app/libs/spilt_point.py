import re


def spilt_point(filename, key='.'):
    regex = '(.*)\\' + key + '(.*)'
    match = re.match(regex, filename)
    return match.group(1), match.group(2)
