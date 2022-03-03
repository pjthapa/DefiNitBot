import os
from cryptography.fernet import Fernet

def get_algo_key():
    # create the ciphertext for the algorand private_key
    current_path = os.path.dirname(__file__)
    key_path = os.path.join(current_path, "../testtext/string.txt")

    # get the fernet_key from OS
    with open(key_path, "r") as keyfile:
        key_string = keyfile.read()
        key_byte = bytes(key_string, "utf-8")
        key = key_byte.decode()

    fernet = Fernet(key)
    #encrypted algorand private_key here
    cipher_string = "gAAAAABiINyfisP7xHuYRItMExkm-fhNLcq0tE6rrv8gF1dw9Xqc2YjGuA91yWd3aRc3x08skq3OnEFdgUvHotg0iZN0JKP18UCZz15fHOoVEp8rFgs4-WPvOMlJLMQ8BnvIaoRn3RbiUN06fwgq05NyUxeKL0XZTYz1N2aR5PSVdY9iS2C_Xpwc0hn_rFmOaUQyPanviTcc"
    cipher = bytes(cipher_string, "utf-8")

    sender_key = fernet.decrypt(cipher).decode()
    return sender_key
