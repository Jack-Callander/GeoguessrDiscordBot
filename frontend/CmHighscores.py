from src import ChromeDevice, Database
import Command
import discord
import re

class CmHighscores(Command):
    def matches_command(self, cm: str):
        return re.match("/geo highscores?$", cm)
    
    async def run_command(self, cm: str, om: discord.Message, sm: discord.Message, device: ChromeDevice, db: Database):
        if not db.record_tables:
            await sm.edit(content="*No challenges yet.*")
            return
        
        await sm.edit(content="**__Geoguessr Competitive__**")
        
        out = ""
        curr_challenge_type = -1
        curr_map_code = ""
        
        embeds = []
        for rt in sorted(db.record_tables):
            if curr_challenge_type != rt.challenge.type.value:
                curr_challenge_type = rt.challenge.type.value
                # Add the ChallengeType title (eg Point-Based:)
                out += "**" + str(rt.challenge.type) + "**\n"
            
            if curr_map_code != rt.challenge.map.code:
                curr_map_code = rt.challenge.map.code
                # Add the GeoguessrMap title (eg Diverse Complete World)
                embeds.append(discord.Embed(title=rt.challenge.map.get_print(),
                    url="https://www.geoguessr.com/maps/" + rt.challenge.map.code,
                    color=discord.Color.red()))
                embeds[-1].set_footer(text="\u2800" * 64)
                #out += self.tab + rt.challenge.map.get_print() + "\n"
                
            embeds[-1].add_field(name="\u2800" * 2 + str(rt.challenge.rules) + " - " + rt.challenge.time_limit.get_print() + "\n", value=rt.get_print_desc("\u2800" * 2), inline=False)
            #out += rt.get_print(self.tab + self.tab)
        
        for embed in embeds:
            await om.channel.send(embed=embed)