<h1 align="center">》 Unzipper Bot 《</h1>

<p align="center">
  A Telegram Bot to Extract Various Types Of Archives
</p>

</br>


## Table of content
- [Features ⚡](#features-)
- [Config vars 📖](#configs-)
- [Deployment 👀](#deploy-)
  - [Heroku](#with-heroku)
  - [Self-hosting](#self-hosting)
- [Report bugs 🐞](#found-a-bug-)
- [Support 💙](#support-)
- [License and Copyright 👮](#license--copyright-)

</br>


## Features ⚡
- Extract various types of archives like `rar`, `zip`, `tar`, `7z`, `tar.xz` etc.
- Password support for extracting
- Extract archives from direct / gdrive links
- Support for multi-part 7z archives (archives ends with file extensions like `.001`, `.002`, etc.)
- Custom thumbnail support
- Muti-language support ([More info](https://github.com/Itz-fork/Unzipper-Bot/tree/main/unzipper/localization#readme))
- Upload files larger than 2GB to gofile.io
- Backup extracted files to gofile.io
- Broadcast messages to users
- Ban / Unban users from using your bot
- Check stats of the bot (users, hardware usage, etc.)
- Send logs in a private channel

And Some other features 🔥!

Also don't forget to check [changelog](CHANGELOG.md) 😉

</br>


## Configs 📖
- `APP_ID` - Your APP ID. Get it from [my.telegram.org](my.telegram.org)
- `API_HASH` - Your API_HASH. Get it from [my.telegram.org](my.telegram.org)
- `BOT_OWNER` - Your Telegram Account ID. Get it from [@MissRose_bot](https://t.me/MissRose_bot) (Start the bot and send <samp>/info</samp> command).
- `BOT_TOKEN` - Bot Token of Your Telegram Bot. Get it from [@BotFather](https://t.me/BotFather)
- `MONGODB_URL` - Your MongoDB url, Tutorial [here](https://www.youtube.com/watch?v=0aYrJTfYBHU)
- `LOGS_CHANNEL` - Follow these steps,
  - Make a private channel
  - Add your bot to the channel as an admin
  - Send a message and copy it's link
  - The link'll be something like `https://t.me/c/12345/1`. Simply copy the `12345` part from it and add `-100` to the beginning of it. Now it'll be something like `-10012345`. That's your channel id!
- `GOFILE_TOKEN` - Your gofile.io API token from your [profile page](https://gofile.io/myProfile)

</br>


## Deploy 👀
Deploying is easy 🤫! You can deploy this bot in Heroku or in a linux VPS ♥️! **Star 🌟 Fork 🍴 and Deploy**

### With Heroku
<a href="https://www.heroku.com/deploy?template=https://github.com/Itz-fork/Unzipper-Bot/tree/arch">
  <img src="https://www.herokucdn.com/deploy/button.svg">
</a>


### Self-Hosting
> Note ⚠️
> 
> It's recomended to use a arch linux based distro to deploy this bot as the original author of the p7zip package has not made an update since 2016, but the arch linux's version is packaged from an active fork.

```bash
git clone https://github.com/Itz-fork/Unzipper-Bot.git
cd Unzipper-Bot
pip3 install -r requirements.txt

# Arch linux
sudo pacman -Syyu
sudo pacman -S zstd p7zip

# Ubuntu
sudo add-apt-repository universe
sudo apt update
sudo apt install p7zip-full p7zip-rar zstd
```

<h4 align="center">Edit config.py with your own values</h4>

```bash
bash start.sh
```

**DONE 🥳, Enjoy The Bot! Be sure to Follow Me on [Github](https://github.com/Itz-fork) and Star 🌟 this repo to Show some support 😍!**

</br>


## Found a bug 🐞?
If you found a bug in this bot please open an [issue](https://github.com/Itz-fork/Unzipper-Bot/issues) or report it at the [Support group](#support).

</br>


## Support 💙
<a href="https://t.me/NexaBotsUpdates">
  <img src="https://img.shields.io/badge/Updates_Channel-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white">
</a>
<a href="https://t.me/Nexa_bots">
  <img src="https://img.shields.io/badge/Support_Group-0a0a0a?style=for-the-badge&logo=telegram&logoColor=white">
</a>

</br>


## License & Copyright 👮
```
Copyright (c) 2022 Itz-fork

This Unzipper-Bot repository is licensed under GPLv3 License (https://github.com/Itz-fork/Unzipper-Bot/blob/master/LICENSE)

Copying or modifying any part of this code without permission or proper credits is strictly prohibited
```
