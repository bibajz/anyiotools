try:
    # Python >=3.10
    from contextlib import aclosing
except ImportError:
    from contextlib2 import aclosing
