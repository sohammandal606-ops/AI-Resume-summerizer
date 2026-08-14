# Shim: pyaudioop -> audioop-lts (Python 3.13+ compatibility)
try:
    from audioop import *
except ModuleNotFoundError:
    try:
        from audioop_lts import *
    except ModuleNotFoundError:
        import warnings
        warnings.warn("Neither 'audioop' nor 'audioop-lts' was found. Audio processing with pydub may fail on Python 3.13+.")

