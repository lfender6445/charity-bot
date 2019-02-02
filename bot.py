import praw
import logging
import yaml
import itertools
import sys
import time
from datetime import datetime
from os import environ, path
from dotenv import load_dotenv
from pdb import set_trace as bp


class Bot:
    GITHUB_LINK = "https://github.com/lfender6445/charity-bot"
    FEEDBACK_LINK = "https://www.reddit.com/message/compose/?to=charity-bot-v1&subject=Feedback"

    def __init__(self):
        self.setup_database()
        self.connect_to_reddit_and_scan()

    def setup_database(self):
        self.development_mode = '-d' in sys.argv
        self.comments_for_run = 0
        if (self.development_mode):
            self.DB = 'commented_test.txt'
            print('executing in development mode... comments disabled')
        else:
            self.DB = 'commented.txt'
            print('executing in production mode... comments ARE enabled')
        self.database = open(self.DB, 'a')

    def connect_to_reddit_and_scan(self):
        self.connect_to_reddit()
        self.scan()

    def connect_to_reddit(self):
        self.load_env()
        self.debug()
        self.reddit = self.authenticate()
        self.config = self.load_config()

    def load_env(self):
        dotenv_path = path.join(path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)

    def debug(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('prawcore')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    def load_config(self):
        with open("config.yml", "r") as stream:
            return yaml.safe_load(stream)['events']

    def authenticate(self):
        reddit = praw.Reddit(
            user_agent='Python:charity-bot-v1:v1 (by /u/lfender6445)',
            client_id=environ.get('CLIENT_ID'),
            client_secret=environ.get('CLIENT_SECRET'),
            username=environ.get('USERNAME'),
            password=environ.get('PASSWORD'))
        return reddit

    def scan(self):
        for event in self.config.keys():
            print('searching on event', event)
            self.event = self.config[event]
            subreddits = self.event['subreddits']
            if subreddits[0] is not None:
                print('running')
                flat_subreddits = list(
                    itertools.chain.from_iterable(subreddits)
                )
                for sub in flat_subreddits:
                    subreddit = self.reddit.subreddit(sub).new(limit=300)
                    for submission in subreddit:
                        self.process_submission(submission)
                print('total comments for bot run', self.comments_for_run)
            else:
                print('could not find any matches')

    def process_submission(self, post):
        title = post.title.lower()
        matchers = [
            item.lower() for item in self.event['items_to_match_title_on']
        ]
        for match in matchers:
            if match in title:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                link = 'https://www.reddit.com{perm}'.format(
                    perm=post.permalink)
                print('-----------------', time)
                print('title: ', post.title)
                print('link: ', link)
                # self.ask_to_comment(post, time)
                self.reply(post)

    def ask_to_comment(self, post, time):
        should_add_comment = input("allow charity bot to comment? Y or N ")
        if (should_add_comment.lower() == 'y'):
            self.reply(post)
        else:
            print('bot was denied comment operation')

    def reply(self, post):
        if post.id in open(self.DB).read():
            print("already commented. skipping comment operation for", post.id)
        else:
            text = self.comment_doc().format(
                cta=self.event['cta'],
                links=self.outbound_links(),
                feedback_text=self.feedback_text())
            if (self.development_mode):
                print('comments are disabled in development mode')
            else:
                print('commenting in production mode')
                post.reply(text)
                time.sleep(600)
                print('comment success')
                # print(text)
            self.save_to_db(post.id)

    def feedback_text(self):
        return "I am a bot - if I did something wrong, [let me know]({link}) | [source]({gh})".format(
            link=self.FEEDBACK_LINK, gh=self.GITHUB_LINK)

    def save_to_db(self, id):
        self.comments_for_run += 1
        self.database.write('%r\n' % id)

    def outbound_links(self):
        str = ""
        for link in self.event['charities']:
            title = link['title']
            href = link['href']
            bullet = '- [{title}]({href}){n}'.format(
                title=title, href=href, n="\n")
            str += bullet
        return str

    def comment_doc(self):
        return \
"""
{cta}\n\n
{links}
\n
{feedback_text}
"""

    # def ask_to_run_script(self):
    # answer = input('starting in production mode. should we continue? ')
    # if (answer.lower() == 'n'):
    #     self.development_mode = False
    #     print('... exiting application')
    #     sys.exit()


bot = Bot()
