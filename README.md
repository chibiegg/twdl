twdl
====

Twitter Download Tool

Requirements
-------------------

* Python
* Django1.3
* Tweepy


Setup
=====

  $ cd ./src/twdl/
  $ python management.py syncdb



Download The Account Tweet
========================

  $ cd ./src/twdl/
  $ python management.py crawl hoge(twitter account name)


Download The Conversation
========================

  $ cd ./src/twdl/
  $ python manage.py crawl_conversation

