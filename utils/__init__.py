import motor.motor_asyncio

import config

db = motor.motor_asyncio.AsyncIOMotorClient(
    config.MONGODB_URI).get_default_database()
