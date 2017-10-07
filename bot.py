import praw
import logging
import yaml
import itertools
from datetime import datetime
from os import environ, path
from dotenv import load_dotenv
from pdb import set_trace as bp
import sys
import time

dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Bot:
    EVENT = "Hurricane Maria"

    def __init__(self):
        self.debug()
        mode = [True for arg in sys.argv if arg == '-d']
        self.dry_run = False
        if (mode == [True]) :
            self.dry_run = mode
            self.DB = 'commented_test.txt'
            print('executing a dry run...')
        else:
            self.DB = 'commented.txt'
            answer = input('starting in production mode. should we continue? ')
            if(answer.lower() == 'n'):
                self.dry_run = False
                print('... exiting application')
                sys.exit()
        self.comments_for_run = 0
        self.reddit = self.authenticate()
        print('Authenticated', self.reddit)
        self.config = self.load_config()
        self.store = open(self.DB, 'a')
        self.scan()

    def debug(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('prawcore')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    def load_config(self):
        with open("config.yml", "r") as stream:
            conf =  yaml.load(stream)
            return conf['events'][self.EVENT]

    def authenticate(self):
      reddit = praw.Reddit(user_agent='Python:charity-bot-v1:v1 (by /u/lfender6445)',
                           client_id=environ.get('CLIENT_ID'), client_secret=environ.get('CLIENT_SECRET'),
                           username=environ.get('USERNAME'), password=environ.get('PASSWORD'))
      return reddit

    def scan(self):
        flat_subreddits = list(itertools.chain.from_iterable(self.config['subreddits']))
        for sub in flat_subreddits:
             subreddit = self.reddit.subreddit(sub).hot(limit=100)
             for submission in subreddit:
                 title = submission.title.lower()
                 matchers = [item.lower() for item in self.config['items_to_match_title_on']]
                 # MATCHERS ['hurricane maria', 'puerto rico', 'san juan', 'ponce']
                 for match in matchers:
                     if match in title:
                         time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                         print('-----------------', time)
                         link = 'https://www.reddit.com{perm}'.format(perm=submission.permalink)
                         print('link: ', link)
                         should_add_comment = input("allow charity bot to comment? Y or N ")
                         if(should_add_comment.lower() == 'y'):
                            self.reply(submission)
                            print('comment success at ', time)
                         else:
                            print('bot was denied comment operation')

        print('--- total comments for bot run', self.comments_for_run)

    def reply(self, post):
        # id = '73mwak'
        # is the id in the db?
        # else comment and save to db
        if post.id in open(self.DB).read():
            print("already commented. skipping comment operation for", post.id)
        else:
            text = self.comment_doc().format(cta=self.config['cta'], links=self.outbound_links())
            if(not self.dry_run):
                print('commenting in production mode')
                post.reply(text)
                time.sleep(600)
                print('10 minutes have passed')
            else:
                print('commenting in dev mode')
                # print(text)
            self.save_to_db(post.id)

    def save_to_db(self, id):
        # print('id to save', id)
        self.comments_for_run += 1
        self.store.write('%r\n' %id)

    def outbound_links(self):
        str = ""
        for link in self.config['charities']:
            title = link['title']
            href = link['href']
            bullet = '- [{title}]({href}){n}'.format(title=title, href=href, n="\n")
            str += bullet
        return str

    def comment_doc(self):
        return \
"""
{cta}\n\n
{links}
"""
    # def notify(self):
    #   # subreddit = reddit.subreddit('worldnews')
    #   # for submission in subreddit.stream.submissions():
    #   # use dir(submission)
    #   # OR pprint(vars(submission))
    #   subreddit = self.reddit.subreddit('worldnews').hot(limit=100)
    #   for submission in subreddit:
    #       title = submission.title.lower()
    #       match = 'Puerto Rico'.lower()
    #       if match in title:
    #           # bp()
    #           # pprint(vars(submission))
    #           print(submission.title, submission.permalink, submission.url)
    #           msg = '[Puerto Rico](reddit.com%s)' % submission.permalink
    #           self.reddit.redditor(environ.get('USER_TO_NOTIFY')).message(title[0:100], msg)


bot = Bot()
