import io

import aiohttp
import discord

from bot import GUILD_ID


def get_guild(cog):
    return cog.bot.get_guild(GUILD_ID)

async def get_submission_channel(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_channel(config["submission_channel"]) if config and "submission_channel" in config else None

async def get_voting_channel(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_channel(config["voting_channel"]) if config and "voting_channel" in config else None

async def get_contest_role(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_role(config["contest_role"]) if config and "contest_role" in config else None

async def get_contest_announcement_channel(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_channel(config["contest_announcement_channel"]) if config and "contest_announcement_channel" in config else None

async def get_contest_ping_role(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_role(config["contest_ping_role"]) if config and "contest_ping_role" in config else None

async def get_contest_archive_channel(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_channel(config["contest_archive_channel"]) if config and "contest_archive_channel" in config else None

async def get_logs_channel(cog):
    guild = get_guild(cog)
    config = await cog.server_config_collection.find_one({"_id": guild.id})
    return guild.get_channel(config["logs_channel"]) if config and "logs_channel" in config else None


async def get_discord_file_from_url(url: str, filename: str = None) -> discord.File:
    """
    Downloads a file from a URL and returns a discord.File object.

    :param url: The direct URL to the file.
    :param filename: Optional custom filename. If not provided, tries to infer from URL.
    :return: discord.File object
    :raises: Exception if the file can't be downloaded
    """
    if filename is None:
        filename = url.split("/")[-1] or "file"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch file: HTTP {resp.status}")
            data = io.BytesIO(await resp.read())
            return discord.File(data, filename=filename)