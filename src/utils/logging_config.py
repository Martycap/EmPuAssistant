import logging
import logging.config

def setup_logging():
    """
    Configure and initialize basic logging for the application.
    
    Sets a console handler with a standard formatter and INFO level.
    """
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'INFO',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }

    logging.config.dictConfig(logging_config)
