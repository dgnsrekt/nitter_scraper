from decouple import config

NITTER_URL = config("NITTER_URL", default="https://nitter.net", cast=str)
