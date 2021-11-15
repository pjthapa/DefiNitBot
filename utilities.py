from datetime import datetime
import json
import numpy

def get_time_difference(time1):

    fmt = '%Y-%m-%d %H:%M:%S'
    tstamp1 = datetime.strptime(time1, fmt)
    tstamp2 = datetime.now()

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))
    return td_mins

def get_current_time_string():
    time =  datetime.now()
    string_time = str(time)
    truncated_to_seconds = string_time[:19]
    return truncated_to_seconds

def time_validity(user:str, current_time:str) -> bool:
    with open("user_log.txt", "r") as infile:
        data = json.load(infile)

    try:
        user_time_stamp = data[user]
        if get_time_difference(user_time_stamp) < 1440:
            return False
        else:
            return True
    except:                                                                                                            # user is tipping for the first time.
        return True

def random_number():
    """returns random int between [1,10] with log-normal distribution"""
    number = numpy.random.lognormal(size = 1)
    number = int(numpy.round(number)[0]) + 1
    if number > 10:
        return 10
    else:
        return number

def random_data_logger(user_sending:str, user_recieving:str, timestamp:str, transaction:str):
    with open("random_data.txt", "r") as infile:
        data = json.load(infile)
    new_data = {transaction: {"sender":user_sending, "reciver":user_recieving, "time": timestamp}}
    data.update(new_data)
    with open("random_data.txt", "w") as outfile:
        json.dump(data, outfile)
