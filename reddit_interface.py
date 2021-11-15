import praw
import json
# """
# reddit file that interacts with the reddit API using praw.
# """

# create reddit instance

reddit = praw.Reddit(
    client_id="O4NyaSFtRiSCnQMRc691mA",
    client_secret="1atyXnwEhwJyXLI_wX3aMAaOayAy-g",
    user_agent="A tip bot for the DefiNite community ASA on Algorad by u/DefiNiteASABot",
    username="Botforpjt",
    password="home135pj",
)

# check if reddit instance is writeable
# print(reddit.read_only)

# events
def get_message() -> iter:
    # returns iterable messages in inbox that are unread
    unread = reddit.inbox.unread()
    message_iter = unread
    # for messages in unread:
    #     messages.mark_read()
    return message_iter


def get_posts(subreddits: str, limit=100) -> list:
    # returns a list of iterable pasts from the correct_subreddit
    posts = []
    for submission in reddit.subreddit(subreddits).hot(limit=limit):
        posts.append(submission)
    return posts


def get_comments(submission: iter) -> iter:
    # returns the iterable comment forest for a given submission
    comment_list = []
    for post in submission:
        comment_list.append(post.comments)
    return comment_list


def send_message(user: str, message: str) -> None:
    """
    :param user: user in reddit (add username exception)
    :param message: message to send to user
    :return: None
    """
    subject = "Tip bot testnet"
    reddit.redditor(user).message(subject, message)

def log_tip_timestamp(user:str, timestamp:str) ->None:
    with open ("user_log.txt", "r") as infile:
        data = json.load(infile)

    with open("user_log.txt", "w") as outfile:
        data[user] = timestamp
        json.dump(data, outfile)

# def previous_tip_timestamp(user:str) -> str:                                                                          #redundat function. handled in utilities
#     with open("user_log.txt", "r") as infile:
#         data = json.load(infile)
#     try:
#         timestamp = data[user]
#         return timestamp
#     except:
#         return "First time tipping"

subreddit = ["finite_asa"]                                                                                                    # add subreddits where this is possible please

