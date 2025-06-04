import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()



# Environmental
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MONGO_URI = os.getenv("MONGO_URI").strip('"')


# Clients

MONGO_CLIENT = AsyncIOMotorClient(MONGO_URI)


#Timezone
SCHEDULE_TIMEZONE = ZoneInfo("Asia/Kolkata")

__all__ = [
    "DISCORD_TOKEN",
    "MONGO_CLIENT",
    "SCHEDULE_TIMEZONE"
]