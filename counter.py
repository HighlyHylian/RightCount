import os
import signal
from datetime import datetime

file_name = f"{datetime.now().strftime('%Y-%m-%d')}_tally_counter.log"

def read_last_entry():
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                timestamp, count = map(float, last_line.split(','))
                return timestamp, count
            else:
                return 0, 0
    except FileNotFoundError:
        return 0, 0

def write_entry(timestamp, count):
    with open(file_name, 'a') as file:
        file.write(f"{timestamp},{count}\n")

def signal_handler(sig, frame):
    global interrupted
    print("\nSaving count and exiting.")
    interrupted = True
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

timestamp, count = read_last_entry()
print(f"Last tally at {datetime.fromtimestamp(timestamp)} - Count: {count}")

interrupted = False

try:
    while True:
        input("Press Enter to increase count:")
        count += 1
        timestamp = datetime.now().timestamp()
        print(f"Current count: {count} - Timestamp: {datetime.fromtimestamp(timestamp)}")
        write_entry(timestamp, count)
except KeyboardInterrupt:
    print("\nInterrupted with Ctrl+C.")

if not interrupted:
    write_entry(timestamp, count)
