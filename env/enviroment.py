import os

from dotenv import load_dotenv


load_dotenv()


class Env:
    host = os.getenv("host")
    db_name = os.getenv("db_name")
    user = os.getenv("user")
    password = os.getenv("password")
    port = os.getenv("port")