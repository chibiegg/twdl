# encoding=utf-8

import tweepy

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from twdl.utils import get_api
from twdl.models import Status

class Command(BaseCommand):
    args = '<screen_name>'
    help = 'Crawl user status.'
    def handle(self, *args, **options):
        if len(args) == 0:
            return

        screen_name = args[0]
        api = get_api()

        print "Crowl statuses by @%s." % screen_name

        for p in tweepy.Cursor(api.user_timeline, screen_name=screen_name).items():
            status = Status.create_from_status(p)
            print status
