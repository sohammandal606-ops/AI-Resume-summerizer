# Shim: pyaudioop -> audioop-lts (Python 3.13 compatibility)
# pydub imports `pyaudioop as audioop` on Python 3.13+ where audioop was removed.
# audioop-lts provides the `audioop` module under its original name.
# This shim re-exports it so pydub can find it as `pyaudioop`.
from audioop import *
