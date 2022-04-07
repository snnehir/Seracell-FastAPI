JWT_SECRET_KEY = "f1dfa3870de55b287e6378ca0f7ff8381aedb1545a6a078f71bcf75875c5c795"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60*24*5

# DB
DB_HOST = "localhost"  # should be postgredb not localhost
DB_USER = "user"
DB_PASSWORD = "1234"
DB_NAME = "seracell_demo"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# REDIS
REDIS_URL = "redis://localhost"

# TEST or REAL
TESTING = False
IS_LOAD_TEST = True

# TEST DB
TEST_DB_HOST = "localhost"  # not localhost
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "test"
TEST_DB_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"

# TEST REDIS
TEST_REDIS_URL = "redis://localhost"
