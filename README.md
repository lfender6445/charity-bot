# charity-bot-v1

a configurable [reddit-bot](https://www.reddit.com/user/charity-bot-v1/) to encourage philanthropy and help those in need

the [config.yml](https://github.com/lfender6445/charity-bot/blob/master/config.yml) 
is what drives the bot to post and comment on threads related to your cause.

contributions are encouraged and welcome

# setup
- `git clone https://github.com/lfender6445/charity-bot`
- install dependencies
  - `pip3 install -r requirements.txt`
- Rename `.env.example` to `.env`
  - `mv .env.example .env`
- Update .env to include your bots `USERNAME`, `PASSWORD`, `CLIENT_SECRET`, and `CLIENT_ID`

# dev mode

you can start the bot in dev mode by running: 

`./bin/start-dev`

developer mode does NOT apply comments to reddit posts, 
but gives you an idea of how your bot configuration will work by logging
important information about the scan.

# production mode

you can start the bot in prod mode by running: 

`./bin/start-prod`

prod mode DOES apply comments to reddit posts and should be used with caution
