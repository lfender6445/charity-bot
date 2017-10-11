# charity-bot

A configurable [reddit-bot /u/charity-bot-v1](https://www.reddit.com/user/charity-bot-v1/) to encourage philanthropy and help those in need

The [config.yml](https://github.com/lfender6445/charity-bot/blob/master/config.yml) 
makes it easy to add, remove, and edit new charitable causes.  

Contributions are encouraged and welcome

## setup
- `git clone https://github.com/lfender6445/charity-bot`
- install dependencies
  - `pip3 install -r requirements.txt`
- rename `.env.example` to `.env`
  - `mv .env.example .env`
- update .env to include your bots `USERNAME`, `PASSWORD`, `CLIENT_SECRET`, and `CLIENT_ID`

### starting the bot in dev mode

you can start the bot in dev mode by running: 

`./bin/start-dev`

**developer mode does NOT apply comments to reddit posts**, 
but gives you an idea of how your bot configuration will work by logging
important information about the scan.

### starting the bot in production mode

you can start the bot in prod mode by running: 

`./bin/start-prod`

**prod mode DOES apply comments to reddit posts** and should be used with caution
