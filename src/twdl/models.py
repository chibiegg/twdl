# encoding=utf-8

from django.db import models
import tweepy
from twdl.utils import get_api
import sys


class User(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = u"Twitterアカウント"

    created_at = models.DateTimeField(u"登録日時")

    id_str = models.CharField("ID", max_length=100)
    screen_name = models.CharField("Screen Name", max_length=100)
    name = models.CharField("Name", max_length=100)
    url = models.URLField(u"プロフィール画像URL", max_length=512, blank=True)
    description = models.TextField(u"プロフィール説明", blank=True)
    profile_image_url = models.URLField(u"プロフィール画像URL", max_length=512, blank=True)
    profile_image = models.ImageField(u"プロフィール画像", blank=True, upload_to="profile")


    def __unicode__(self):
        return u"@%s" % self.screen_name

    @classmethod
    def create_from_id(cls, id_str):
        try:
            instance = cls.objects.get(id_str=id_str)
            return instance
        except cls.DoesNotExist:
            instance = cls(id_str=id_str)

        api = get_api()
        user = api.get_user(user_id=id_str)
        instance.created_at = user.created_at
        instance.screen_name = user.screen_name
        instance.name = user.name
        instance.url = user.url or u""
        instance.description = user.description or u""
        instance.profile_image_url = user.profile_image_url or u""
        instance.save()
        return instance


class Status(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = u"Twitterステータス"
        ordering = ("-created_at",)

    created_at = models.DateTimeField(u"登録日時")

    id_str = models.CharField("Status ID", max_length=100)
    text = models.TextField(u"本文")
    author = models.ForeignKey(User, related_name="author")
    source = models.CharField("ソース", max_length=100, blank=True)
    source_url = models.URLField(u"ソースURL", max_length=512, blank=True)

    in_reply_to_user_id_str = models.CharField("in Reply to User ID", max_length=100, blank=True)
    in_reply_to_status_id_str = models.CharField("in Reply to Status ID", max_length=100, blank=True)
    in_reply_to_status = models.ForeignKey("Status", blank=True, null=True)
    in_reply_to_user = models.ForeignKey(User, blank=True, null=True, related_name="in_reply_to_user")

    def __unicode__(self):
        return u"@%s: %s" % (self.author.screen_name, self.text)


    @classmethod
    def create_from_id(cls, id):
        api = get_api()

        try:
            return cls.objects.get(id_str=id)
        except cls.DoesNotExist:
            pass

        try:
            status = api.get_status(id=id)
            return cls.create_from_status(status)
        except tweepy.error.TweepError as e:
            print >> sys.stderr , e
            if u"limit" in unicode(e).lower():
                raise
            return None

    @classmethod
    def create_from_status(cls, status):
        id_str = status.id_str

        try:
            instance = cls.objects.get(id_str=id_str)
            return instance
        except cls.DoesNotExist:
            instance = cls(id_str=id_str)

        instance.created_at = status.created_at
        instance.text = status.text
        instance.source = status.source or u""
        instance.source_url = status.source_url or u""
        instance.in_reply_to_user_id_str = status.in_reply_to_user_id_str or u""
        instance.in_reply_to_status_id_str = status.in_reply_to_status_id_str or u""


        #User
        instance.author = User.create_from_id(status.author.id_str)
        #in Reply to User
        if instance.in_reply_to_user_id_str:
            instance.in_reply_to_user = User.create_from_id(instance.in_reply_to_user_id_str)

        instance.save()
        return instance




