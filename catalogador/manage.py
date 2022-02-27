import os
import sys
#import logging
from datetime import datetime


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogador.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s %(name)s %(levelname)s %(message)s',
    #     filename=f'./logs/log_{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log',
    #     filemode='w'
    #     )

    # log = logging.getLogger(__name__)
    
    main()
