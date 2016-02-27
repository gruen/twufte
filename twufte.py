#!/usr/bin/env python
__author__ = "Michael E. Gruen"


import twitter

import pandas as pd
import json

import time
from time import mktime
from datetime import datetime

api = twitter.Api(consumer_key=         TODO_consumer_key,
                  consumer_secret=      TODO_consumer_secret,
                  access_token_key=     TODO_access_token_key,
                  access_token_secret=  TODO_access_token_secret)

def convert_time(ts):
    return datetime.fromtimestamp(mktime(time.strptime(ts,'%a %b %d %H:%M:%S +0000 %Y')))

tufte_id = api.GetUser(screen_name='EdwardTufte').id
# tufte_id = api.GetUser(screen_name='gruen').id


statuses = []
max_id = None

while True:
    window = api.GetUserTimeline(user_id=tufte_id, count=200, include_rts=1, max_id=max_id)
    if len(window) == 0:
        break
    else:
        if max_id:
            statuses += window[1:]
        else:
            statuses += window
        max_id = window[-1].id

k = []
for s in statuses:
    t = []
    t.append(str(s.id))                                                       # tweet id
    t.append(convert_time(s.created_at))                                      # timestamp
    rt = s.retweeted_status                                               
    if(rt == None):                                                       
        t.append('tufte' in s.text.lower())                                   # rt w/ text tufte?
        t.append(False)                                                       # rt
        t.append(None)                                                        # rt id is none
        t.append(False)                                                       # tweet w/ mention tufte is none
    else:
        t.append('tufte' in s.retweeted_status.text.lower())                  # rt w/ text tufte?
        t.append(True)                                                        # rt
        t.append(str(s.retweeted_status.id))                                  # rt id
        t.append(tufte_id in [um.id for um in s.retweeted_status.user_mentions]) # rt w/ mention tufte?
    k.append(t)

twufts = pd.DataFrame(k, columns=['tweet_id', 'created_at', 'tufte_in_text', 'is_retweet', 'retweet_id', 'tufte_mentioned'])
twufts['is_tweet'] = True # for resample bullshit


twufts.set_index('created_at').resample('W', how='sum').fillna(0).to_clipboard()