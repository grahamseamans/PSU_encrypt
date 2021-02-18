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
        R_0, R_1, R_2, R_3 = R
        for _ in range(20):
            # print("Beginning round: ", self.round)
            # print("keys: ", [hex(x) for x in self.key_list[self.round]])
            F_0, F_1 = self.f_func(R_0, R_1)
            swap0 = R_0
            swap1 = R_1
            R_0 = R_2 ^ F_0
            R_1 = R_3 ^ F_1
            R_2 = swap0
            R_3 = swap1
            # print("Block: ", hex(cons_bin_list([R_0, R_1, R_2, R_3], 16)))
            # print()
            self.round += 1
        y_0 = R_2
        y_1 = R_3
        y_2 = R_0
        y_3 = R_1
        c = self.whiten([y_0, y_1, y_2, y_3])
        cypher = cons_bin_list(c, 16)
        return cypher

    def f_func(self, R_0, R_1):
        T_0 = self.G(R_0, 0)
        T_1 = self.G(R_1, 1)
        # print("T_0: ", hex(T_0), " T_1: ", hex(T_1))
        key_part_1 = cons_bin(
            self.key_list[self.round][8], self.key_list[self.round][9], input_size=8
        )
        key_part_2 = cons_bin(
            self.key_list[self.round][10], self.key_list[self.round][11], input_size=8
        )
        F_0 = (T_0 + (2 * T_1) + key_part_1) % 2 ** 16
        F_1 = ((2 * T_0) + T_1 + key_part_2) % 2 ** 16
        # print("F_0: ", hex(F_0), " F_1: ", hex(F_1))
        return F_0, F_1

    def G(self, w, occourance):
        occourance *= 4
        g_1, g_2 = bin_split(w, split_index_from_right=8)
        g_3 = self.f_table.do(g_2 ^ self.key_list[self.round][0 + occourance]) ^ g_1
        g_4 = self.f_table.do(g_3 ^ self.key_list[self.round][1 + occourance]) ^ g_2
        g_5 = self.f_table.do(g_4 ^ self.key_list[self.round][2 + occourance]) ^ g_3
        g_6 = self.f_table.do(g_5 ^ self.key_list[self.round][3 + occourance]) ^ g_4
        """
        print(
            "g_1:",
            hex(g_1),
            "g_2:",
            hex(g_2),
            "g_3:",
            hex(g_3),
            "g_4:",
            hex(g_4),
            "g_5:",
            hex(g_5),
            "g_6:",
            hex(g_6),
        )
        """
        return cons_bin(g_5, g_6, input_size=8)
