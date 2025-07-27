from discord.ext import commands

def setup_bot_commands(bot, messages_by_channel):
    @bot.command(name="send_daily_summary")
    async def send_daily_summary(ctx):
        await ctx.send("Résumé envoyé.")
