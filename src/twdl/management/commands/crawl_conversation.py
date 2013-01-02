# encoding=utf-8

import tweepy

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from twdl.utils import get_api
from twdl.models import Status

class Command(BaseCommand):
    args = '<screen_name>'
    help = 'Crawl conversations of user status.'
    def handle(self, *args, **options):

        print u"%d" % Status.objects.filter(in_reply_to_status__isnull=True).exclude(in_reply_to_status_id_str="").exclude(in_reply_to_status_id_str__startswith="_").count()
        #return
        for s in Status.objects.filter(in_reply_to_status__isnull=True).exclude(in_reply_to_status_id_str="").exclude(in_reply_to_status_id_str__startswith="_"):
            status = Status.create_from_id(s.in_reply_to_status_id_str)
            if status:
                s.in_reply_to_status = status
            else:
                s.in_reply_to_status_id_str = u"_%s" % s.in_reply_to_status_id_str
            s.save()
            print s.in_reply_to_status_id_str, status

