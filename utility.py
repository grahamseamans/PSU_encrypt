def bin_to_str(binary):
    """
    while len(string) < arg:
        string = 0 + string"""
    return bin(binary)[2:]


def str_to_bin(string):
    return int(string, 2)
