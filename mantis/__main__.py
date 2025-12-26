"""
MANTIS – Core IA local
Entry point
"""

import signal
from mantis.kernel import Kernel
from mantis.logger import setup_logger


def main():
    logger = setup_logger()
    logger.info("Boot sequence initiated")

    kernel = Kernel()

    signal.signal(signal.SIGINT, kernel.stop)
    signal.signal(signal.SIGTERM, kernel.stop)

    kernel.start()


if __name__ == "__main__":
    main()
