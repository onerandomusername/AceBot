from datetime import datetime
from typing import Union

import disnake
import sqlalchemy as sa
from disnake.ext import commands

from ace import AceBot
from cogs.mixins import AceMixin
from models.logging import CommandType, Log as LogRecord
from utils.context import AceContext
from utils.string import po


class InternalLogger(commands.Cog, AceMixin):
    @commands.Cog.listener()
    async def on_command(self, ctx: Union[AceContext, disnake.Interaction]):
        spl = ctx.message.content.split("\n")
        self.bot.log.info(
            "%s in %s: %s",
            po(ctx.author),
            po(ctx.guild),
            spl[0] + (" ..." if len(spl) > 1 else ""),
        )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: AceContext):
        async with self.bot.db_session() as session:
            record = LogRecord(
                ctx.guild.id,
                ctx.channel.id,
                ctx.author.id,
                datetime.utcnow(),
                ctx.command.qualified_name,
                CommandType.PREFIX,
            )
            session.add(record)
            await session.commit()

    @commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.ApplicationCommandInteraction):
        async with self.bot.db_session() as session:
            record = LogRecord(
                inter.guild_id,
                inter.channel_id,
                inter.author.id,
                datetime.utcnow(),
                inter.application_command.qualified_name,
                CommandType.APPLICATION,
            )
            session.add(record)
            await session.commit()


def setup(bot: AceBot):
    bot.add_cog(InternalLogger(bot))
