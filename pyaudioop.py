import sys
import warnings

# Shim: pyaudioop -> audioop-lts (Python 3.13+ compatibility)
try:
    import audioop
    from audioop import *
except ModuleNotFoundError:
    try:
        import audioop_lts as _audioop
        sys.modules['audioop'] = _audioop
        sys.modules['pyaudioop'] = _audioop
        from audioop_lts import *
    except ModuleNotFoundError:
        warnings.warn("Neither 'audioop' nor 'audioop-lts' was found. Audio processing with pydub may fail on Python 3.13+.")


