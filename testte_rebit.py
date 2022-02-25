from rq import Connection, Queue
from redis import Redis


import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

redis_conn = Redis()
q = Queue(connection=redis_conn)
job = q.enqueue(count_words_at_url, 'http://nvie.com')
print(job)