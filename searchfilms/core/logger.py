
import logging

logger = logging.getLogger('fast_api')
logging.basicConfig(filename='api.log', encoding='utf-8',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)

