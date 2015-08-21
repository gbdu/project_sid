import logging

formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(name)s:%(lineno)d} %(levelname)s - %(message)s','%H:%M:%S')

logger = logging.getLogger("neuron")
hdlr = logging.FileHandler('logs/neuron')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


logger.info("working")