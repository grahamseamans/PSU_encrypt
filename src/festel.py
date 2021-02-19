from utility import bin_multi_split, bin_split, cons_bin, cons_bin_list
from ftable import ftable
from key import key

test_key = 0xABCDEF0123456789ABCD
test_plaintext = 0x7365637572697479
test_cyphertext = 0x7BCC265A38E7555F


class festel:
    def __init__(self):
        self.round = 0
        self.key = test_key
        self.key_list = key(self.key).get_keys()
        self.f_table = ftable()

    def set_key(self, new_key):
        self.key = new_key
        self.key_list = key(self.key).get_keys()

    def whiten(self, w):
        k = bin_multi_split(self.key, split_size=16, num_splits=5)
        k = k[:-1]
        R = [w_x ^ k_x for w_x, k_x in zip(w, k)]
        return R

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
            # print("Beginning round: ", self.round)
            # print("keys: ", [hex(x) for x in self.key_list[self.round]])
            F0, F1 = self.f_func(R0, R1)
            swap0 = R0
            swap1 = R1
            R0 = R2 ^ F0
            R1 = R3 ^ F1
            R2 = swap0
            R3 = swap1
            # print("Block: ", hex(cons_bin_list([R0, R1, R2, R3], 16)))
            # print()
            self.round += 1
        y0 = R2
        y1 = R3
        y2 = R0
        y3 = R1
        c = self.whiten([y0, y1, y2, y3])
        cypher = cons_bin_list(c, 16)
        return cypher

    def f_func(self, R0, R1):
        T0 = self.G(R0, 0)
        T1 = self.G(R1, 1)
        # print("T_0: ", hex(T0), " T_1: ", hex(T1))
        key_part_1 = cons_bin(
            self.key_list[self.round][8], self.key_list[self.round][9], input_size=8
        )
        key_part_2 = cons_bin(
            self.key_list[self.round][10], self.key_list[self.round][11], input_size=8
        )
        F0 = (T0 + (2 * T1) + key_part_1) % 2 ** 16
        F1 = ((2 * T0) + T1 + key_part_2) % 2 ** 16
        # print("F_0: ", hex(F0), " F_1: ", hex(F1))
        return F0, F1

    def G(self, w, occourance):
        occourance *= 4
        g1, g2 = bin_split(w, split_index_from_right=8)
        g3 = self.f_table.do(g2 ^ self.key_list[self.round][0 + occourance]) ^ g1
        g4 = self.f_table.do(g3 ^ self.key_list[self.round][1 + occourance]) ^ g2
        g5 = self.f_table.do(g4 ^ self.key_list[self.round][2 + occourance]) ^ g3
        g6 = self.f_table.do(g5 ^ self.key_list[self.round][3 + occourance]) ^ g4
        """
        print(
            "g_1:",
            hex(g1),
            "g_2:",
            hex(g2),
            "g_3:",
            hex(g3),
            "g_4:",
            hex(g4),
            "g_5:",
            hex(g5),
            "g_6:",
            hex(g6),
        )
        """
        return cons_bin(g5, g6, input_size=8)
