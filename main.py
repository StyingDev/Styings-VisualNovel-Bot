import requests
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import random
import os
import re

load_dotenv()
TOKEN = os.getenv("TOKEN")

VNDB_API_URL = "https://api.vndb.org/kana"

LANGUAGE_TO_FLAG = {
    "en": "🇺🇸",  # English
    "ja": "🇯🇵",  # Japanese
    "fr": "🇫🇷",  # French
    "de": "🇩🇪",  # German
    "es": "🇪🇸",  # Spanish
    "it": "🇮🇹",  # Italian
    "ru": "🇷🇺",  # Russian
    "zh": "🇨🇳",  # Chinese (Simplified)
    "zh-Hant": "🇹🇼",  # Chinese (Traditional)
    "ko": "🇰🇷",  # Korean
    "pt": "🇵🇹",  # Portuguese
    "pt-BR": "🇧🇷",  # Portuguese (Brazil)
    "nl": "🇳🇱",  # Dutch
    "sv": "🇸🇪",  # Swedish
    "da": "🇩🇰",  # Danish
    "fi": "🇫🇮",  # Finnish
    "no": "🇳🇴",  # Norwegian
    "pl": "🇵🇱",  # Polish
    "cs": "🇨🇿",  # Czech
    "hu": "🇭🇺",  # Hungarian
    "ro": "🇷🇴",  # Romanian
    "el": "🇬🇷",  # Greek
    "tr": "🇹🇷",  # Turkish
    "ar": "🇸🇦",  # Arabic
    "hi": "🇮🇳",  # Hindi
    "bn": "🇧🇩",  # Bengali
    "ur": "🇵🇰",  # Urdu
    "ta": "🇱🇰",  # Tamil
    "th": "🇹🇭",  # Thai
    "vi": "🇻🇳",  # Vietnamese
    "id": "🇮🇩",  # Indonesian
    "ms": "🇲🇾",  # Malay
    "tl": "🇵🇭",  # Filipino
    "fa": "🇮🇷",  # Persian
    "uk": "🇺🇦",  # Ukrainian
    "bg": "🇧🇬",  # Bulgarian
    "hr": "🇭🇷",  # Croatian
    "sr": "🇷🇸",  # Serbian
    "sk": "🇸🇰",  # Slovak
    "sl": "🇸🇮",  # Slovenian
    "lt": "🇱🇹",  # Lithuanian
    "lv": "🇱🇻",  # Latvian
    "et": "🇪🇪",  # Estonian
    "is": "🇮🇸",  # Icelandic
    "ga": "🇮🇪",  # Irish
    "mt": "🇲🇹",  # Maltese
    "ca": "🇪🇸",  # Catalan
    "eu": "🇪🇸",  # Basque
    "gl": "🇪🇸",  # Galician
    "af": "🇿🇦",  # Afrikaans
    "sw": "🇰🇪",  # Swahili
    "am": "🇪🇹",  # Amharic
    "yo": "🇳🇬",  # Yoruba
    "ig": "🇳🇬",  # Igbo
    "ha": "🇳🇬",  # Hausa
    "zu": "🇿🇦",  # Zulu
    "xh": "🇿🇦",  # Xhosa
    "ny": "🇲🇼",  # Chichewa
    "sn": "🇿🇼",  # Shona
    "so": "🇸🇴",  # Somali
    "mg": "🇲🇬",  # Malagasy
    "la": "🇻🇦",  # Latin
    "sm": "🇼🇸",  # Samoan
    "to": "🇹🇴",  # Tongan
    "mi": "🇳🇿",  # Maori
    "haw": "🇺🇸",  # Hawaiian
}

EMBED_COLOR = 0x757e8a

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="D!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="🌲linktr.ee/Stying"))
    await bot.tree.sync()
    print(f'We have logged in as {bot.user.name}')

def format_description(description):
    if description is None:
        return "N/A"
    
    url_pattern = re.compile(r'\[url=(https?://[^\]]+)\](.*?)\[/url\]')
    relative_url_pattern = re.compile(r'\[url=/([^\]]+)\](.*?)\[/url\]')
    
    formatted_description = re.sub(url_pattern, r'[\2](\1)', description)
    formatted_description = re.sub(relative_url_pattern, r'[\2](https://vndb.org/\1)', formatted_description)
    
    return formatted_description

def truncate_text(text, limit=1024):
    if text is None:
        return "N/A"
    return text if len(text) <= limit else text[:limit - 3] + "..."

def fetch_vn_details(vn_id):
    request_data = {
        "filters": ["id", "=", vn_id],
        "fields": "title,alttitle,titles.title,titles.lang,description,relations.id,relations.relation,relations.title,platforms,image.url,length,length_minutes,languages"
    }

    response = requests.post(f"{VNDB_API_URL}/vn", headers={'Content-Type': 'application/json'}, json=request_data)

    if response.status_code == 200:
        data = response.json()
        vn_info = data.get('results', [{}])[0]

        if vn_info:
            title = vn_info.get('title', 'N/A')
            original_title = vn_info.get('alttitle', 'N/A')
            alternate_names = [t.get('title', 'N/A') for t in vn_info.get('titles', []) if t.get('lang') != 'ja']
            description = format_description(vn_info.get('description', 'N/A'))
            related_media = vn_info.get('relations', [])
            platforms = vn_info.get('platforms', [])
            cover = vn_info.get('image', {}).get('url', 'N/A')
            length_minutes = vn_info.get('length_minutes')
            languages = vn_info.get('languages', [])

            if length_minutes is not None:
                try:
                    length_minutes = int(length_minutes)
                    hours = length_minutes // 60
                    minutes = length_minutes % 60
                    if hours > 0 and minutes > 0:
                        length_formatted = f"{hours} hours {minutes} minutes"
                    elif hours > 0:
                        length_formatted = f"{hours} hours"
                    elif minutes > 0:
                        length_formatted = f"{minutes} minutes"
                    else:
                        length_formatted = "N/A"
                except ValueError:
                    length_formatted = "N/A"
            else:
                length_formatted = "N/A"

            related_vns = ", ".join([f"[{rel['title']}](https://vndb.org/{rel['id']})" for rel in related_media]) if related_media else "N/A"

            return {
                "title": title,
                "original_title": original_title,
                "alternate_names": alternate_names,
                "description": description,
                "related_vns": related_vns,
                "platforms": platforms,
                "cover": cover,
                "length": length_formatted,
                "languages": languages
            }
        else:
            return None
    else:
        return None


def fetch_character_details(char_id):
    request_data = {
        "filters": ["id", "=", char_id],
        "fields": "id, name, original, aliases, description, image.url, blood_type, height, weight, bust, waist, hips, cup, age, birthday, sex, vns.title, vns.role, vns.id"
    }

    response = requests.post(f"{VNDB_API_URL}/character", json=request_data)

    if response.status_code == 200:
        data = response.json()
        char_info = data.get('results', [{}])[0]

        if char_info:
            name = char_info.get('name', 'N/A')
            original_name = char_info.get('original', 'N/A')
            aliases = char_info.get('aliases', [])
            height = char_info.get('height', 'N/A')
            weight = char_info.get('weight', 'N/A')
            bust = char_info.get('bust', 'N/A')
            waist = char_info.get('waist', 'N/A')
            hips = char_info.get('hips', 'N/A')
            cup = char_info.get('cup', 'N/A')
            age = char_info.get('age', 'N/A')
            birthday = char_info.get('birthday', 'N/A')
            blood_type = char_info.get('blood_type', 'N/A')
            sex = char_info.get('sex', [])
            description = format_description(truncate_text(char_info.get('description', 'N/A')))
            vn_roles = char_info.get('vns', [])
            image_url = char_info.get('image', {}).get('url', None)

            measurements = (
                f"- **Height:**\n - {height} cm\n"
                f"- **Weight:**\n - {weight} kg\n"
                f"- **Bust - Waist - Hips:** \n - {bust} cm\n - {waist} cm\n - {hips} cm\n"
                f"- **Cup:**\n - {cup}"
            ) if height != 'N/A' else "N/A"

            visual_novels = "\n".join([f"[{vn['title']}](https://vndb.org/{vn['id']}) ({vn['role']})" for vn in vn_roles]) if vn_roles else "N/A"
            visual_novels = truncate_text(visual_novels)

            unique_sex = set(sex)
            sex_output = ", ".join(['♂️ Male' if s == 'm' else '♀️ Female' if s == 'f' else '⚪ Not Specified' for s in unique_sex])

            return {
                "name": name,
                "original_name": original_name,
                "aliases": aliases,
                "measurements": measurements,
                "age": age,
                "birthday": birthday,
                "blood_type": blood_type,
                "sex": sex_output,
                "role": visual_novels,
                "description": description,
                "image_url": image_url
            }
        else:
            return None
    else:
        return None


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="vn", description="Search for a Visual Novel in VNDB")
async def vn_search(interaction: discord.Interaction, name: str):
    search_query = {
        "filters": ["search", "=", name],
        "fields": "id,title,aliases,olang"
    }

    response = requests.post(f"{VNDB_API_URL}/vn", json=search_query)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            options = []
            for result in results:
                title = result['title']
                olang = result.get('olang', 'en')
                flag = LANGUAGE_TO_FLAG.get(olang, '🏳️')
                truncated_title = title[:90] + "..." if len(title) > 90 else title
                display_name = f"{flag} {truncated_title}"

                description = ", ".join(result['aliases']) if result['aliases'] else "N/A"
                description = description[:100]

                options.append(
                    discord.SelectOption(
                        label=display_name,
                        description=description,
                        value=result['id']
                    )
                )

            class VNDropdown(discord.ui.Select):
                def __init__(self):
                    super().__init__(placeholder="Select a visual novel...", min_values=1, max_values=1, options=options)

                async def callback(self, interaction: discord.Interaction):
                    selected_id = self.values[0]
                    vn_details = fetch_vn_details(selected_id)

                    if vn_details:
                        embed = discord.Embed(
                            title=vn_details['title'],
                            url=f"https://vndb.org/{selected_id}",
                            description=vn_details['description'],
                            color=EMBED_COLOR
                        )
                        embed.set_thumbnail(url=vn_details['cover'])
                        embed.add_field(name="🏷️ __Original Name:__", value=truncate_text(vn_details['original_title']), inline=False)
                        embed.add_field(name="🔄 __Alternate Names:__", value=truncate_text(", ".join(vn_details['alternate_names']) if vn_details['alternate_names'] else "N/A"), inline=False)
                        embed.add_field(name="⏳ __Playtime:__", value=truncate_text(vn_details['length']), inline=False)
                        embed.add_field(name="🌐 __Languages:__", value=truncate_text(" ".join(LANGUAGE_TO_FLAG.get(lang, '🏳️') for lang in vn_details['languages'])), inline=False)
                        embed.add_field(name="🎮 __Platforms:__", value=truncate_text(", ".join(vn_details['platforms'])), inline=False)
                        embed.add_field(name="🔗 __Related Media:__", value=truncate_text(vn_details['related_vns']), inline=False)

                        buttons = VNButtonPanel(selected_id)

                        await interaction.response.send_message(embed=embed, view=buttons)
                    else:
                        await interaction.response.send_message(f"No details found for the selected visual novel.", ephemeral=False)


            view = discord.ui.View()
            view.add_item(VNDropdown())

            await interaction.response.send_message(f"{len(results)} results found. Select one from the list below:", view=view, ephemeral=False)
        else:
            await interaction.response.send_message(f"No results found.", ephemeral=False)
    else:
        await interaction.response.send_message(f"Error searching for visual novels. Please try again later.", ephemeral=False)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="character", description="Search for a character in VNDB")
async def character_search(interaction: discord.Interaction, name: str):
    search_query = {
        "filters": ["search", "=", name],
        "fields": "id,name,original,aliases,sex"
    }

    response = requests.post(f"{VNDB_API_URL}/character", json=search_query)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            options = []
            for result in results:
                name = result['name']
                original_name = result.get('original', 'N/A')
                aliases = result.get('aliases', [])
                sex = result.get('sex', [])

                # Create description with aliases
                description = ", ".join(aliases) if aliases else "N/A"
                
                # Include gender emoji based on sex
                sex_emoji = '♂️' if 'm' in sex else '♀️' if 'f' in sex else '⚪'
                display_name = f"{sex_emoji} {name}"
                
                truncated_description = description[:100]  # Truncate description to fit dropdown

                options.append(
                    discord.SelectOption(
                        label=display_name,
                        description=truncated_description,
                        value=result['id']
                    )
                )

            class CharacterDropdown(discord.ui.Select):
                def __init__(self):
                    super().__init__(placeholder="Select a character...", min_values=1, max_values=1, options=options)

                async def callback(self, interaction: discord.Interaction):
                    selected_id = self.values[0]
                    char_details = fetch_character_details(selected_id)

                    if char_details:
                        embed = discord.Embed(
                            title=char_details['name'],
                            url=f"https://vndb.org/{selected_id}",
                            description=char_details['description'],
                            color=EMBED_COLOR
                        )
                        embed.set_thumbnail(url=char_details['image_url'])
                        embed.add_field(name="🏷️ __Original Name:__", value=truncate_text(char_details['original_name']), inline=False)
                        embed.add_field(name="🔄 __Aliases:__", value=truncate_text(", ".join(char_details['aliases']) if char_details['aliases'] else "N/A"), inline=False)
                        embed.add_field(name="📏 __Measurements:__", value=char_details['measurements'], inline=False)
                        embed.add_field(name="🎂 __Birthday (Month, Day):__", value=char_details['birthday'], inline=False)
                        embed.add_field(name="🩸 __Blood Type:__", value=char_details['blood_type'], inline=False)
                        embed.add_field(name="♂️ __Gender:__", value=char_details['sex'], inline=False)
                        embed.add_field(name="🎭 __Roles:__", value=char_details['role'], inline=False)

                        buttons = CharacterButtonPanel(selected_id)

                        await interaction.response.send_message(embed=embed, view=buttons)
                    else:
                        await interaction.response.send_message(f"No details found for the selected character.", ephemeral=False)

            view = discord.ui.View()
            view.add_item(CharacterDropdown())

            await interaction.response.send_message(f"{len(results)} results found. Select one from the list below:", view=view, ephemeral=False)
        else:
            await interaction.response.send_message(f"No results found.", ephemeral=False)
    else:
        await interaction.response.send_message(f"Error searching for characters. Please try again later.", ephemeral=False)


class CharacterButtonPanel(discord.ui.View):
    def __init__(self, char_id):
        super().__init__()
        self.char_id = char_id

        self.add_item(discord.ui.Button(label="More Info", url=f"https://vndb.org/{self.char_id}"))

class VNButtonPanel(discord.ui.View):
    def __init__(self, vn_id):
        super().__init__()
        self.vn_id = vn_id

        self.add_item(discord.ui.Button(label="More Info", url=f"https://vndb.org/{self.vn_id}"))


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="randomvn", description="Fetch a random visual novel")
async def random_vn(interaction: discord.Interaction):
    # Acknowledge the interaction first
    await interaction.response.defer()

    # Step 1: Fetch the highest VN ID
    highest_id_response = requests.post(f"{VNDB_API_URL}/vn", headers={'Content-Type': 'application/json'}, json={"sort": "id", "reverse": True, "results": 1})
    
    if highest_id_response.status_code == 200:
        highest_id_data = highest_id_response.json()
        highest_id = highest_id_data.get('results', [{}])[0].get('id', None)

        if highest_id:
            # Step 2: Generate a random VN ID
            random_id = f"v{random.randint(1, int(highest_id[1:]))}"
            
            # Step 3: Fetch details for the random VN ID
            vn_details = fetch_vn_details(random_id)
            
            if vn_details:
                embed = discord.Embed(
                    title=vn_details['title'],
                    url=f"https://vndb.org/{random_id}",
                    description=vn_details['description'],
                    color=EMBED_COLOR
                )
                embed.set_thumbnail(url=vn_details['cover'])
                embed.add_field(name="🏷️ __Original Name:__", value=truncate_text(vn_details['original_title']), inline=False)
                embed.add_field(name="🔄 __Alternate Names:__", value=truncate_text(", ".join(vn_details['alternate_names']) if vn_details['alternate_names'] else "N/A"), inline=False)
                embed.add_field(name="⏳ __Playtime:__", value=truncate_text(vn_details['length']), inline=False)
                embed.add_field(name="🌐 __Languages:__", value=truncate_text(" ".join(LANGUAGE_TO_FLAG.get(lang, '🏳️') for lang in vn_details['languages'])), inline=False)
                embed.add_field(name="🎮 __Platforms:__", value=truncate_text(", ".join(vn_details['platforms'])), inline=False)
                embed.add_field(name="🔗 __Related Media:__", value=truncate_text(vn_details['related_vns']), inline=False)

                buttons = VNButtonPanel(random_id)

                await interaction.followup.send(embed=embed, view=buttons)
            else:
                await interaction.followup.send("No details found for the selected visual novel.", ephemeral=False)
        else:
            await interaction.followup.send("Unable to determine the highest VN ID.", ephemeral=False)
    else:
        await interaction.followup.send("Error fetching the highest VN ID. Please try again later.", ephemeral=False)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="cover", description="Search for a Visual Novel cover in VNDB")
async def cover_search(interaction: discord.Interaction, name: str):
    search_query = {
        "filters": ["search", "=", name],
        "fields": "id,title,image.url,aliases"
    }

    try:
        response = requests.post(f"{VNDB_API_URL}/vn", json=search_query)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        results = data.get('results', [])

        if results:
            options = []
            for result in results:
                title = result['title']
                truncated_title = title[:90] + "..." if len(title) > 90 else title

                aliases = result.get('aliases', [])
                description = ", ".join(aliases) if aliases else "N/A"
                if len(description) > 100:
                    description = description[:97] + "..."

                options.append(
                    discord.SelectOption(
                        label=truncated_title,
                        description=description,
                        value=result['id']
                    )
                )

            class CoverDropdown(discord.ui.Select):
                def __init__(self):
                    super().__init__(placeholder="Select a visual novel...", min_values=1, max_values=1, options=options)

                async def callback(self, interaction: discord.Interaction):
                    selected_id = self.values[0]
                    vn_details = fetch_vn_details(selected_id)

                    if vn_details:
                        embed = discord.Embed(
                            title=vn_details['title'],
                            url=f"https://vndb.org/{selected_id}",
                            color=EMBED_COLOR
                        )
                        embed.set_image(url=vn_details['cover'])

                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message("No details found for the selected visual novel.", ephemeral=True)

            view = discord.ui.View()
            view.add_item(CoverDropdown())

            await interaction.response.send_message(f"{len(results)} results found. Select one from the list below:", view=view, ephemeral=False)
        else:
            await interaction.response.send_message("No results found.", ephemeral=False)
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        await interaction.response.send_message(f"Error searching for visual novels: {e}", ephemeral=True)

bot.run(TOKEN)
