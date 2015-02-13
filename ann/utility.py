def convert_str_to_list(src_str, sep):
    if src_str is None:
        lst = []
    elif sep not in src_str:
        lst = [src_str]
    else:
        lst = src_str.split(sep)
    return lst

def convert_list_to_str(lst, sep):
    if not lst:
        return None
    return reduce(lambda x, y: str(x) + sep + str(y), lst) if isinstance(lst, list) else "Wrong type of {}".format(lst)

def debug(msg):
    print "Debug: {}".format(msg)

