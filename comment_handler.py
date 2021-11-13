with open("read_posts.txt", "r") as infile:
    # read each reply so far
    posts_read = infile.read()
    posts_read = posts_read.split("\n")
    posts_read = list(filter(None, posts_read))


def check_for_read(comment_id:str) -> bool:
    """
    :param comment_id: unique ID of the submission
    :return: True if the post_id has not already been logged, false otherwise.
    """
    if comment_id in posts_read:
        return False
    else:
        return True


def log_post(comment_id:str) -> None:
    """
    logs post_id into read_posts.txt
    """
    with open("read_posts.txt", "w") as outfile:
        posts_read.append(comment_id)
        for post_id in posts_read:
            outfile.write(post_id + "\n")

