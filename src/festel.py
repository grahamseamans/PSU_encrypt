from utility import bin_multi_split, bin_split, cons_bin, cons_bin_list
from ftable import ftable
from key import key

test_key = 0xABCDEF0123456789ABCD
test_plaintext = 0x7365637572697479
test_cyphertext = 0x7BCC265A38E7555F


class festel:
    def __init__(self):
        self.round = 0
        self.key = key()
        self.key_list = self.key.get_keys()
        self.whitening_list = self.key.get_whitening_list()
        self.f_table = ftable()

    def decrypt(self, encrypted):
        self.key_list.reverse()
        plain_text = self.encrypt(encrypted)
        self.key_list.reverse()
        return plain_text

    def encrypt(self, plain_text):
        self.round = 0
        w = bin_multi_split(plain_text, split_size=16, num_splits=4)
        R = self.whiten(w)
        R0, R1, R2, R3 = R
        for _ in range(20):
            F0, F1 = self.f_func(R0, R1)
            swap0 = R0
            swap1 = R1
            R0 = R2 ^ F0
            R1 = R3 ^ F1
            R2 = swap0
            R3 = swap1
            self.round += 1
        y0 = R2
        y1 = R3
        y2 = R0
        y3 = R1
        c = self.whiten([y0, y1, y2, y3])
        cypher = cons_bin_list(c, 16)
        return cypher

    def whiten(self, w):
        R = [w_x ^ k_x for w_x, k_x in zip(w, self.whitening_list)]
        return R

    def f_func(self, R0, R1):
        T0 = self.G(R0, order="first")
        T1 = self.G(R1, order="second")
        k = self.key_list[self.round][8:12]
        combined1 = cons_bin(k[0], k[1], input_size=8)
        combined2 = cons_bin(k[2], k[3], input_size=8)
        F0 = (T0 + (2 * T1) + combined1) % 2 ** 16
        F1 = ((2 * T0) + T1 + combined2) % 2 ** 16
        return F0, F1

    def G(self, w, order):
        k = []
        if order == "first":
            k = self.key_list[self.round][0:4]
        else:
            k = self.key_list[self.round][4:8]
        g1, g2 = bin_split(w, split_index_from_right=8)
        g3 = self.f_table.do(g2 ^ k[0]) ^ g1
        g4 = self.f_table.do(g3 ^ k[1]) ^ g2
        g5 = self.f_table.do(g4 ^ k[2]) ^ g3
        g6 = self.f_table.do(g5 ^ k[3]) ^ g4
        return cons_bin(g5, g6, input_size=8)

    def get_subkey_third(self):
        return self.key_list[self.round][8:12]
