#!/usr/bin/python3
import argparse
import os
from time import sleep

RTHF = argparse.RawTextHelpFormatter
PARSER = argparse.ArgumentParser(description='A simple tool to manage astronomy papers and a bibtex–library', formatter_class=RTHF)
PARSER.add_argument('time', help='length of timer', type=str)
PARSER.add_argument('topic', help='Timer topic', nargs='*', type=str, default=['Timer'])
PARSER.add_argument('-t', '--test', help='do not actually sleep (for testing)', action='store_true')

ARGS = PARSER.parse_args()
topic = ' '.join(ARGS.topic)


def parse(v):
    try:
        return float(str(v).strip())
    except ValueError:
        return 0.0


# parse the time

time = ARGS.time
h = 0
m = 0
s = 0
last = 'm'

if ':' not in time:
    if any(v in time for v in ['h', 'm', 's']):
        if 'h' in time:
            h, time = time.split('h')
            h = parse(h)
            last = 'h'
        if 'm' in time:
            m, time = time.split('m')
            m = parse(m)
            last = 'm'
        if 's' in time:
            s, time = time.split('s')
            s = parse(s)

        if time.strip() != '':
            if last == 'h':
                m = parse(time)
            elif last == 'm':
                s = parse(time)
    else:
        m = parse(time)
elif ':' in time:
    for i, v in enumerate(time.split(':')[::-1]):
        if i == 0:
            s = parse(v)
        elif i == 1:
            m = parse(v)
        elif i == 2:
            h = parse(v)
        else:
            raise ValueError(f"couldn't parse {time}")
else:
    raise ValueError(f"couldn't parse {time}")

# compute total seconds and string representation

total = h * 60 * 60 + m * 60 + s

time_str = ''
if h > 0:
    time_str += f'{h:.0f} h'
if m > 0:

    time_str += f' {m:.0f} m'
if s > 0:
    time_str += f' {s:.0f} s'
time_str = time_str.strip()

# start timer with notification
os.system(f"osascript -e 'display notification \"Timer set to {time_str}\" with title \"Timer\"'")

if not ARGS.test:
    sleep(total)

# produce dialog
output = topic + ' completed after ' + time_str + '.'

try:
    os.system('osascript -e \'Tell application \"System Events\" to activate display dialog \"' + output + '\" buttons {\"OK\"} with title \"Timer\"\' & > / dev/null')
except Exception:
    print(output)
