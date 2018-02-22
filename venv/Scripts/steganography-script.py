#!c:\users\deepak\pycharmprojects\instabot1\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'steganography==0.1.1','console_scripts','steganography'
__requires__ = 'steganography==0.1.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('steganography==0.1.1', 'console_scripts', 'steganography')()
    )
