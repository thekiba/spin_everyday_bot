from os import getenv

# region Load config
TOKEN = getenv("TOKEN", None)
SUPERUSER = int(getenv("SUPERUSER", 0))
# endregion

# region Check config
if TOKEN is None:
    raise ImportError("TOKEN env var is not set!")
if SUPERUSER == 0:
    raise ImportError("SUPERUSER env var is not set!")
# endregion
