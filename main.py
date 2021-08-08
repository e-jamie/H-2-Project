import discord
from discord.ext import commands
from numpy import random
import json
import pandas as pd

intents = discord.Intents.default()
intents.members = True

help_command = commands.DefaultHelpCommand(no_category = 'Command list', ending_note = 'Always in service, whenever and wherever.')

client = commands.Bot(command_prefix='MEA ', intents=intents, help_command = help_command)

@client.event
async def on_ready():
    print('Bot is ready, whenever & wherever.')

@client.command(brief='Returns the time delay between you and MEA Bot.')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(brief='Randomized questions to break the ice.')
async def icebreakers(ctx):
    icebreakers_list = ['What is your ulam?',
                        'What animal would you want to be?',
                        'If you could meet anyone, living or dead, who would it be?',
                        'Why is ITM your favorite subject?',
                        'So, do you like Messi?',
                        'Is a hotdog a sandwich?',
                        'What is your favorite electric fan number?',
                        'How many holes does a straw have?',
                        'When a bar of soap falls on the floor, will the soap become dirty or will the floor become clean?',
                        'What is the best piece of advice you have ever been given?',
                        'What do you want to be remembered for?',
                        'Pineapples on pizza: yes or no?',
                        '"prih-mer" or "pry-mer"?'
                        ]
    await ctx.send(icebreakers_list[random.randint(0, len(icebreakers_list))])

@client.command(aliases=['8ball', 'test'],brief='Let 8ball see into your future.')
async def _8ball(ctx, *, question):
    responses = ['It is certain',
                 'It is decidedly so',
                 'Without a doubt',
                 'Chums approved',
                 'You may rely on it',
                 'As I see it, yes',
                 'Most likely',
                 'Outlook good',
                 'Yes',
                 'Signs point to yes',
                 'Reply hazy, try again',
                 'Ask again later',
                 'Better not tell you now',
                 'Cannot predict now',
                 'Concentrate and think again',
                 "Don't count on it",
                 'My reply is no',
                 'My sources say no',
                 'Outlook is not so good',
                 'Very doubtful',
                 'Indubitably',
                 'Lyka likes it.',
                 'Haha. No.',
                 'Not a chance bro.',
                 'Jamil says yes, assuming Jego does also.',
                 "If you'll join a project, then yes sure."
                ]

    await ctx.send(f'Question: {question}\nAnswer: {responses[random.randint(0, len(responses))]}')

@client.command(brief='Get the MEA website link to any department.')
async def tellme(ctx, *, info):
    with open('mea_data.json', 'r') as mea_master:
        mea_data = json.loads(mea_master.read())
    if info.split()[0] not in mea_data:
        await ctx.send(f"The category you're looking for cannot be found, please use these categories below:\n{mea_data.keys()}")
    elif info.upper().split()[1] not in mea_data[info.split()[0]]:
        await ctx.send(f"We cannot find the {info.split()[0]} you're looking for, maybe you're looking for these:\n{mea_data[info.split()[0]].keys()}")
    else:
        await ctx.send(mea_data[info.split()[0]][info.upper().split()[1]])

@client.command(brief='Check the schedule of a MEA Project.')
async def timeline(ctx, *, project):
    sheet_id = '1kWSiOa7W-KFhgISUPE99Wwbdz2LgocMLNPES0S-J680'
    df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
    projlist = (df['Project']).to_list()
    projstring = ((df['Project']).to_string(index=False))
    userproj = project.split()[0]
    userproj = userproj.upper()
    if userproj not in projlist:
        await ctx.send(f'This project is not part of the timeline. Try these: {projstring}.')
    else:
        row = df[df['Project'] == userproj].index[0]
        sched = df.iloc[row]['Schedule']
        sched = str(sched)
        if sched != "Yearlong":
            await ctx.send(f'{userproj} is happening on {sched}.')
        else:
            await ctx.send(f'{userproj} is a yearlong project.')

@client.command(brief='Get a MEA Project Primer link.')
async def primer(ctx, *, project):
    sheet_id = '1kWSiOa7W-KFhgISUPE99Wwbdz2LgocMLNPES0S-J680'
    df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
    projlist = (df['Project']).to_list()
    projstring = ((df['Project']).to_string(index=False))
    userproj = project.split()[0]
    userproj = userproj.upper()
    if userproj not in projlist:
        await ctx.send(f'This project is not on the list. Try these: {projstring}.')
    else:
        row = df[df['Project'] == userproj].index[0]
        primer = df.iloc[row]['Primer']
        await ctx.send(f'{userproj} Primer: {primer}')

@client.command(brief='Track the attendance of your meeting by sending a message with the name of the people who joined!')
async def attendance(ctx):
    current_attendance = 0
    attendee_list = ''
    await ctx.send('Attendance will be taken, enter "x" to finalize the attendance')
    def check(m):
        return ctx.author == m.author
    while True:
        msg = await client.wait_for('message', check=check)
        if msg.content == 'x':
            break
        else:
            await ctx.send(f'{msg.content} has joined the meeting!')
            current_attendance += 1
            attendee_list = attendee_list + f'{msg.content}, '
            continue
    await ctx.send('What is this meeting for?')
    meeting_agenda = await client.wait_for('message', check=check)
    await ctx.send(f'''Meeting title: {meeting_agenda.content}
Final attendance tallied, {current_attendance} members present.
Attendees: {attendee_list[:-2]}''')

client.run(f'{discordtoken}')
