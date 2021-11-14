from reddit_interface import reddit, get_message, send_message, get_posts, get_comments, subreddit
from comment_handler import check_for_read, log_post
from inbox_handler import check_opted_user, log_user, get_user_wallet
from algorand_interface import tip_finite
# driver code

def main():
    tip_bot_page = ""                                                                                                   #add the algoexplorer.io link for the tip bot address once created
    bot_instruction_page = ""
    # read unread inbox message for "opt in".
    unread_messages = get_message()

    for message in unread_messages:
        try:
            if message.subject.lower() == "opt in":
                user = message.author
                if not check_opted_user(user):
                    user_wallet_address = message.body

                    log_user(user.name, user_wallet_address)

                    send_message(user, (f"Your wallet {user_wallet_address} has been opted in for the tipbot! \n\n"
                                        f"Consider donating to the Tip Bot at this wallet: {tip_bot_page}"))            # This needs to be formatted better

                else:
                    send_message(user, "You have already opted in to the Defi-Nite Tipbot. "
                                      f"Were you looking for other commands? You can view them here at \n\n "
                                       f"{bot_instruction_page} \n\n "
                                       f"Consider donating to the Tip Bot at this wallet: {tip_bot_page}")

            else:
                send_message(user, f"The bot cannot understand that command. Go here for a "
                                   f"list of commands ->{bot_instruction_page} \n\n"
                                   f"Consider donating to the Tip Bot at this wallet: {tip_bot_page}")                  # format this message

            message.mark_read()                                                                                         # this needs to be a function of its own

        except:
            message.mark_read()                                                                                           # create a function to log the errors: The functions should log the timestamp, the message and the user that made the message.
            print(f"Issue with reading this message {message.body} from {user.name}")

    # read comments for "!nite them!"
    for sub in subreddit:
        posts = get_posts(sub, limit=100)
        list_of_comment_tree = get_comments(posts)
        for comment_tree in list_of_comment_tree:
            for comment in comment_tree.list():

                if check_for_read(comment.id):

                    if "!nite them!" in comment.body:

                        tipping_user = comment.author
                        tipping_username = tipping_user.name

                        valid_parent_id = comment.parent_id
                        valid_parent = reddit.comment(valid_parent_id).author
                        parent_name = valid_parent.name

                        if check_opted_user(parent_name):
                            wallet_to_tip = get_user_wallet(parent_name)
                            print(wallet_to_tip)
                            sender_key = "QC/NiCyN7YtfiIKUQFAYfMw9YLfv0AZavS7Ts+0RIf0xL9864AAK2Qr9YJZgahm36iOCoNq5uxV5cMpal21MGA=="                                 # add central wallet address
                            sender_address = "GEX56OXAAAFNSCX5MCLGA2QZW7VCHAVA3K43WFLZODFFVF3NJQMMRBDKVY"

                            try:
                                tip_finite(sender_key, sender_address, wallet_to_tip, 389093723)                        #currently tipping shiva inu
                                                                                                                        # change this back once lower is fixed
                            except:
                                print("tipping error")
                            send_message(parent_name, f"{tipping_username} tipped you with 1 Finite ASA. Find out more about this ->")

                            log_post(comment.id)

                        else:
                            send_message(tipping_username, f"The user you tried to tip {parent_name} has not opted in to the Finite ASA."
                                                       f" Let them know about this!")
                            send_message(parent_name, f"{tipping_username} tried to tip you with a Finite ASA. Unfortuately, the bot was unable to "
                                                       f"process the tip as you have not opted into the ASA. Find out how to do so here - >")

                            log_post(comment.id)
                    else:
                        log_post(comment.id)


if __name__ == "__main__":

    main()
