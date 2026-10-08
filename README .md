# log-error-triage-tool

Parses application log files and outputs a triage summary: errors grouped by endpoint and status code, with occurrence counts and the first and last time each one was seen.

## Why this exists

When a customer reports that something broke overnight, the first questions are always the same: what failed, how many times, and when did it start. Answering that from a raw log means scrolling. This tool answers it in one command, so the investigation starts from a summary instead of a wall of text.

Built as a personal project, based on the log triage I did in support at IDBS and Dispatch. I built it with Claude Code walking me through each step.

## Usage

```
python3 triage.py sample.log
```

Example output (first three groups):

```
/api/v1/orders (500) - 8 occurrences
  first seen: 2026-09-13T22:16:02Z
  last seen:  2026-09-14T00:43:18Z
  Internal Server Error: database connection timeout

/api/v1/webhooks (429) - 13 occurrences
  first seen: 2026-09-13T22:16:34Z
  last seen:  2026-09-14T00:47:03Z
  Too Many Requests: rate limit exceeded

/api/v1/inventory (503) - 10 occurrences
  first seen: 2026-09-13T22:18:04Z
  last seen:  2026-09-14T00:32:49Z
  Service Unavailable: upstream timeout
```

## How it works

Each line is matched against a regex expecting a timestamp, log level, HTTP method, endpoint, status code, and message. Lines with an ERROR level are grouped by endpoint and status code. Each group tracks a count plus the first and last timestamp seen. Lines that don't match the expected format are skipped instead of crashing the run, since real logs usually have a few malformed entries mixed in.

## Sample data

`sample.log` is a generated log file included so the tool can be run without supplying your own. It has a mix of INFO and ERROR lines, several recurring failure types, and a few malformed entries.

## Known limitations

- Expects one log format (timestamp, level, method, endpoint, status, message). Other formats will not parse.
- Shows the message from the first occurrence in each group only.
- Results are printed in the order each error first appeared, not sorted by count.

## Requirements

Python 3. No external dependencies.
