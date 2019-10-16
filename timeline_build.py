#!/usr/bin/env python3
"""
Build timeline for a CFN build
and "draw" a diagram of it
"""
import json
import sys
import arrow

def print_help():
    """
    Usage printer for any error
    """
    print(
        '''
    Usage:
     ./timeline_build.py events.json

     hint: to generate the events.json run
     aws cloudformation describe-stack-events --stack-name mystack > events.json
        ''')
    sys.exit(1)

# depending the screen size and whole build time
SCALE = 0.18  # potential improvment, calc this based on terminal size and max time
# Set it to -1 to show all entries
TOSMALL = 1

RESOURCES = []
START_TIMES = {}
END_TIMES = {}

try:
    EF = sys.argv[1]
    if EF == "help":
        print_help()
    with open(EF) as json_file:
        DATA = json.load(json_file)
        for event in DATA['StackEvents']:
            if event['ResourceStatus'] in ("CREATE_IN_PROGRESS", "CREATE_COMPLETE"):
                r = event['LogicalResourceId']
                if event['ResourceStatus'] == "CREATE_IN_PROGRESS":
                    try:
                        if START_TIMES[r] < arrow.get(event['Timestamp']).timestamp:
                            START_TIMES[r] = arrow.get(event['Timestamp']).timestamp
                    except KeyError:
                        START_TIMES[r] = arrow.get(event['Timestamp']).timestamp
                else:
                    END_TIMES[r] = arrow.get(event['Timestamp']).timestamp
                if r not in RESOURCES:
                    RESOURCES.append(r)
except IndexError:
    print("[ERROR] You forgot to specify the event file location!")
    print("to check usage run ./timeline_build.py help")
    sys.exit(1)
except FileNotFoundError:
    print("[ERROR] Can't find the file, make sure it exist and readable!")
    print("to check usage run ./timeline_build.py help")
    sys.exit(1)
except ValueError:
    print("[ERROR] That does not look like a well formated JSON!")
    print("to check usage run ./timeline_build.py help")
    sys.exit(1)

FIRST = min(START_TIMES, key=START_TIMES.get)
FIRST_T = START_TIMES[FIRST]

RESOURCES.sort(key=START_TIMES.get)

for res in RESOURCES:
    start = START_TIMES[res] - FIRST_T
    end = END_TIMES[res] - FIRST_T
    timesum = end - start
    if timesum > TOSMALL:
        print(" "*(int(start*SCALE)) +
              "»"*(int(timesum*SCALE)) +
              " - {} ({}s)".format(res, timesum))
