# charity-bot-v1

a configurable reddit-bot to encourage philanthropy and help those in need

contributions are welcome

# setup

```bash
mv .env.example .env
# update .env with appropriate credentials
# dev mode does not apply comments
./bin/start-dev
# or
./bin/start-prod
# comments are applied in prod mode
```

### debugging

```bash
python3 -m pdb bot.py -d
````
