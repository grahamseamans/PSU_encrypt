from utility import bin_to_ascii, bin_to_hex_no_0x, str_hex_no_0x_to_bin
from festel import festel

test_key = 0xABCDEF0123456789ABCD
test_plaintext = 0x7365637572697479
test_ciphertext = 0x7BCC265A38E7555F


class cipher:
    def __init__(self):
        self.file_plain = "./plaintext.txt"
        self.file_encrypted = "./ciphertext.txt"
        self.file_key = "./key.txt"
        self.festel = festel()
        self.key = test_key
        self.block = ""

    def decrypt(self):
        self.get_key()
        encrypted_lines = self.get_ciphertext()
        with open(self.file_plain, "w") as w:
            for block in encrypted_lines:
                block = block[:-1]
                block = str_hex_no_0x_to_bin(block)
                plain = self.festel.decrypt(block)
                plain = bin_to_ascii(plain)
                w.write(plain)

    def get_ciphertext(self):
        with open(self.file_encrypted, "r") as c:
            return c.readlines()

    def encrypt(self):
        self.get_key()
        self.get_plaintext()
        with open(self.file_encrypted, "w") as f:
            while self.plaintext:
                self.extract_leading_plaintext_block()
                self.block_to_bin_with_padding()
                self.block = self.festel.encrypt(self.block)
                self.block = bin_to_hex_no_0x(self.block, 16)
                f.write(self.block + "\n")

    def extract_leading_plaintext_block(self):
        self.block = self.plaintext[:8]
        self.plaintext = self.plaintext[8:]

    def block_to_bin_with_padding(self):
        length = len(self.block)
        self.block = int("".join(format(ord(i), "08b") for i in self.block), 2)
        if length < 8:
            self.block = self.block << (8 - length) * 8

    def get_key(self):
        self.key = ""
        with open(self.file_key, "r") as f:
            self.key = f.read()
        self.key = str_hex_no_0x_to_bin(self.key)
        self.festel.set_key(self.key)

    def get_plaintext(self):
        self.plaintext = ""
        with open(self.file_plain, "r") as f:
            self.plaintext = f.read()[:-1]
