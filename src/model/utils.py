import os

if "DEBUG" in os.environ:
    DEBUG = os.environ["DEBUG"]
else:
    DEBUG = 1

if "TARGET_PLATFORM" in os.environ:
    ARCH = os.environ["TARGET_PLATFORM"]
else:
    ARCH = "x86_64"

if "APP_VERSION" in os.environ:
    VERSION = os.environ["APP_VERSION"]
else:
    VERSION = "Latest"

# Langs
EN = "English"
RU = "Русский"

# Scheme options.json
FG = "fg"
BG = "bg"
SEL = "sel"
FONT = "font"
FONTSIZE = "fontsize"
POSITIONS = "positions"
POSI = "posi"
AUDIO = "audio"
CHUNK = "chunk"

# Scheme sync.json
TIME_START = 0
TIME_END = 1
TIME = 2
WORD = 3
POS_START = 4
POS_END = 5
POS = 6

# Scheme micro.json
L_POS = 0
R_POS = 1
L_WORDS = 2
R_WORDS = 3
L_a = 4
L_b = 5

# Scheme BOOK_ENG_SCHEME / BOOK_RUS_SCHEME
ANNOT = 0
TXT = 1
FB2 = 2
MP3 = 3
SYNC = 4

# Scheme BOOK_SCHEME
COVER = 0
MICRO = 1
ENG2RUS = 2
RUS2ENG = 3
VALID = 4
