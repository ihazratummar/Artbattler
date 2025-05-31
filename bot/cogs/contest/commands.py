import discord
from discord.ext import commands

from bot.cogs.contest.utils import get_logs_channel
from bot.core.error_embed import create_logs_embed
from bot.utils.update_schedule import validate_time_inputs, update_schedule


class ContestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = self.bot.db["ServerConfig"]

    @commands.hybrid_command(name="contest_submission_channel", description="Select submission channel")
    @commands.has_permissions(administrator=True)
    async def contest_submission_channel(self, ctx: commands.Context, *, channel: discord.TextChannel = None):
        await ctx.defer()

        logs_channel = await get_logs_channel(self.bot, guild_id=ctx.guild.id)
        if logs_channel:
            logs_embed = create_logs_embed(
                title="Submission channel set",
                description=f"Submission channel set to <#{channel.id}>" if channel else "Submission channel unset",
                color=discord.Color.green() if channel else discord.Color.red()
            )
            await logs_channel.send(
                embed=logs_embed
            )

        if channel is None:
            channel = ctx.channel

        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"submission_channel": channel.id}},
                upsert=True)
            await ctx.send(f"<#{channel.id}> is set as submission channel")
        except Exception as e:
            if logs_channel:
                await logs_channel.send(
                    embed=create_logs_embed(
                        title="Error setting submission channel",
                        description=f"Error: {e}",
                        color=discord.Color.red()
                    )
                )
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="contest_voting_channel", description="Select voting channel")
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
                    bot_member: discord.PermissionOverwrite(view_channel=True, manage_channels=True, send_messages=True,
                                                            manage_threads=True, read_message_history=True),
                    role: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                      send_messages=False),
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False, read_message_history=False,
                                                                        send_messages=False)
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
    @commands.has_permissions(administrator=True)
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

    @commands.hybrid_command(name="contest_logs_channel", description="Select bot log channel")
    @commands.has_permissions(administrator=True)
    async def contest_logs_channel(self, ctx: commands.Context, *, channel: discord.TextChannel = None):
        await ctx.defer()
        if channel is None:
            channel = ctx.channel

        if not isinstance(channel, discord.TextChannel):
            await ctx.send("Please select a valid text channel for bot log.")
            return

        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"contest_logs_channel": channel.id}},
                upsert=True)
            await ctx.send(f"<#{channel.id}> is set as bot log channel")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name="contest_create_channel", description="Create contest channel")
    @commands.has_permissions(administrator=True)
    async def contest_create_channel(self, ctx: commands.Context):
        await ctx.defer()
        guild = ctx.guild
        if "NEWS" not in guild.features:
            await ctx.send("⚠️ This server must be a Community Server to create announcement channels.")
            return

        bot_member = guild.me
        server_config = await self.collection.find_one({"_id": guild.id})

        # Create base permission overwrites
        default_overwrites = {
            bot_member: discord.PermissionOverwrite(
                view_channel=True,
                manage_channels=True,
                send_messages=True,
                manage_threads=True,
                read_message_history=True
            ),
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False,
                send_messages=False,
                create_public_threads=False,
                create_private_threads=False
            )
        }

        contest_category = discord.utils.get(guild.categories, name="Contest")
        if contest_category is None:
            try:
                contest_category = await guild.create_category("Contest", overwrites=default_overwrites)
            except discord.Forbidden:
                print(f"Bot does not have permission to create category{discord.Forbidden}")
                return
            # ✅ Ensure bot has manage permission on the category
        try:
            await contest_category.set_permissions(
                bot_member,
                overwrite=discord.PermissionOverwrite(
                    manage_channels=True,
                    view_channel=True,
                    send_messages=True,
                    manage_threads=True,
                    read_message_history=True
                )
            )
        except Exception as e:
            print(f"❌ Could not update category permissions for bot: {e}")

        contest_role = guild.get_role(server_config.get("contest_role")) if server_config else None
        print(f"Contest role: {contest_role}")

        view_only_overwrite = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=True,
                read_message_history=True,
                send_messages=False
            )
        }

        print(f"View only overwrite: {view_only_overwrite}")

        async def get_or_create_role(name):
            return discord.utils.get(guild.roles, name=name) or await guild.create_role(name=name)

        # Handle ping role
        ping_role = await get_or_create_role("Contest Ping")

        async def get_or_create_channel(name, cls, reason, is_news=False, extra_overwrite=None,
                                        inactivity_timeout=None):
            existing = discord.utils.get(guild.channels, name=name)
            if existing:
                return existing

            # Start with default overwrites
            overwrites = {**default_overwrites}  # Safe copy

            # Safely add extra overwrites, skipping any roles above bot
            if extra_overwrite:
                for role, perms in extra_overwrite.items():
                    if isinstance(role, discord.Role) and role.position >= guild.me.top_role.position:
                        print(f"⚠️ Skipping overwrite for {role.name} due to role hierarchy (bot role too low).")
                        continue
                    overwrites[role] = perms

            # ✅ Ensure bot's permissions are applied last and preserved
            overwrites[bot_member] = discord.PermissionOverwrite(
                view_channel=True,
                manage_channels=True,
                send_messages=True,
                manage_threads=True,
                read_message_history=True
            )

            try:
                if cls == discord.TextChannel:
                    return await guild.create_text_channel(
                        name,
                        category=contest_category,
                        reason=reason,
                        overwrites=overwrites,
                        news=is_news
                    )

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

            except discord.Forbidden:
                print(
                    f"❌ Bot does not have permission to create {cls.__name__}: Missing permissions or role hierarchy issue.")
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

        # ✅ Reorder channels inside the category
        channels = [
            announcement_channel,
            voting_channel,
            submission_channel,
            contest_archive_channel,
            logs_channel
        ]

        for index, channel in enumerate(channels):
            if channel and channel.category_id == contest_category.id:
                try:
                    await channel.edit(position=index)
                except Exception as e:
                    print(f"Error setting position for {channel.name}: {e}")

        # Save everything to DB
        try:
            await self.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {
                    "submission_channel": submission_channel.id,
                    "voting_channel": voting_channel.id,
                    "contest_announcement_channel": announcement_channel.id,
                    "contest_archive_channel": contest_archive_channel.id,
                    "contest_logs_channel": logs_channel.id,
                    "contest_ping_role": ping_role.id
                }},
                upsert=True
            )
            await ctx.send("✅ Contest channels created successfully.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.hybrid_command(name="set_submission_open_time", description="Set submission time")
    @commands.has_permissions(administrator=True)
    async def set_submission_open_time(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="open_submission", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Submission time set successfully.\n➡️ Now set when to ** close the submission channel** using `/set_close_submission_time`.",
            ephemeral=True)

    @commands.hybrid_command(name="set_close_submission", description="Set time for submission close time")
    @commands.has_permissions(administrator=True)
    async def set_close_submission(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="close_submission", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Close submission time updated.\n➡️ Next, set the **post to forum** time using `/set_post_to_forum_time`.",
            ephemeral=True
        )

    @commands.hybrid_command(name="set_post_to_forum", description="Set time for posting submissions to forum")
    @commands.has_permissions(administrator=True)
    async def set_post_to_forum(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="post_submission", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Post to forum time updated.\n➡️ Next, set the **open voting** time using `/set_open_voting_time`.",
            ephemeral=True
        )

    @commands.hybrid_command(name="set_open_voting", description="Set time for opening voting")
    @commands.has_permissions(administrator=True)
    async def set_open_voting(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="open_voting", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Open voting time updated.\n➡️ Now set the **close voting** time using `/set_close_voting_time`.",
            ephemeral=True
        )

    @commands.hybrid_command(name="set_close_voting_time", description="Set time for closing voting")
    @commands.has_permissions(administrator=True)
    async def set_close_voting_time(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="close_voting", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Close voting time updated.\n➡️ Next, set the **announce winner** time using `/set_announce_winner_time`.",
            ephemeral=True
        )

    @commands.hybrid_command(name="set_announce_winner_time", description="Set time for announcing the winner")
    @commands.has_permissions(administrator=True)
    async def set_announce_winner_time(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="announce_winner", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Announce winner time updated.\n➡️ Lastly, set the **close contest** time using `/set_close_contest_time`.",
            ephemeral=True
        )

    @commands.hybrid_command(name="set_close_contest_time", description="Set time for closing the contest")
    @commands.has_permissions(administrator=True)
    async def set_close_contest_time(self, ctx: commands.Context, day: int, hour: int, minute: int, seconds: int = 0):
        if not await validate_time_inputs(ctx=ctx, day=day, hour=hour, minute=minute, seconds=seconds):
            return

        await update_schedule(collection=self.collection, key="close_contest", guild_id=ctx.guild.id, day=day,
                              hour=hour, minute=minute, second=seconds)
        await ctx.send(
            "✅ Close contest time updated.\n🎉 All contest timings are now configured! You’re ready to go!",
            ephemeral=True
        )

    @commands.hybrid_command(name="help", description="Get bot's guild id")
    async def help(self, ctx: commands.Context):

        embed = discord.Embed(
            title="👋 Welcome to Contest Bot!",
            description=(
                "Here’s how to get started with your monthly contest setup:\n\n"
                "**1️⃣ `/create_contest_channel`** – Create the channel where users submit entries.\n"
                "**2️⃣ `/contest_role`** – Set the role to be notified for contest events.\n"
                "**3️⃣ `/set_submission_open_time`** – Set when submissions should open.\n"
                "**4️⃣ `/set_close_submission_time`** – Set when submissions should close.\n"
                "**5️⃣ `/set_post_to_forum_time`** – When to post entries to the forum.\n"
                "**6️⃣ `/set_voting_open_time`** – When the voting channel opens.\n"
                "**7️⃣ `/set_voting_close_time`** – When voting ends.\n"
                "**8️⃣ `/set_announce_winner_time`** – When to announce the winner.\n"
                "**9️⃣ `/set_contest_close_time`** – When the entire contest ends.\n\n"
                "✅ Once these are set, the bot will take care of everything monthly!"
            ),
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
