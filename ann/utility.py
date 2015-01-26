def convert_str_to_list(src_str, sep):
    if src_str is None:
        lst = []
    elif sep not in src_str:
        lst = [src_str]
    else:
        lst = src_str.split(sep)
    return lst
