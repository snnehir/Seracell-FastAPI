from databases import Database
from utils.const import DB_URL, TEST_DB_URL, TESTING

# URL is determined by TESTING bool
if TESTING:
    db = Database(TEST_DB_URL)
else:
    db = Database(DB_URL)
