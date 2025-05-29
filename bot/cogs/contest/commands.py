import discord
from discord.ext import commands


class ContestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = self.bot.db["ServerConfig"]

    @commands.hybrid_command(name="contest_submission_channel", description="Select submission channel")
    @commands.has_permissions(administrator=True)
    async def contest_submission_channel(self, ctx: commands.Context, *, channel: discord.TextChannel = None):
        await ctx.defer()
        if channel is None:
            channel = ctx.channel

        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"submission_channel": channel.id}},
                upsert=True)
            await ctx.send(f"<#{ctx.channel.id}> is set as submission channel")
        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.hybrid_command(name = "contest_voting_channel", description = "Select voting channel")
    @commands.has_permissions(administrator=True)
    async def contest_voting_channel(self, ctx: commands.Context, *, channel: discord.ForumChannel = None):
        await ctx.defer()
        if channel is None:
            channel = ctx.channel

        if not isinstance(channel, discord.ForumChannel):
            await ctx.send("Please select a valid forum channel for voting.")
            return

        try:
            update = await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"voting_channel": channel.id}},
                upsert=True
            )
            if update.modified_count == 0:
                await ctx.send(f"Voting channel already set to <#{channel.id}>")
            else:
                await ctx.send(f"<#{channel.id}> is set as voting channel")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="contest_role", description="Select contest role")
    @commands.has_permissions(administrator=True)
    async def contest_role(self, ctx: commands.Context, *, role: discord.Role = None):
        await ctx.defer()
        if role is None:
            await ctx.send("Please specify a role.")
            return
        if not isinstance(role, discord.Role):
            await ctx.send("Please select a valid role.")
            return

        bot_member = ctx.guild.me

        server_config = await self.collection.find_one({"_id": ctx.guild.id})
        announcement_channel = ctx.guild.get_channel(server_config.get("contest_announcement_channel"))
        if announcement_channel:
            if role not in announcement_channel.overwrites:
                overwrites = {
                    role: discord.PermissionOverwrite(view_channel=True, read_message_history=True,send_messages=False),
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False, read_message_history=False, send_messages=False),
                    bot_member: discord.PermissionOverwrite(view_channel=True, manage_channels=True, send_messages=True, manage_threads=True, read_message_history=True)
                }
                await announcement_channel.edit(overwrites=overwrites)
            else:
                print("role already in announcement channel")


        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"contest_role": role.id}},
                upsert=True)
            await ctx.send(f"{role.mention} is set as contest role")
        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.hybrid_command(name="contest_announcement_channel", description="Select announcement channel")
    @commands.has_permissions(administrator=True)
    async def contest_announcement_channel(self, ctx: commands.Context, *, channel: discord.TextChannel = None):
        await ctx.defer()
        if channel is None:
            channel = ctx.channel

        if not isinstance(channel, discord.TextChannel):
            await ctx.send("Please select a valid text channel for announcement.")
            return

        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"contest_announcement_channel": channel.id}},
                upsert=True
            )
            await ctx.send(f"<#{channel.id}> is set as announcement channel")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="contest_ping_role", description="Select contest ping role")
    @commands.has_permissions(administrator= True)
    async def contest_ping_role(self, ctx: commands.Context, *, role: discord.Role = None):
        await ctx.defer()
        if role is None:
            await ctx.send("Please specify a role.")
            return
        if not isinstance(role, discord.Role):
            await ctx.send("Please select a valid role.")
            return
        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"contest_ping_role": role.id}},
                upsert=True
            )
            await ctx.send(f"{role.mention} is set as contest ping role")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="contest_archive_channel", description="Select art archive channel")
    @commands.has_permissions(administrator=True)
    async def contest_archive_channel(self, ctx: commands.Context, *, channel: discord.ForumChannel = None):
        await ctx.defer()
        if channel is None:
            channel = ctx.channel

        if not isinstance(channel, discord.ForumChannel):
            await ctx.send("Please select a valid forum channel for art archive.")
            return

        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"contest_archive_channel": channel.id}},
                upsert=True)
            await ctx.send(f"<#{channel.id}> is set as art archive channel")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="logs_channel", description="Select bot log channel")
    @commands.has_permissions(administrator=True)
    async def logs_channel(self, ctx: commands.Context, *, channel: discord.TextChannel = None):
        await ctx.defer()
        if channel is None:
            channel = ctx.channel

        if not isinstance(channel, discord.TextChannel):
            await ctx.send("Please select a valid text channel for bot log.")
            return

        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"logs_channel": channel.id}},
                upsert=True)
            await ctx.send(f"<#{channel.id}> is set as bot log channel")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="contest_create_channel", description="Create contest channel")
    @commands.has_permissions(administrator=True)
    async def contest_create_channel(self, ctx: commands.Context):
        await ctx.defer()
        guild = ctx.guild

        if "FEATURE" and "NEWS" not in guild.features:
            await ctx.send("Enable community features to use this command.")
            return

        bot_member = guild.me
        server_config = await self.collection.find_one({"_id": guild.id})

        # Create base permission overwrites
        default_overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False,
                send_messages=False,
                create_public_threads=False,
                create_private_threads=False
            ),
            bot_member: discord.PermissionOverwrite(
                view_channel=True,
                manage_channels=True,
                send_messages=True,
                manage_threads=True,
                read_message_history=True
            )
        }

        # Create or get "Contest" category
        contest_category = discord.utils.get(guild.categories, name="Contest")
        if contest_category is None:
            contest_category = await guild.create_category("Contest", overwrites=default_overwrites)


        contest_role = guild.get_role(server_config.get("contest_role")) if server_config else None

        # If contest_role exists, give it special permissions
        view_only_overwrite = {
            contest_role or guild.default_role: discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False
            )
        }

        async def get_or_create_role(name):
            return discord.utils.get(guild.roles, name=name) or await guild.create_role(name=name)

        # Handle ping role
        ping_role = await get_or_create_role("Contest Ping")

        async def get_or_create_channel(name, cls, reason, is_news=False, extra_overwrite=None,
                                        inactivity_timeout=None):
            existing = discord.utils.get(guild.channels, name=name)
            if existing:
                return existing

            # Start with default category overwrites
            overwrites = default_overwrites.copy()
            if extra_overwrite:
                overwrites.update(extra_overwrite)

            if cls == discord.TextChannel:
                return await guild.create_text_channel(name, category=contest_category, reason=reason,
                                                       overwrites=overwrites, news=is_news)
            elif cls == discord.ForumChannel:
                kwargs = {
                    "category": contest_category,
                    "reason": reason,
                    "default_layout": discord.ForumLayoutType.gallery_view,
                    "overwrites": overwrites
                }
                if inactivity_timeout:
                    kwargs["default_auto_archive_duration"] = inactivity_timeout
                return await guild.create_forum(name, **kwargs)
            return None

        # Create all needed channels
        submission_channel = await get_or_create_channel("contest-submit", discord.TextChannel, "Submission channel")
        voting_channel = await get_or_create_channel("contest-vote", discord.ForumChannel, "Voting channel",
                                                     inactivity_timeout=10080)
        announcement_channel = await get_or_create_channel("contest-announcement", discord.TextChannel,
                                                           "Announcement channel", extra_overwrite=view_only_overwrite,
                                                           is_news=True)
        contest_archive_channel = await get_or_create_channel("contest-archive", discord.ForumChannel,
                                                              "Contest archive channel")
        logs_channel = await get_or_create_channel("bot-logs", discord.TextChannel, "Bot log channel")

        # Save everything to DB
        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {
                    "submission_channel": submission_channel.id,
                    "voting_channel": voting_channel.id,
                    "contest_announcement_channel": announcement_channel.id,
                    "contest_archive_channel": contest_archive_channel.id,
                    "logs_channel": logs_channel.id,
                    "contest_ping_role": ping_role.id
                }},
                upsert=True
            )
            await ctx.send("✅ Contest channels created successfully.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")


