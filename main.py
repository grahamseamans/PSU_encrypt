import sys
from cipher import cipher


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        encrypt_decrypt = input("e for encrypt, d for decrypt: ")
    else:
        encrypt_decrypt = sys.argv[1]
    c = cipher()
    if encrypt_decrypt == "e":
        c.encrypt()
    elif encrypt_decrypt == "d":
        c.decrypt()
    else:
        print("bad input")
