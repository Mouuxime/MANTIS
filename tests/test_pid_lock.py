import os
import unittest

from mantis.kernel import pid_is_running


class PidLockTest(unittest.TestCase):
    def test_current_process_pid_is_running(self):
        self.assertTrue(pid_is_running(os.getpid()))

    def test_invalid_pid_is_not_running(self):
        self.assertFalse(pid_is_running(-1))

    def test_unlikely_pid_is_not_running(self):
        self.assertFalse(pid_is_running(999999))


if __name__ == "__main__":
    unittest.main()