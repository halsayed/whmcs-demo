import logging
import os

# other config
log_level = os.environ.get('LOG_LEVEL', 'INFO')

# create logger
log = logging.getLogger()
log.setLevel(log_level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(log_level)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)