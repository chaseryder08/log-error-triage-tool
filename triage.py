import sys
import re

def read_lines(path):
    try:
        with open(path) as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []

def parse(line):
    m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) ([A-Z]+) ([A-Z]+) (\S+) (\d{3}) (.+)", line)
    return m

def group_errors(lines):
    errors = {}

    for line in lines:
        m = parse(line)
        if m is None:
            continue

        timestamp, level, method, endpoint, status, message = m.groups()

        if level != "ERROR":
            continue

        key = (endpoint, status)

        if key not in errors:
            errors[key] = {
                "count": 0,
                "first": timestamp,
                "last": timestamp,
                "message": message,
            }

        errors[key]["count"] += 1
        errors[key]["last"] = timestamp

    return errors

def print_summary(errors):
    for key, data in errors.items():
        endpoint, status = key
        print(f"{endpoint} ({status}) - {data['count']} occurrences")
        print(f"  first seen: {data['first']}")
        print(f"  last seen:  {data['last']}")
        print(f"  {data['message']}")
        print()

if __name__ == "__main__":
    lines = read_lines(sys.argv[1])
    errors = group_errors(lines)
    print_summary(errors)
