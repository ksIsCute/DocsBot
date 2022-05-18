from host import run
from voltage.ext import commands
import json, voltage, asyncio, os, requests, time, datetime

async def getprefix(message, client):
  with open("json/prefixes.json", "r") as f:
    prefixes = json.load(f)
  try:
    return prefixes[message.server.id]['prefixes']
  except KeyError:
    with open("json/prefixes.json", "w") as f:
      prefixes[message.server.id] = {
        'prefixes': ["d!"]
      }
      json.dump(prefixes, f, indent=2)
    return "d!"

class HelpCommand(commands.HelpCommand):
  async def send_help(self, ctx: commands.CommandContext):
    embed = voltage.SendableEmbed(
      title="Help",
      description=f"Use `{ctx.prefix}help <command>` to get help for any of our {len(ctx.client.commands)} commands.",
      colour="#516BF2",
      icon_url=ctx.author.display_avatar.url
    )
    text = "\n### **My Commands**\n"
    for command in self.client.commands.values():
      if command.cog is None:
        text += f"> {command.name}\n"
    for i in self.client.cogs.values():
      text += f"\n### **{i.name}**\n{i.description}\n"
      for j in i.commands:
        text += f"\n> {j.name}"
    if embed.description:
      embed.description += text
    return await ctx.reply(f"[]({ctx.author.id})", embed=embed)

bot = commands.CommandsClient(getprefix, help_command=HelpCommand)
onlinesince = time.time()
@bot.listen("message")
async def count(message):
  if message.content == "<@01FZJS79PT44V3H9H7NTGGT7DR>":
    with open("json/prefixes.json", "r") as f:
      prefixes = json.load(f)
    embed = voltage.SendableEmbed(
      title = "Active Prefixes:",
      description = ', '.join(prefixes[message.server.id]["prefixes"]),
      color="#00FF00"
    )
    await message.channel.send(content="[]()", embed=embed)
  await bot.handle_commands(message)

@bot.command()
async def addprefix(ctx, prefix:str):
  if ctx.author.permissions.manage_server:
    if ctx.server is None:
      return await ctx.reply("Custom prefixes are only available in servers.")
    with open("json/prefixes.json", "r") as f:
      data = json.load(f)
    if prefix in data[ctx.server.id]['prefixes']:
      return await ctx.reply(f"You already have that prefix in your list of `{len(data[ctx.server.id]['prefixes'])}`!")
    with open("json/prefixes.json", "w") as f:
      data[ctx.server.id]['prefixes'].append(prefix)
      json.dump(data, f, indent=2)
    await ctx.reply(f"Added `{prefix}` to your current list of {len(data[ctx.server.id]['prefixes'])} prefixes!")
  else:
    await ctx.send("You dont have the required permission `manage_server` for this command!")

@bot.command()
async def delprefix(ctx, prefix:str):
  if ctx.author.permissions.manage_server:
    if ctx.server is None:
      return await ctx.reply("Custom prefixes are only available in servers.")
    with open("json/prefixes.json", "r") as f:
      data = json.load(f)
  
    if len(data[ctx.server.id]['prefixes']) == 1:
      return await ctx.reply("Sorry, you only have `ONE` prefix! Meaning that removing your only prefix, renders this bot useless!")
    elif prefix not in data[ctx.server.id]['prefixes']:
      return await ctx.reply(f"Prefix `{prefix}` doesnt exist! You have to remove a prefix from your prefix array (shown below)\n\n`{','.join(data[ctx.server.id]['prefixes'])}`")
    with open("json/prefixes.json", "w") as f:
      data[ctx.server.id]['prefixes'].remove(prefix)
      json.dump(data, f, indent=2)
    await ctx.reply(f"Removed `{prefix}` from this servers prefixes.")
  else:
    await ctx.reply("You dont have the required permission `manage_server` for this command!")

@bot.listen("ready")
async def on_ready():
  serverarray = []
  for i in bot.servers:
    serverarray.append(i.name.lower().capitalize())
  with open("json/prefixes.json", "r") as h:
    prefixes = json.load(h)
  for i in bot.servers:
    prefixes[i.id] = {
      "name": i.name,
      "prefixes": ["d!", "docs!"]
    }
  with open("json/prefixes.json", "w") as h:
    json.dump(prefixes, h, indent=2)
  with open("json/data.json", "r") as f:
    data = json.load(f)
  with open("json/data.json", "w") as f:
    data['Docs'] = {
      "server": {
        "count":len(bot.servers), 
        "servers": serverarray
      },
      "users": len(bot.users)
    }
    json.dump(data, f, indent=2)
  with open("json/data.json", "w") as f:
    for server in bot.servers:
      if server.name.lower().capitalize() in data:
        pass
      else:
        print(f"added server {server.name}")
        channellist = []
        for channel in server.channels:
            #print(dir(bot.cache.members[server.id]["01FZJS79PT44V3H9H7NTGGT7DR"].permissions))
            try:
              if "textchannel" in str(channel).lower():
                channellist.append(f"{channel.name} - {channel.id}")
              else:
                pass
              
              data[server.name.lower().capitalize()] = {
                "channels": channellist,
                "id": server.id,
                "sendable": {
                  "message": "None Yet",
                  "sentmessage": "None Yet",
                  "channel": "Channel ID Not Yet"
                }
              }
            except Exception as e:
              print(e)
              pass
          #else:
            #print(f"dont have perms for {channel.name}")
    json.dump(data, f, indent=2)
  print("online")

@bot.command()
async def asd(ctx):
  await ctx.reply("hi")

@bot.command()
async def send(ctx):
  await ctx.send("Sending messages..")
  with open("json/data.json", "r") as f:
    data = json.load(f)
  for server in bot.servers:
    if data[server.name.lower().capitalize()]['sendable']['message'] == data[server.name.lower().capitalize()]['sendable']['sentmessage']:
        pass
    else:
      data[server.name.lower().capitalize()]['sendable']['sentmessage'] = data[server.name.lower().capitalize()]['sendable']['message']
      channel = bot.get_channel(data[server.name.lower().capitalize()]['sendable']['channel'])
      embed = voltage.SendableEmbed(
        title = "Sent from Send-A-Message",
        description = data[server.name.lower().capitalize()]['sendable']['message'],
        color = "#00FF00"
      )
      await channel.send(content="[]()", embed=embed)
  with open("json/data.json", "w") as f:
    json.dump(data, f, indent=2)
  await ctx.send("Sent all messages!")

@bot.command()
async def thing(ctx):
  await ctx.send("Running loop")
  for i in range(1, 10000):
    print(i)
    with open("json/data.json", "r") as f:
      data = json.load(f)
    for server in bot.servers:
      if data[server.name.lower().capitalize()]['sendable']['message'] == data[server.name.lower().capitalize()]['sendable']['sentmessage']:
          pass
      else:
        data[server.name.lower().capitalize()]['sendable']['sentmessage'] = data[server.name.lower().capitalize()]['sendable']['message']
        channel = bot.get_channel(data[server.name.lower().capitalize()]['sendable']['channel'])
        embed = voltage.SendableEmbed(
          title = "Sent from Send-A-Message",
          description = data[server.name.lower().capitalize()]['sendable']['message'],
          color = "#00FF00"
        )
        try:
          await channel.send(content="[]()", embed=embed)
        except Exception as e:
          print(f"no perms or channel doesnt exist {channel.name}")
          print(e)
    with open("json/data.json", "w") as f:
      json.dump(data, f, indent=2)
    await asyncio.sleep(5)
  await ctx.send("Loop ended!")

@bot.command()
async def dashboard(ctx):
  await ctx.reply("[there is a dashboard in progress here!](https://flaskmsgsendthing.ksiscute.repl.co/dashboard)")

@bot.command()
async def test(ctx, user: voltage.User):
  link = requests.get(url=f"https://api.revolt.chat/users/{user.id}", headers={"x-session-token": "wK4XdZfvQrc4mA_DhwHcxtCLcj5OOLf4dtO7uOu0AzHxjWONviF0D6-Ue98N4qUk"})
  print(link.json()['username'])
  await ctx.reply(f"`{link.json()['username']}`")

@bot.command()
async def createacc(ctx, password:str, email:str):
  #link = requests.post(url=f"https://api.revolt.chat/auth/account/create", headers={"Content-Type": "application/json"}, data={"email": email, "password": password})
  linka = {"no": ":trol:"}
  print(linka.json())
  await ctx.reply(f"no `{linka['no']}`")

@bot.command()
async def uptime(ctx):
  await ctx.reply(f"`{str(datetime.timedelta(seconds=int(round(time.time() - onlinesince))))}`")

@bot.command()
async def userinfo(ctx, user: voltage.User):
  print(user.created_at)
  print(time.time())
  print(datetime.datetime.now())
  print(datetime.timedelta(seconds=user.created_at - time.time()))

@bot.command()
async def typing(ctx):
  await bot.user.start_typing
  await asyncio.sleep(2)
  await bot.user.end_typing

run()
bot.run(os.environ['token'])