import logging
logger = logging.getLogger('uvcsite.uvc.seccheck')

def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)
