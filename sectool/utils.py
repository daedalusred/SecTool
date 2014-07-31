
import sys

if sys.version < '3':
    def bytes_str(x):
        return x
else:
    def bytes_str(x):
        return bytes(x, 'utf-8')
