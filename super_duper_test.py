import os
import logging


logger = logging.Logger(__name__)


numbers_str = os.getenv("NUMBERS", "")
if not numbers_str:
    logger.warning("FILL ENV WITH NUMBERS")
else:
    numbers = list(map(int, numbers_str.split(",")))
    logger.warning(f"SUM {sum(numbers)}")
