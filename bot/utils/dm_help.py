async def dm_help_guide(guild, discord):
    # Try to DM the server owner or first admin found
    target = guild.owner
    if target is None or not target.dm_channel:
        for member in guild.members:
            if member.guild_permissions.administrator and not member.bot:
                target = member
                break

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
    embed.set_footer(text="Need help? Use /help or ping the bot!")

    try:
        await target.send(embed=embed)
    except discord.Forbidden:
        print(f"[!] Couldn't send setup DM to {target} in {guild.name}.")