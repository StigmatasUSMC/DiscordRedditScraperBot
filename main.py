import asyncio
import discord
import praw
import sqlite3


post_frequency = 600  # in seconds
token = 'faketoken'
id_channel = 'fakechannel'
sublist = [['netsecstudents', 30], ['fakesubreddit', 9000]]

reddit = praw.Reddit('bot1')
replied_to = sqlite3.connect('replied_to.db')
c = replied_to.cursor()
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

c.execute('create table if not exists replied_to(submission text)')


def forumal_dank(sub, count):
    danger = reddit.subreddit(sub)
    new_title = []
    new_post = []
    for post in danger.hot(limit=10):
        if post.ups > count and not post.stickied:
            c.execute("SELECT * FROM replied_to WHERE submission=?", (post.id,))
            if c.fetchone():
                pass
            else:
                c.execute("INSERT INTO replied_to VALUES (:submission)", {'submission': post.id})
                replied_to.commit()
                new_title.append(post.title)
                new_post.append(post.url)
            print(new_post, new_title)
    return new_post, new_title


async def my_background_task():
    await client.wait_until_ready()
    channel = await client.fetch_channel(int(id_channel))
    while not client.is_closed():
        for item in sublist:
            sub, title = forumal_dank(item[0], item[1])
            [await channel.send(post_title + '\n' + post) for post, post_title in zip(sub, title)]
        await asyncio.sleep(600)  # task runs every x seconds


client.loop.create_task(my_background_task())
client.run(str(token))
