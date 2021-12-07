import datetime
import fileinput

from more_itertools import peekable

# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
datetime_format = "%d %b %H:%M:%S.%f"
date_pattern_start = 2
date_pattern_end = 2 + 19
window = 15  # minutes


def group(input):
    consume = True

    def window(start, end):
        counter = 0
        for line in input:
            dt = datetime.datetime.strptime(line[date_pattern_start:date_pattern_end], datetime_format)
            if start.time() <= dt.time() and dt.time() < end.time():  # with regards to some abs if logs are interleaved?
                counter = counter + 1
            else:
                break
        return counter

    while consume:
        next_line = input.peek(input)
        window_start = datetime.datetime.strptime(next_line[date_pattern_start:date_pattern_end], datetime_format)
        window_end = window_start + datetime.timedelta(0, 15 * 60)
        count = window(window_start, window_end)
        print(count)
        # todo continue
        consume = False


stdin = peekable(fileinput.input())
group(stdin)
