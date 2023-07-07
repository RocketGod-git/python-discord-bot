import discord
from discord.ext import commands
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

# Variables
BOT_TOKEN = 'your-bot-token'
CHANNEL_ID = 1234567890  # Replace with your channel ID

# Initialize bot with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info('Bot has started up.')
    await bot.get_channel(CHANNEL_ID).send('Bot has started up.')

@bot.command(name='py', help='Run a Python eval command. Demonstrates the dangers of unsanitized input.')
async def _py(ctx, *, command: str):
    # Ignore DMs
    if ctx.guild is None:
        logging.info('Command ignored, was a DM.')
        return

    # Ensure command is run in the designated channel
    if ctx.channel.id != CHANNEL_ID:
        logging.info('Command attempted in wrong channel.')
        await ctx.send('This command can only be run in the designated bot channel.')
        return

    logging.info(f'Running command: {command}')
    try:
        # Capture the output of print() statements
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        # Dangerously evaluate the command
        exec(command)

        # Get the output and restore the old stdout
        sys.stdout = old_stdout
        result = redirected_output.getvalue().strip()

        # Send the result back to the channel
        logging.info(f'Command result: {result}')
        await ctx.send(f'Result: {result}')

    except Exception as e:
        # If an error occurred, send back the error message
        logging.error(f'Error running command: {str(e)}')
        await ctx.send(f'An error occurred: {str(e)}')

# Run the bot in a loop to handle exceptions and restart
while True:
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}, restarting bot.')