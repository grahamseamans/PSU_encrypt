def bin_to_str(binary, lenght):
    string = bin(binary)[2:]
    while len(string) < lenght:
        string = "0" + string
    return string


def bin_to_hex_no_0x(binary, length):
    block = hex(binary)[2:]
    if len(block) < length:
        block = "0" + block
    return block


def str_hex_no_0x_to_bin(hexi):
    return int(hexi, 16)


def str_to_bin(string):
    return int(string, 2)


def bin_to_ascii(binary):
    string = bin_to_str(binary, lenght=64)
    out = ""
    while string:
        character = string[:8]
        string = string[8:]
        out += chr(int(character, 2))
    return out


def BinaryToDecimal(binary):
    decimal, i = 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def cons_bin(first, second, input_size):
    return (first << input_size) | second


def cons_bin_list(l, item_size):
    ans = 0
    for item in l:
        ans = cons_bin(ans, item, item_size)
    return ans


def bin_split(binary, split_index_from_right):
    mask = 2 ** split_index_from_right - 1
    right = binary & mask
    left = binary >> split_index_from_right
    return left, right


def bin_multi_split(binary, split_size, num_splits):
    split = []
    for _ in range(num_splits):
        binary, taken = bin_split(binary, split_size)
        split.append(taken)
    split.reverse()
    return split


if __name__ == "__main__":
    a = 0b11
    b = 0b10
    c = 0b10
    x = [a, b, c]
    print(bin(cons_bin_list(x, 2)))
