#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main(port=None):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceDriving.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if port is None:
        port = 8081
    if len(sys.argv) == 1:
        sys.argv += ["runserver", "0.0.0.0:%s" % port]
    sys.argv[0] = "manage.py"
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
