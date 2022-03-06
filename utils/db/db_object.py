from databases import Database
from utils.const import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD


db = Database(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")