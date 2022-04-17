import logging

import coloredlogs


def get_logger(name="simplify", debug=False):
    """Create a colored logger.

    Debug messages are not displayed by default.
    Set up debug flag to True if you want to log all debug messages.

    # Get logger
    logger = get_logger(debug=True)

    # Some examples of usage:
    logger.debug("this is a debugging message")
    logger.info("this is an informational message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")
    """
    level_styles = dict(coloredlogs.DEFAULT_LEVEL_STYLES)
    coloredlogs.install(
        level=logging.DEBUG if debug else logging.INFO,
        logger=logging.getLogger(name),
        level_styles=level_styles,
        fmt="%(asctime)s|%(levelname)s|%(module)s:%(lineno)s|%(funcName)s(): %(message)s")
    return logging.getLogger(name)
