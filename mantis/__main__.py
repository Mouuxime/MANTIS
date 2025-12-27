"""
MANTIS – Core IA local
Starter
"""

import signal
from mantis.kernel import Kernel
from mantis.logger import setup_logger


def main():
    logger = setup_logger()
    logger.info("Démarrage de Mantis")

    kernel = Kernel()

    signal.signal(signal.SIGINT, kernel.stop)
    signal.signal(signal.SIGTERM, kernel.stop)

    kernel.start()


if __name__ == "__main__":
    main()
