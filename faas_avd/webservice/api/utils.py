import string
import re


def check_page_name(page_name):
    charset = string.ascii_letters
    for l in page_name:
        if charset.find(l) == -1:
            return False
    return True

def safe_cmd(cmd):
    for x in "'\\$":
        cmd = cmd.replace(x, f'\{x}')
    return cmd

def make_args(args):
    if args:
        args = args.split(",")
        for i in range(len(args)):
            if re.search(r'int\((.*)\)', args[i]):
                args[i] = int(re.search(r'int\((.*)\)', args[i]).groups()[0])
                continue
            if re.search(r'str\((.*)\)', args[i]):
                args[i] = str(re.search(r'str\((.*)\)', args[i]).groups()[0])
                continue
            if re.search(r'bool\((.*)\)', args[i]):
                args[i] = bool(int(re.search(r'bool\((.*)\)', args[i]).groups()[0]))
                continue
        args = tuple(args)
    return args