# VNDB Discord Bot 🎮📚 

A Discord bot that interacts with the VNDB API to search for visual novels and characters, providing detailed information in informative embeds. The bot includes a variety of commands to enhance your server's experience with visual novel related content.
[Invite the Bot!](https://discord.com/oauth2/authorize?client_id=1231996105366048888&permissions=277025441856&integration_type=0&scope=bot)

## Features

- **Visual Novel Search (`/vn`)**: Search for visual novels by name. Select from a list of results and receive detailed information, including the original name, alternate names, playtime, languages, platforms, related media, and more.
- **Character Search (`/character`)**: Search for characters by name. View detailed information including aliases, measurements, birthday, blood type, gender, and roles in associated visual novels.
- **Random Visual Novel (`/randomvn`)**: Fetch a random visual novel from VNDB and view its detailed information.
- **Multilingual Support**: The bot displays country flags based on the language of the visual novel.
- **Clean UI**: All commands feature dropdown menus and buttons for a seamless user experience.

## Commands

### Character Information
- `/character`: Search for a character by name. Returns a dropdown menu of results from which you can select one to view detailed information.
  
  Usage: /character `name:<character name>`

### Visual Novel Information
- `/vn`: Search for a visual novel by name. Returns a dropdown menu of results from which you can select one to view detailed information.
  
  Usage: /vn `name:<visual novel name>`

### RandomVN
- `/randomvn`: Fetch a random visual novel and display its information.

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/StyingDev/Styings-VisualNovel-Bot.git
  ```

2. Navigate to the project directory:
  ```bash
  cd Styings-VisualNovel-Bot
  ```

3. Install the required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

4. Create a '.env' file in the project directory and add your Discord Bot Token:

  ```bash
  TOKEN=your_discord_bot_token_here
  ```

## Environment Variables

- `TOKEN`: Your Discord bot token, which can be obtained from the Discord Developer Portal.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This bot utilizes the [VNDB API](https://vndb.org/d11) for fetching visual novel and character data.
- Built using [Discord.py](https://discordpy.readthedocs.io/) library.
