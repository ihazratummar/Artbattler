from datetime import datetime

import discord
from discord.ext import commands

from bot import GMT_TIMEZONE
from bot.cogs.contest.jobs import ContestJobs
from bot.cogs.contest.utils import get_submission_channel
from bot.config import Bot
from bot.utils.image_utils import resize_and_save_image


class ContestManager(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.server_config_collection = bot.db["ServerConfig"]
        self.jobs = ContestJobs(cog=self)
        self.jobs.schedule_job()

    async def track_image_upload(self, message: discord.Message):
        submission_channel = await get_submission_channel(self)
        if message.channel.id != submission_channel.id or not message.attachments:
            return
        user_id = message.author.id
        attachment = message.attachments[0]
        current_month = datetime.now(GMT_TIMEZONE).strftime("%Y-%m")

        submissions = self.bot.db.submissions

        image_bytes = await  attachment.read()
        output_path = f"bot/data/submissions/{str(user_id)}.webp"
        await resize_and_save_image(image_bytes, output_path)
        print(f"Saved image for {user_id} at {output_path}")

        await submissions.delete_many({"user_id":user_id, "month": current_month})
        await submissions.insert_one({
            "user_id": user_id,
            "month": current_month,
            "file_path": output_path,
            "message_id": message.id,
            "guild_id": message.guild.id
        })
