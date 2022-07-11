from asyncio.log import logger
import requests
import logging


logger = logging.Logger(__name__)

req = requests.get("https://aws.random.cat/meow")
logger.warning(req.json())