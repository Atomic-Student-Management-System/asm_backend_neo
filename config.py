import os

import dotenv

dotenv.load_dotenv()

MONGODB_URI = os.environ['MONGODB_URI']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
