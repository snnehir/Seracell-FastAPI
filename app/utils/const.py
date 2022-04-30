JWT_SECRET_KEY = "f1dfa3870de55b287e6378ca0f7ff8381aedb1545a6a078f71bcf75875c5c795"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60*24*5
JWT_EXPIRED_MESSAGE = "Your JWT token is expired!"
JWT_INVALID_MESSAGE = "Invalid JWT token!"
JWT_UNAUTHORIZED_ROLE = "Unauthorized role!"
TOKEN_INVALID_MATCH_MESSAGE = "Invalid username - password match!"

# DB
DB_HOST = "postgres"  # host should be container name (depends_on) not "localhost" (compose up)
DB_USER = "user"
DB_PASSWORD = "password"
DB_NAME = "seracell_demo_db"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# REDIS
REDIS_URL = "redis://redis"     # redis host also should be container name (compose up)

# TEST or REAL
TESTING = False
IS_LOAD_TEST = False

# TEST DB
TEST_DB_HOST = "localhost"  # not localhost
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "test"
TEST_DB_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"

# TEST REDIS
TEST_REDIS_URL = "redis://localhost"
