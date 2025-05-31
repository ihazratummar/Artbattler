async def update_schedule(
        collection,
        guild_id: int,
        key: str,
        day: int,
        hour: int,
        minute: int,
        second: int,
):
    try:
        await collection.update_one(
            {"_id": guild_id},
            {"$set": {
                f"schedule.{key}": {
                    "day": day,
                    "hour": hour,
                    "minute": minute,
                    "second": second
                }
            }},
            upsert=True
        )
    except Exception as e:
        print(f"Error updating schedule: {e}")


async def validate_time_inputs(ctx, day: int, hour: int, minute: int, seconds: int) -> bool:
    if not isinstance(day, int) or not (1 <= day <= 31):
        await ctx.send("❌ Please enter a valid day (1–31).")
        return False
    if not isinstance(hour, int) or not (0 <= hour <= 23):
        await ctx.send("❌ Please enter a valid hour (0–23).")
        return False
    if not isinstance(minute, int) or not (0 <= minute <= 59):
        await ctx.send("❌ Please enter a valid minute (0–59).")
        return False
    if not isinstance(seconds, int) or not (0 <= seconds <= 59):
        await ctx.send("❌ Please enter a valid second (0–59).")
    return True
