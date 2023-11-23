import random
import discord
import requests
import json
from discord.ext import commands
# token = MTA0MjY2OTM5Mzc4MTQ3MzMzMA.GG-7rw.gbGxi1l7amSDytO-CguSrng94IW-j-IQ-nl378

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)



# header untuk autorisasi
headers = {
    "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijc5YWJhOTMxODUyYzYyYmFiNzFkYjViMzMwMTFiMTY5MzkwMDk5NDhhMmYxNGNmZjJmYjllZTljZjZhNzIwZWRjNzEwNDhjZWZhYWIwYzI1In0.eyJhdWQiOiI3MmUwYzBiZTYxMzczZGFlNTdjZDRjMTBjNzk4YTkyMSIsImp0aSI6Ijc5YWJhOTMxODUyYzYyYmFiNzFkYjViMzMwMTFiMTY5MzkwMDk5NDhhMmYxNGNmZjJmYjllZTljZjZhNzIwZWRjNzEwNDhjZWZhYWIwYzI1IiwiaWF0IjoxNzAwNzM4MTczLCJuYmYiOjE3MDA3MzgxNzMsImV4cCI6MTcwMzMzMDE3Mywic3ViIjoiMTAzNzYyNjAiLCJzY29wZXMiOltdfQ.hqfTB9KaL-_EtxYAWSMyx1qD0rUHN3_OxOHLUwawB7zK1wsQHy6_qra0oHjCXc5fXd__7aXDNQtEPBP3PqZVlNwtRkHUVeoolMgjzw5rjZcIpxLdZRVcu07AxAJPDN4hYMukTzB_rpewnsArO1Ubn69AiI15MKYwE0ZiGCGKKEpd3JJ3LkMcuLP0Wdu0ngbJfK5kFOUofKSxIFO-HY_6G1ABB9rVcA3bA6sIICqokz38WExF8oM-mK-pAo1MdOJT1z3wUATlULT8cYP4emRLLZlbobfJILlaKGG-Q4Exqsc2RoKOYbxJMZF4zipJ6pnkMglN6hFMiQLmfPfdtQuINA"
}

def get_profile():
    response = requests.get("https://api.myanimelist.net/v2/users/@me",headers=headers)
    json_data = json.loads(response.text)
    output = "Profile Name : {name}\n{picture}".format(name=json_data['name'],picture=json_data['picture'])
    return output

def get_anime(startswith : str):
    title = []
    rank = []
    score = []
    main_picture = []
    synopsis = []
    params = {
        "q" : startswith
    }
    params_details = {
        "fields" : "title,mean,rank,synopsis,main_picture,synopsis"
    }
    response = requests.get("https://api.myanimelist.net/v2/anime",headers=headers,params=params)
    json_data = json.loads(response.text)
    print(json_data)
    for i in range(len(json_data["data"])):
        anime_id = json_data["data"][i]["node"]["id"]
        response_details = requests.get("https://api.myanimelist.net/v2/anime/{anime_id}".format(anime_id=anime_id),headers=headers,params=params_details)
        json_details = json.loads(response_details.text)
        try:
            title.append(json_details["title"])
        except KeyError:
            title.append("Title Unknown")
        try:
            rank.append(str(json_details['rank']))
        except KeyError:
            rank.append("Rank Unknown")
        try:
            score.append(str(json_details['mean']))
        except KeyError:
            score.append("Score Unknown")
        try:
            main_picture.append(json_details["main_picture"]["medium"])
        except KeyError:
            main_picture.append("Unknown Picture")
        try:
            synopsis.append(json_details["synopsis"])
        except KeyError:
            synopsis.append("Unknown synopsis")
    return title,rank,score,main_picture,synopsis

def get_top_n_by_genre(N : int, genre : str):
    return ""


@bot.command(
    name="admin",
    brief="show admin MAL profile (don't forget to visit)"
)
async def admin(ctx):
    profile = get_profile()
    await ctx.channel.send(profile)

@bot.command(
    name="find",
    help="input anime name that you are looking for\n$find <anime-name>",
    brief="show list of anime based on the arguments",
)
async def find(ctx,*args):
    input = ""
    for arg in args:
        input = input + " " + arg
    title,rank,score,main_picture,synopsis = get_anime(input)

    for index in range(len(title)):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)  
        embed = discord.Embed(
            title='Anime Details',
            description= synopsis[index],
            colour= discord.Colour.from_rgb(r,g,b)
        )

        embed.set_image(url=main_picture[index])
        embed.set_author(name=title[index],icon_url=main_picture[index])
        embed.add_field(name='Rank',value=rank[index])
        embed.add_field(name='Score',value=score[index])
        embed.set_footer(text="This information was taken from MyAnimeList API")
        await ctx.send(embed=embed)

bot.run('MTA0MjY2OTM5Mzc4MTQ3MzMzMA.GvcRn9.kzRQU8sWI7uqKJDWn-jsf6c__h7Y8NSZZZMHZ4')