import aioredis
from app.utils.const import TESTING, TEST_REDIS_URL
redis = None


# add as dependency to app. if testing mode is true, create redis pool with test url
async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.from_url(TEST_REDIS_URL)
