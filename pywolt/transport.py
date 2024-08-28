import time
from collections import deque

import httpx


class Throttler:
    def __init__(self, calls_per_second=5, min_interval=0.05):
        self.calls_per_second = calls_per_second
        self.min_interval = min_interval
        self.history = deque()

    def __enter__(self):
        if not self.history:
            self.history.append(time.time())
            return self

        if self.min_interval > 0:
            delta = time.time() - self.history[-1]
            if delta < self.min_interval:
                time.sleep(self.min_interval - delta)
        sleep_time = 0
        cur_time = time.time()
        while len(self.history) >= self.calls_per_second:
            last_time = self.history.popleft()
            sleep_time = last_time + 1 - cur_time
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.history.append(time.time())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


class RateLimitedTransport(httpx.BaseTransport):
    def __init__(self, throttler: Throttler, max_attempts: int = 3, wait_time: int = 30, **kwargs):
        self._wrapper = httpx.HTTPTransport(**kwargs)
        self.throttler = throttler
        self.max_attempts = max_attempts
        self.wait_time = wait_time

    def handle_request(self, request, attempt: int = 0):
        with self.throttler:
            response = self._wrapper.handle_request(request)

        if response.status_code == httpx.codes.TOO_MANY_REQUESTS and attempt < self.max_attempts:
            time.sleep(self.wait_time)
            return self.handle_request(request, attempt + 1)

        return response

    def close(self):
        self._wrapper.close()
