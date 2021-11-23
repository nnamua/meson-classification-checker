from typing import Union


class Log:
    """Keeps track of successful and failed tests"""

    successful = 0
    failures   = 0

    @staticmethod
    def success():
        """Increment success counter"""
        Log.successful += 1

    @staticmethod
    def failure():
        """Increment failure counter"""
        Log.failures += 1

    @staticmethod
    def result() -> Union[int, int]:
        """Returns the tuple (successes, failures)"""
        return (Log.successful, Log.failures)