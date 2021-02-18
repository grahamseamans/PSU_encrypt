from utility import bin_to_str, str_to_bin

test_key = 0xABCDEF0123456789ABCD


class key:
    def __init__(self, key):
        self.bin_key = key
        self.str_key = None
        self.update_str_key()

    def update_str_key(self):
        self.str_key = bin_to_str(self.bin_key, lenght=80)

    def update_bin_key(self):
        self.bin_key = str_to_bin(self.str_key)

    def rotate_left(self):
        lsb = self.str_key[1:]
        msb = self.str_key[0]
        self.str_key = lsb + msb
        self.update_bin_key()

    def get_subkey(self, x):
        self.rotate_left()
        pos = x % 10
        scaled_pos = 80 - (pos * 8)
        str_substring = self.str_key[scaled_pos - 8 : scaled_pos]
        return str_to_bin(str_substring)

    def get_keys(self):
        keys = []
        for round in range(20):
            keys.append([])
            for four in range(12):
                x = (4 * round) + (four % 4)
                keys[round].append(self.get_subkey(x))
        return keys


def print_hex(l):
    for sublist in l:
        for subkey in sublist:
            print(hex(subkey), end=" ")
        print()


if __name__ == "main":
    key_obj = key(test_key)
    keylist = key_obj.get_keys()
    print_hex(keylist)
