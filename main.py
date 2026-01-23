import os

from dotenv import load_dotenv
from twitchio.ext import commands
import random

load_dotenv()

BOT_NICK = os.environ.get("BOT_NICK")
TOKEN = os.environ.get("TOKEN")
CHANNEL = os.environ.get("CHANNEL")


def to_string(array):
    if not isinstance(array, list):
        return None
    response = ""
    for entry in array:
        response += f"{entry}, "
    return response


class TirageBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="^",
            initial_channels=[CHANNEL]
        )
        self.participants = []

    # bot prêt
    async def event_ready(self):
        print(f"Connecté en tant que {self.nick}")

    # mise en place de la liste : commande format ^list Bob, Alice, Charlie
    @commands.command(name="list")
    async def set_list(self, ctx):
        if not ctx.author.is_mod and ctx.author.name != CHANNEL.lower():
            return

        content = ctx.message.content.replace("^list", "").strip()
        if not content:
            await ctx.send("❌ Liste vide.")
            return

        self.participants = [p.strip() for p in content.split(",")]
        await ctx.send(f"📋 Liste enregistrée ({len(self.participants)} participants)")

    # commande ^pick : choisit un prénom dans la liste
    @commands.command(name="pick")
    async def pick(self, ctx):
        if not self.participants:
            await ctx.send("❌ Plus personne à tirer.")
            return

        winner = random.choice(self.participants)
        self.participants.remove(winner)

        await ctx.send(
            f"🎉 Gagnant : {winner} | Restants : {len(self.participants)}"
        )

    # réinitialise la liste de participants
    @commands.command(name="reset")
    async def reset(self, ctx):
        if ctx.author.name != CHANNEL.lower() and not ctx.author.is_mod:
            return
        self.participants = []
        await ctx.send("La liste a été vidée !")

    @commands.command(name="show")
    async def show(self, ctx):
        if self.participants.__len__() == 0:
            await ctx.send("La liste est vide !")
            return

        _list = ""
        for participant in self.participants:
            _list = _list + f"{participant}, "
        await ctx.send("Liste actuelle : " + _list)

    @commands.command(name="add")
    async def add_participant(self, ctx):
        content = ctx.message.content.replace("^add", "").strip()
        participants = [p.strip() for p in content.split(",")]
        removed = ""
        if participants.__len__() == 0:
            await ctx.send("Commande incorrecte. Format : ^add Charlie, Delta")
            return
        for participant in participants:
            if participant not in self.participants:
                self.participants.append(participant)
                removed = removed + participant + ", "
        await ctx.send("Participant(s) ajouté(s) à la liste : " + removed)

    @commands.command(name="remove")
    async def remove_participant(self, ctx):
        content = ctx.message.content.replace("^remove", "").strip()
        participants = [p.strip() for p in content.split(",")]
        removed = ""
        if participants.__len__() == 0:
            await ctx.send("Commande incorrecte. Format : ^remove Alice, Bob")
            return
        for p in participants:
            if p in self.participants:
                self.participants.remove(p)
                removed = removed + p + ", "
            else:
                await ctx.send("Participant inconnu : " + p)
        await ctx.send("Participant(s) retiré(s) de la liste : " + removed)


bot = TirageBot()
bot.run()
