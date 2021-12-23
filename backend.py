import re
import datetime


def to_datetime(string):
    return datetime.datetime.strptime(string, '%d.%m.%Y %H:%M')


def to_string(date):
    return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')


def parse_timedelta(delta):
    days = delta.days
    if days >= 0:
        s = delta.seconds
    else:
        s = 86400 - delta.seconds
        days += 1
    hours = s // 3600
    minutes = (s - 3600 * hours) // 60
    seconds = s % 60
    return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'


def to_timedelta(string):
    l = list(map(int, re.findall(r'\d+', string)))
    
    if string[0] != '-':
        return datetime.timedelta(days = l[0], hours = l[1], minutes = l[2], seconds = l[3])
    else:
        return datetime.timedelta(days = -l[0], hours = -l[1], minutes = -l[2], seconds = -l[3])


def check_date_format(date):
    try:
        d = to_datetime(date)
    except:
        date = ""
    return date


def auto_transfer(string, length=35, rows=5):
    """Auto-transfers the string by spaces, underscores and by max length.
        
    Key arguments:
    string - the string for transferring
    length - maximal length of each row of the result (default 20)
    rows - maximal number of rows (default 5)
    """

    l = re.split(r'[_. ]+', string)
    cur_len = 0
    cur_transfer = 0
    cur_string = ""
    i = 0
    while cur_transfer + 1 < rows and i < len(l):
        # there is place left in the button

        while i < len(l) and cur_len + len(l[i]) < length:
            # current row is not full yet
            cur_len += len(l[i]) + 1
            cur_string = cur_string + l[i] + " "
            if i < len(l):
                # there are elements of string to add to the result
                i += 1

        if i >= len(l):
            break
        # current row will be full by adding the next element
        # consider several options
        if len(l[i]) > length or length - cur_len > 5:
            # option 1: the next element is too long even for the whole row
            # option 2: there are more than 5 symbols left

            # cut first length-cur_len elements from it, paste into the result
            # change current element of l to the remainder of it
            cur_part = l[i]
            cur_string = cur_string + cur_part[:length-cur_len] + "\n"
            cur_part = cur_part[length-cur_len:]
            l[i] = cur_part
        else:
            # option 3: there are less than 5 symbols left
            # transfer the element to the next row
            cur_string += "\n"

        cur_len = 0
        cur_transfer += 1

    return cur_string



    
