import praw
import logging
# settings.py
from os import environ, path
from dotenv import load_dotenv
from pdb import set_trace as bp

dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Bot:
    def __init__(self):
        # self.debug()
        self.reddit = self.authenticate()
        print('authenticated', self.reddit)
        self.send_message()

    def debug(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('prawcore')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    def authenticate(self):
      reddit = praw.Reddit(user_agent='charity-bot (by /u/lfender6445)',
                           client_id=environ.get('CLIENT_ID'), client_secret=environ.get('CLIENT_SECRET'),
                           username=environ.get('USERNAME'), password=environ.get('PASSWORD'))
      return reddit

    def send_message(self):
      # subreddit = reddit.subreddit('worldnews')
      # for submission in subreddit.stream.submissions():
      subreddit = self.reddit.subreddit('worldnews').hot(limit=100)
      # use dir(submission)
      # OR pprint(vars(submission))


      for submission in subreddit:
          title = submission.title.lower()
          match = 'Puerto Rico'.lower()
          if match in title:
              # bp()
              # pprint(vars(submission))
              print(submission.title, submission.permalink, submission.url)
              msg = '[Puerto Rico](reddit.com%s)' % submission.permalink
              self.reddit.redditor(environ.get('USERNAME')).message(title[0:100], msg)

bot = Bot()
