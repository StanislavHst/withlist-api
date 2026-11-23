import os

from dotenv import load_dotenv

load_dotenv()
os.environ["DB_NAME"] = os.getenv("TEST_DB_NAME", "wishlist_test")
