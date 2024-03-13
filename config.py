import datetime
import os

import dotenv

dotenv.load_dotenv()

MONGODB_URI = os.environ['MONGODB_URI']
DATABASE_NAME = os.environ['DATABASE_NAME']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

APIKEY_EXPIRY = datetime.timedelta(minutes=1)
