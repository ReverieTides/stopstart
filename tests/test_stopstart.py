import time
import pytest
from stopstart.stopstart import Timer


@pytest.fixture
def timer():
    """Fixture to create a fresh  instance for each test."""
    return Timer()


def test_start(timer):
    """Test the start method of the Timer."""
    timer.start()
    assert timer.is_running is True
    assert timer.start_time is not None
    assert timer.latest_start_time is not None
    initial_time = time.time()
    assert timer.start_time == pytest.approx(initial_time, abs=0.05)


def test_stop(timer):
    """Test the stop method of the Timer."""
    timer.start()
    time.sleep(0.1)
    timer.stop()
    assert timer.is_running is False
    assert timer.end_time is not None
    assert timer.total_duration == pytest.approx(0.1, abs=0.05)


def test_total_duration(timer):
    """Test the total duration calculation after start/stop."""
    timer.start()
    time.sleep(0.2)
    timer.stop()
    assert timer.total_duration == pytest.approx(0.2, abs=0.05)


def test_format_time(timer):
    """Test the format_time method to format elapsed time."""
    timer.start()
    time.sleep(1.5)
    timer.stop()
    formatted_time = timer.format_time(timer.total_duration)
    assert "second" in formatted_time
    assert "1" in formatted_time


def test_get_stats(timer):
    """Test the get_stats method to calculate total time, number of stops, and average session time."""
    timer.start()
    time.sleep(1)
    timer.stop()
    timer.start()
    time.sleep(0.2)
    timer.stop()
    stats = timer.get_stats()
    assert stats["total_time"] == pytest.approx(0.2, abs=0.05)
    assert stats["number_of_stops"] == 1
    assert stats["average_time_between_stops"] == pytest.approx(0.20, abs=0.05)


def test_print(timer, capsys):
    """Test the print method to ensure the formatted time is correctly printed."""
    timer.start()
    time.sleep(1)
    timer.stop()
    timer.print()
    captured = capsys.readouterr()
    assert "second" in captured.out
    assert "microseconds" in captured.out
    assert "nanoseconds" in captured.out


def test_print_snapshot(timer, capsys):
    """Test the print_snapshot method to ensure the formatted time is correctly printed after a snapshot."""
    timer.start()
    time.sleep(1)
    timer.stop()
    timer.print_snapshot()
    captured = capsys.readouterr()
    print(timer)
    assert "second" in captured.out
    assert "microseconds" in captured.out
    assert "nanoseconds" in captured.out


def test_multiple_sessions_with_reset(timer):
    """Test multiple start/stop sessions with reset."""
    timer.start()
    time.sleep(0.1)
    timer.stop()
    time.sleep(0.2)
    timer.start()
    time.sleep(0.3)
    timer.stop()
    assert timer.total_duration == pytest.approx(0.3, abs=0.05)


def test_multiple_sessions_without_reset(timer):
    """Test multiple start/stop sessions without reset."""
    timer.start()
    time.sleep(0.1)
    timer.stop()
    timer.start(reset=False)
    time.sleep(0.2)
    timer.stop()
    timer.start(reset=False)
    time.sleep(0.3)
    timer.stop()
    assert timer.total_duration == pytest.approx(0.6, abs=0.05)


def test_no_actions(timer):
    """Test the case when no actions (start/stop) have been performed."""
    assert timer.total_duration == 0
    assert timer.total_duration == 0
    assert timer.get_stats()["total_time"] == 0
