import json
import logging.config

from .config import CONFIG

logging.config.dictConfig(json.loads(str(CONFIG)))
logger = logging.getLogger('fast_api')
