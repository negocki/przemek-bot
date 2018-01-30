import wykop
import random

class WykopFeatures:
    def __init__(self):
        key = "DckQrvYifo"
        secret = "eh1KVgsGxJ"  # super secreit!!111one
        self.api = wykop.WykopAPI(key, secret)

    def get_hot(self):  # getting first page of gorace
        return self.api.get_stream_hot(1)

    def get_random_hot(self):  # getting random entry from first page
        hot_list = self.get_hot()
        hot_random = random.choice(hot_list)

        url = hot_random["url"]
        author = hot_random["author"]
        author_avatar = hot_random["author_avatar"]
        votes = hot_random["vote_count"]
        date = hot_random["date"]
        body = hot_random["body"]

        return (body,author,author_avatar,votes,date,url)

