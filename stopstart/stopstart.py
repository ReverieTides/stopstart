import time
from typing import Optional, Literal

IGNORE_DURATIONS = [
    Literal["days"],
    Literal["hours"],
    Literal["minutes"],
    Literal["seconds"],
    Literal["milliseconds"],
    Literal["microseconds"],
    Literal["nanoseconds"],
]


class Timer:
    def __init__(
        self,
        ignore_durations: Optional[
            (
                list[
                    Literal["days"],
                    Literal["hours"],
                    Literal["minutes"],
                    Literal["seconds"],
                    Literal["milliseconds"],
                    Literal["microseconds"],
                    Literal["nanoseconds"],
                ]
                | Literal[
                    "days",
                    "hours",
                    "minutes",
                    "seconds",
                    "milliseconds",
                    "microseconds",
                    "nanoseconds",
                ]
            )
        ] = None,
    ):
        self.start_time = None
        self.end_time = None
        self.pause_durations = []
        self.actions = []
        self.latest_start_time = None
        self.is_running = False
        ignore_durations = ignore_durations or []
        ignore_durations = (
            ignore_durations
            if isinstance(ignore_durations, list)
            else [ignore_durations]
        )
        self.ignore_durations = ignore_durations

    def start(self, reset: bool = True):
        latest_time = time.time()
        if reset or not self.start_time:
            self.start_time = latest_time
            self.actions = []
        self.latest_start_time = latest_time
        self.is_running = True

    def stop(self, comment: Optional[str] = None):
        if not self.is_running:
            return
        self.end_time = time.time()
        self.actions.append(
            {
                "start_time": self.latest_start_time,
                "end_time": self.end_time,
                "duration": self.end_time - self.latest_start_time,
                "comment": comment,
            }
        )
        self.is_running = False

    def resume(self):
        self.start(reset=False)

    @staticmethod
    def calculate_total_duration(actions):
        return sum([action["end_time"] - action["start_time"] for action in actions])

    @property
    def total_duration(self):
        """Return the total duration (in seconds) from all actions."""
        return self.calculate_total_duration(self.actions)

    @property
    def nano(self):
        return self.total_duration * 1e9

    @property
    def milli(self):
        return self.total_duration * 1e3

    @property
    def seconds(self):
        return self.total_duration

    @property
    def minutes(self):
        return self.total_duration / 60

    @property
    def hours(self):
        return self.total_duration / 3600

    @property
    def days(self):
        return self.total_duration / 86400

    def format_time(self, duration_in_seconds):
        """Convert total seconds into a nicely formatted string with different durations."""
        days = int(duration_in_seconds // 86400)
        hours = int((duration_in_seconds % 86400) // 3600)
        minutes = int((duration_in_seconds % 3600) // 60)
        seconds = int(duration_in_seconds % 60)
        milliseconds = int((duration_in_seconds % 1) * 1000)
        microseconds = int((duration_in_seconds % 1) * 1e6) % 1000  # Limit to 999
        nanoseconds = int((duration_in_seconds % 1) * 1e9) % 1000  # Limit to 999

        formatted_time = []

        if days and "days" not in self.ignore_durations:
            formatted_time.append(f"{days} day{'s' if days > 1 else ''}")

        if hours and "hours" not in self.ignore_durations:
            formatted_time.append(f"{hours} hour{'s' if hours > 1 else ''}")

        if minutes and "minutes" not in self.ignore_durations:
            formatted_time.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

        if seconds and "seconds" not in self.ignore_durations:
            formatted_time.append(f"{seconds} second{'s' if seconds > 1 else ''}")

        if milliseconds and "milliseconds" not in self.ignore_durations:
            formatted_time.append(
                f"{milliseconds} millisecond{'s' if milliseconds > 1 else ''}"
            )

        if microseconds and "microseconds" not in self.ignore_durations:
            formatted_time.append(
                f"{microseconds} microsecond{'s' if microseconds > 1 else ''}"
            )

        if nanoseconds and "nanoseconds" not in self.ignore_durations:
            formatted_time.append(
                f"{nanoseconds} nanosecond{'s' if nanoseconds > 1 else ''}"
            )

        if len(formatted_time) > 1:
            formatted_time[-1] = "and " + formatted_time[-1]

        return ", ".join(formatted_time) if formatted_time else "0 seconds"

    def __str__(self):
        return (
            self.format_time(self.total_duration)
            if self.total_duration
            else "No time has elapsed"
        )

    def get_stats(self):
        """Return stats for total time, number of sessions, and average session time."""
        num_sessions = len(self.actions)
        total_time = self.total_duration
        avg_time = total_time / num_sessions if num_sessions else 0
        return {
            "total_time": total_time,
            "number_of_stops": num_sessions,
            "average_time_between_stops": avg_time,
        }

    def print(self, prefix=""):
        if prefix:
            print(f"{prefix} {self}")
        else:
            print(self)

    def print_snapshot(self, prefix=""):
        current_time = time.time()
        past_actions = self.actions.copy()
        past_actions.append({"start_time": self.end_time, "end_time": current_time})
        total_seconds = self.calculate_total_duration(past_actions)
        print(f"{prefix} {self.format_time(total_seconds)}")

    def print_actions(self, justification: int = 15):
        for i, each_action in enumerate(self.actions, start=1):
            text = each_action["comment"] if each_action["comment"] else f"Stop {i}:"
            print(
                f'{text:<{justification}} {self.format_time(each_action["duration"])}'
            )
