from databases import Database
from utils.const import DB_URL, TEST_DB_URL, TESTING, IS_LOAD_TEST

# URL is determined by TESTING bool
if TESTING or IS_LOAD_TEST:
    db = Database(TEST_DB_URL)
else:
    db = Database(DB_URL)
