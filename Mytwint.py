import twint
import requests
import re
from bs4 import BeautifulSoup
import requests


def getReplyer(name,id):

    url = "https://twitter.com/"+str(name)+"/status/" + str(id)
    # print(url)
    f = requests.get(url)  # Get该网页从而获取该html内容
    soup = BeautifulSoup(f.content, "lxml")  # 用lxml解析器解析该网页的内容, 好像f.text也是返回的html
    # print(f.text)

    # @classmethod

    tweet_div = soup.find('div', 'tweet')
    # print(tweet_div)
    replies = int(soup.find(
        'span', 'ProfileTweet-action--reply u-hiddenVisually').find(
        'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0')
    is_replied = False if replies == 0 else True

    if is_replied == False:
        replies_to_users = []
    else:
        stream_items = \
            soup.find_all('div', 'stream-item-header')
        # print(stream_items)
        replies_to_users = []
        for k in stream_items:
            username = k.find('b').text.strip('@')
            #        username = "".join(username.split())
            #         print(username)
            replies_to_users.append(username)
        # print(replies_to_users)
        return replies_to_users


def get_retweeters_list(tweet_id):
    # get the data of retweets
    r = requests.get('https://twitter.com/i/activity/retweeted_popup?id=' + str(tweet_id))
    # r = requests.get('https://twitter.com/BryanAlexander/status/' + str(tweet_id))
    # use the grep in order to get the retweeters

    text = r.text
    x = re.findall(
        'div class=\\\\"account  js-actionable-user js-profile-popup-actionable \\\\" data-screen-name=\\\\"(.+?)\\\\" data-user-id=\\\\"',
        text)
    return x


# Configure
c = twint.Config()
c.Username = "realDonaldTrump"
# c.Search = "COVID 19"
c.Limit = 10


# c.Tweet_id = "1257793742540386304"
c.Show_hashtags = True
c.Get_replies = True
c.Verified = True
c.Stats = True
c.Count = True
# print(get_retweeters_list("1258837711806496770"))
# Run
# twint.run.Profile(c)
c.Store_object = True
twint.run.Search(c)

tweets_as_objects = twint.output.tweets_list
print(type(tweets_as_objects))
# print(tweets_as_objects[0].id)
for tweet in tweets_as_objects:
    id = tweet.id
    name = tweet.username
    # print(name,"HHHHHHHHHHHHHHHHHHHHHHHH")
    likes_amount  = tweet.likes_count
    retweets_count = tweet.retweets_count
    replies_count = tweet.replies_count
    print(str(id), ":",
          " replay_people : ", getReplyer(name,id),
          " retweet_people : ",get_retweeters_list(id),
          " likes_amount : ",likes_amount,
          " retweets_count : ",retweets_count,
          " replies_count : ",replies_count)
