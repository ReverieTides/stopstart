# stopstart

A simple and intuitive Python class for tracking elapsed time across multiple sessions. The `Timer` class offers a clean, human-readable interface to start and stop time, while providing detailed session statistics and beautifully formatted elapsed time. Whether you're measuring short intervals or long-running processes, the `Timer` class ensures you have accurate data with minimal effort.

## Features

- **Easy to Use**: No complex setup—just call `start()` to begin and `stop()` to end your time tracking. Perfect for quick and efficient use.
- **Time Formatting**: Effortlessly convert elapsed time into a human-friendly format, including days, hours, minutes, seconds, and even fractions like microseconds and nanoseconds.
- **Session Statistics**: Track total time, the number of sessions, and average session durations with just one method call.
- **Formatted Output**: Receive time statistics in an easy-to-read format that includes precise microseconds and nanoseconds.


## Methods:
- **`start(reset=True)`**: Starts the timer. If `reset=True`, it resets the timer and clears any past session history. If `reset=False`, the timer continues from where it left off.
- **`stop()`**: Stops the timer, records the elapsed time for the current session, and appends it to the history.
- **`print_snapshot(prefix="")`**: Prints a snapshot of the total elapsed time up to the current moment, appending a given prefix (optional).
- **`print(prefix="")`**: Prints the formatted total elapsed time with an optional prefix.
- **`get_stats()`**: Returns a dictionary with statistics about the timer, including total time, number of sessions, and average session time.


### Properties:
- **`days`**: The total elapsed time in days.
- **`hours`**: The total elapsed time in hours.
- **`minutes`**: The total elapsed time in minutes.
- **`seconds`**: The total elapsed time in seconds.
- **`milli`**: The total elapsed time in milliseconds (total duration in seconds * 1e3).
- **`nano`**: The total elapsed time in nanoseconds (total duration in seconds * 1e9).
- **`total_duration`**: The total accumulated duration of all actions in seconds, calculated by summing the durations of all recorded sessions.


## Installation

Install the package via `pip`:

```bash
pip install timer
```
## Usage
### Example: Typical Usecase
In this example, the timer is used to measure a single session. Starting and stopping the timer around an activity (like a 2-second wait) will give you the total duration for that period, along with a detailed human-readable output and session statistics.
```python
import time
from stopstart import Timer

# Initialize the Timer
timer = Timer()

# Start the timer (reset to 0)
timer.start()

# Wait for 2 seconds
time.sleep(2)

# Stop the timer
timer.stop()

# Get total duration in seconds
print(f"Total duration in seconds: {timer.seconds}")

# Get a nice clean formatted total duration
print(timer)

# Get stats
stats = timer.get_stats()
print(f"Stats: {stats}")
```
#### Output:
```
Total duration in seconds: 2.000082492828369  
2 seconds, 82 microseconds, and 492 nanoseconds  
Stats: {'total_time': 2.000082492828369, 'num_sessions': 1, 'avg_time': 2.000082492828369}
```
### Example: Session Resuming
The Timer class can resume timing without resetting the session history, allowing you to track multiple periods of time over the course of your work. This makes it easy to start new sessions without losing track of the total time across sessions.

In this example, we start a second session without resetting the timer, simulate another 2-second activity, and then stop the timer to get the updated total duration.
```python
# Start the second session (without reset)
timer.start(reset=False)

# Wait for another 2 seconds
time.sleep(2)

# Stop the timer
timer.stop()

# Get updated total duration
print(f"Total duration in seconds: {timer.seconds}")
print(timer)
```
#### Output:
```
Total duration in seconds: 4.0001797676086426
4 seconds, 179 microseconds, and 767 nanoseconds
Stats: {'total_time': 4.0001797676086426, 'num_sessions': 2, 'avg_time': 2.0000898838043213}
```
### Print snapshots
You can also print time snapshots without affecting the ongoing time tracking. This is useful for logging intermediate results or showing progress without interrupting the current session. The snapshot feature is non-intrusive and does not reset or stop the timer.
```python
time.sleep(30)
timer.print_snapshot(prefix='Snapshot Example:')
timer.print('Actual recorded time:')
```
#### Output:

```
Snapshot Example: 34 seconds, 132 microseconds, and 165 nanoseconds
Actual recorded time: 4 seconds, 179 microseconds, and 767 nanoseconds
```

### Example: Accessing Timer History
The Timer automatically preserves the history of previous sessions in the `actions` attribute. This allows you to access a complete log of all sessions, including their start and stop times, without losing any context. You can easily retrieve this history to analyze past sessions or track progress over time.
```python
import time
from stopstart import Timer

# Initialize the Timer object
timer = Timer()

# Start the first session
timer.start()
time.sleep(2)
timer.stop()
print(f"Session 1 Duration: {timer}")

# Start a second session without resetting the timer
timer.start(reset=False)
time.sleep(3)
timer.stop()
print(f"Session 2 Duration: {timer}")

# Accessing the history of all actions
print(f"Actions History: {timer.actions}")
```
#### Output:

```
Session 1 Duration: 2 seconds, 0 microseconds, and 0 nanoseconds  
Session 2 Duration: 5 seconds, 0 microseconds, and 0 nanoseconds  
Actions History: [
    {'start': 1699392400.0, 'stop': 1699392402.0, 'duration': 2.0}, 
    {'start': 1699392402.0, 'stop': 1699392407.0, 'duration': 5.0}
]
```
