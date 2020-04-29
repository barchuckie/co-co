"""Fibonacci series."""


class Fibonacci():
    """Class implementing cached Fibonacci series."""

    def __init__(self):
        """Initilize with two first elements of the series (f0 anf f1)."""
        self._cache = [1, 1]

    def fib(self, n):
        """Calculate and cache n-th element of the Fibonacci series."""
        if n >= len(self._cache):
            self._cache.append(self.fib(n-2) + self.fib(n-1))
        return self._cache[n]
