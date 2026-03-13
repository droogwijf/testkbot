import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from utils.views import WarningView

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("moderation.apply")
        await self.load_extension("moderation.automod")
        await self.load_extension("moderation.history")
        await self.load_extension("moderation.kick")
        await self.load_extension("moderation.mutes")
        await self.load_extension("moderation.warns")

        self.add_view(WarningView(self.get_cog("Warnings")))

        solli_cog = self.get_cog("SollicitatiePanel")
        if solli_cog:
            from moderation.apply import SollicitatieButtons

            self.add_view(SollicitatieButtons(solli_cog))

        MY_GUILD = discord.Object(id=int(GUILD_ID))
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def on_command_error(self, ctx, error):
        """Voorkomt dat commando's van andere bots je terminal vervuilen."""
        if isinstance(error, commands.CommandNotFound):
            return
        print(f"⚠️ Commando Fout: {error}")

    async def on_ready(self):
        os.system("cls" if os.name == "nt" else "clear")
        GRAY, CYAN, GREEN, BLUE, WHITE, BOLD, END = (
            "\033[90m",
            "\033[96m",
            "\033[92m",
            "\033[94m",
            "\033[97m",
            "\033[1m",
            "\033[0m",
        )

        await self.change_presence(
            activity=discord.Game(name="📝 • Beheert sollicitaties")
        )

        print(f"{BLUE}{BOLD}=" * 50)
        print(f"{CYAN}{BOLD}                    MeneerKBot")
        print(f"{BLUE}{BOLD}=" * 50 + f"{END}")
        print(f"{WHITE} Status:       {GREEN}🟢  Online")
        print(f"{WHITE} Gebruiker:    {BOLD}{self.user.name}")
        print(f"{WHITE} Servers:      {BOLD}{len(self.guilds)}")
        print(f"{BLUE}{BOLD}" + "-" * 50 + f"{END}")

        print(f"{CYAN}{BOLD} Geladen Slash Commands:{END}")

        all_cmds = self.tree.get_commands(guild=discord.Object(id=int(GUILD_ID)))

        if all_cmds:
            for cmd in all_cmds:
                if isinstance(cmd, app_commands.Group):
                    for sub in cmd.commands:
                        print(f"{GRAY} > {WHITE}/{cmd.name} {sub.name}{END}")
                else:
                    print(f"{GRAY} > {WHITE}/{cmd.name}{END}")
        else:
            print(f"{GRAY} > Geen guild-commands gevonden.{END}")

        print(f"{BLUE}{BOLD}=" * 50 + f"{END}")


bot = MyBot()
bot.run(TOKEN)
