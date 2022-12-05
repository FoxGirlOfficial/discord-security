import discord
from discord.ext import commands
import random
import os
import json

with open("config.json", "r") as c:
  config_data = json.load(c)

intents=discord.Intents.all()
bot = commands.Bot(debug_guilds=[config_data["guild_id"]], intents=intents)

@bot.event
async def on_ready():
  bot.add_view(MyView())
  print("Logged in.")

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None

    @discord.ui.button(label="Verify", custom_id="button-1", style=discord.ButtonStyle.primary, emoji="✅") # the button has a custom_id set
    async def button_callback(self, button, interaction):
      with open('sessions.json', 'r') as s:
        usersessions = json.load(s)
        for s in usersessions:
          if str(interaction.user.id) in s:
            user_verifying = True
          else:
            user_verifying = False
      if not user_verifying:
        global num1
        global num2
        user = interaction.user
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name=config_data['verification_category_name'])
        overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False),
                  user: discord.PermissionOverwrite(view_channel=True)}
        channel = await guild.create_text_channel(f'verify-{user.id}', category=category, overwrites=overwrites)
        with open('captchas.json', 'r') as f:
          data = json.load(f)
          num1 = random.choice(list(data[0].keys()))
          num2 = random.choice(data[1])
        with open('sessions.json', 'r') as s:
          allSessions = json.load(s)
          newSession = {str(user.id): {'first_num': num1, 'second_num': num2, 'session_channel': channel.id}}
          allSessions.append(newSession)
        with open('sessions.json', 'w') as s:
          sessionLogs = json.dumps(allSessions, indent=2)
          s.write(sessionLogs)
        embed = discord.Embed(title='Captcha', description=f'Here is your easy math problem. All you have to do is answer it correctly and you will gain access to the server.\n\n**{num1} + {num2} =**')
        await channel.send(embed=embed)
        await channel.send(user.mention, delete_after=1)
        await interaction.response.send_message("A verification channel has been created for you.", ephemeral=True)
      else:
        await interaction.response.send_message("You already have a verification channel open.", ephemeral=True)

@bot.slash_command(description='Verify for full access to the server.')
async def verify(ctx):
  embed = discord.Embed(title='Verification', description='In order to get full access to this server, you must complete a simple verification task. All you have to do is react to this message and solve an easy math problem.\n\n**By pressing this button, you confirm that you have read and agree to follow the server rules, and accept that breaking them can lead to punishments.**', color=0x922BFF)
  await ctx.send(embed=embed, view=MyView())
  
@bot.event
async def on_message(ctx):
  with open("sessions.json", 'r') as s:
    data = json.load(s)
  with open("captchas.json", 'r') as c:
    cdata = json.load(c)
  for s in data:
    if str(ctx.author.id) in s:
      if ctx.channel.id in s[str(ctx.author.id)].values():
        for key in cdata[0].keys():
          if key in s[str(ctx.author.id)].values():
            newkey = cdata[0][key]
        if int(ctx.content) == int(newkey) + s[str(ctx.author.id)]['second_num']:
          guild = ctx.author.guild
          memberrole = discord.utils.get(guild.roles, name=config_data['member_role_name'])
          await ctx.channel.send("That is correct. You are now verified.")
          await ctx.author.add_roles(memberrole)
          channel = bot.get_channel(s[str(ctx.author.id)]['session_channel'])
          await channel.delete()
          with open('sessions.json', 'r') as s:
            allsessions = json.load(s)
          with open('sessions.json', 'w') as s:
            for ses in allsessions:
              if str(ctx.author.id) in ses:
                allsessions.remove(ses)
                newsessions = json.dumps(allsessions, indent=2)
            s.write(newsessions)
        else:
          await ctx.channel.send("Sorry, that's not correct. Try again.")

bot.run(os.getenv('TOKEN'))
