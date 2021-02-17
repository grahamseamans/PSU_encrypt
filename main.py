from utility import bin_to_str, str_to_bin
from ftable import ftable
from key import key

test_key = int("abcdef0123456789abcd", 16)
test_plaintext = int("7365637572697479", 16)  # "security" in hex


# untested!!!!
def whiten(key, W):
    plaintext = bin_to_str(W)
    test_key = bin_to_str(key)
    w = []
    k = []
    for i in range(0, 64, 16):
        w.append(str_to_bin(plaintext[i : i + 16]))
    for i in range(0, 64, 16):
        k.append(str_to_bin(test_key[i : i + 16]))
    R = []
    for w_x, k_x in zip(w, k):
        R.append(w_x ^ k_x)
    return R


class cypher:
    def __init__(self):
        self.round = 0
        self.key = key().get_keys()
        self.f_table = ftable()

    def f_func(self, R_0, R_1):
        T_0 = self.G(R_0, 0)
        T_1 = self.G(R_1, 1)
        key_part_1 = "".join(self.key[self.round][8], self.key[self.round][9])
        key_part_2 = "".join(self.key[self.round][10], self.key[self.round][11])
        F_0 = (T_0 + (2 * T_1) + key_part_1) % 2 ^ 16
        F_1 = ((2 * T_0) + T_1 + key_part_2) % 2 ^ 16
        return F_0, F_1

    def G(self, w, occourance):
        occourance *= 4
        w = bin_to_str(w)
        g_1 = str_to_bin(w[:7])  # should these be 7?
        g_2 = str_to_bin(w[7:])
        g_3 = self.f_table.do(g_2 ^ self.key[self.round][0 + occourance]) ^ g_1
        g_4 = self.f_table.do(g_3 ^ self.key[self.round][1 + occourance]) ^ g_2
        g_5 = self.f_table.do(g_4 ^ self.key[self.round][1 + occourance]) ^ g_3
        g_6 = self.f_table.do(g_5 ^ self.key[self.round][1 + occourance]) ^ g_4
        return str_to_bin("".join([bin_to_str(g_5), bin_to_str(g_6)]))


def print_list(l):
    for i in l:
        print(hex(i))


print_list(whiten(test_key, test_plaintext))
