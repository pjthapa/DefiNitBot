from reddit_interface import reddit
import json

# message = [[username1, wallet_address1], [username2, wallet_address2] ...]

with open("opt_in.txt", "r") as json_infile:
    message = json.load(json_infile)
    # message = json_infile.split("\n")
    message = message["Data"]


def check_opted_user(username) -> bool:
    """returns True if username has been logged into the wallet"""
    for user in message:
        if username == user[0]:
            return True

    return False


def log_user(username:str, wallet_address:str) -> None:
    """Adds the username provided to eh opt_in.txt file"""
    with open("opt_in.txt", "w") as outfile:
        message.append([username, wallet_address])
        json.dump({"Data":message}, outfile)


def get_user_wallet(username) -> str:
    for user in message:
        if username in user[0]:
            return user[1]

