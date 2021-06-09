import string


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