from utility import bin_to_str, str_to_bin, str_hex_no_0x_to_bin, bin_multi_split


class key:
    def __init__(self):
        self.key_file = "./key.txt"
        self.bin_key = 0
        self.str_key = ""
        self.get_key_from_file()
        self.update_str_key()

    def get_key_from_file(self):
        read_key = None
        with open(self.key_file, "r") as f:
            read_key = f.read()
        self.bin_key = str_hex_no_0x_to_bin(read_key)

    def get_whitening_list(self):
        k = bin_multi_split(self.bin_key, split_size=16, num_splits=5)
        k = k[:-1]
        return k

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
