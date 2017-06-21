import sys
from config import LOGENABLED

# logging wrapper
def log(message):
    if LOGENABLED:
        print str(message)
        sys.stdout.flush()