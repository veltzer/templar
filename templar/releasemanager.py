import smtplib
import email.mime.text
import configparser
import os
import sys
import tweepy


class ReleaseManager:
    def __init__(self):
        self.debug = False
        self.config = configparser.ConfigParser()
        self.name = 'release_manager'
        self.config.read([
            self.name+'.cfg',
            'support/'+self.name+'.cfg',
            os.path.expanduser('~/.'+self.name+'.cfg')
        ])
        self.section = 'release'
        self.p_subject = self.config.get(self.section, 'subject')
        self.p_from = self.config.get(self.section, 'from')
        self.p_to_string = self.config.get(self.section, 'to')
        self.p_to = self.p_to_string.split(',')
        self.p_doTo = self.config.get(self.section, 'doTo')
        self.p_smtp_host = self.config.get(self.section, 'smtp_host')
        self.p_smtp_port = self.config.get(self.section, 'smtp_port')
        self.p_content = self.config.get(self.section, 'content')
        self.p_mail_user = self.config.get(self.section, 'mail_user')
        self.p_mail_password = self.config.get(self.section, 'mail_password')
        self.p_twitter_user = self.config.get(self.section, 'twitter_user')
        self.p_twitter_password = self.config.get(self.section, 'twitter_password')
        self.p_facebook_user = self.config.get(self.section, 'facebook_user')
        self.p_facebook_password = self.config.get(self.section, 'facebook_password')
        self.p_debug = bool(self.config.get(self.section, 'debug'))
        self.p_use_tls = bool(self.config.get(self.section, 'use_tls'))

        self.p_email = bool(self.config.get(self.section, 'email'))
        self.p_tweet = bool(self.config.get(self.section, 'tweet'))
        self.p_face = bool(self.config.get(self.section, 'face'))
        self.p_twitter_consumer_key = self.config.get(self.section, 'twitter_consumer_key')
        self.p_twitter_consumer_secret = self.config.get(self.section, 'twitter_consumer_secret')
        self.p_twitter_access_token = self.config.get(self.section, 'twitter_access_token')
        self.p_twitter_access_token_secret = self.config.get(self.section, 'twitter_access_token_secret')
        # p_non_exist = config.get(section, 'non_exist')
        if self.debug:
            # print the entire config
            self.config.write(sys.stdout)
            self.p_debug = True

    def do_email(self):
        # build the message...
        msg = email.mime.text.MIMEText(self.p_content)
        msg['Subject'] = self.p_subject
        msg['From'] = self.p_from
        if self.p_doTo:
            msg['To'] = self.p_to_string
        # Send the message via our own SMTP server, but don't include the # envelope header.
        server = smtplib.SMTP(self.p_smtp_host, self.p_smtp_port)
        server.ehlo()
        if self.p_debug:
            server.set_debuglevel(1)
        if self.p_use_tls:
            server.starttls()
        server.ehlo()
        if self.p_debug:
            print('p_mail_user is ', self.p_mail_user)
            print('p_mail_password is ', self.p_mail_password)
        server.login(self.p_mail_user, self.p_mail_password)
        server.sendmail(self.p_from, self.p_to, msg.as_string())
        server.quit()

    def do_tweet(self):
        auth = tweepy.OAuthHandler(self.p_twitter_consumer_key, self.p_twitter_consumer_secret)
        auth.set_access_token(self.p_twitter_access_token, self.p_twitter_access_token_secret)
        api = tweepy.API(auth)
        api.update_status(self.p_content)

    def do_facebook(self):
        pass

    def release(self):
        if self.p_email:
            self.do_email()
        if self.p_tweet:
            self.do_tweet()
        if self.p_face:
            self.do_facebook()


def release():
    rm = ReleaseManager()
    rm.release()
