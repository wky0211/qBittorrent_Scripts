import time
import json
import requests

#Example
#host = "http://192.168.1.110"

host = ""

class qBittorrent(object):
    def __init__(self, host):
        self.host = host
    
    def get_torrent_list(
        self,
        filter: str = None,
        category: str = None,
        sort:str = None,
        reverse: bool = False,
        limit: int = None,
        offset: int = 0,
        hashes: str = None
    ):
        endpoint = "/api/v2/torrents/info"
        data = {
            "filter": filter,
            "category": category,
            "sort": sort,
            "reverse": reverse,
            "limit": limit,
            "offset": offset,
            "hashes": hashes
        }
        try:
            return json.loads(requests.get(self.host + endpoint, data).text)
        except:
            raise RuntimeError("Cannot connect to qBittorrent server")

    def edit_tracker(
        self,
        hash: str,
        old_url: str,
        new_url: str
    ):
        endpoint = "/api/v2/torrents/editTracker"
        data = {
            "hash": hash,
            "origUrl": old_url,
            "newUrl": new_url
        }
        try:
            return requests.get(self.host + endpoint, data).status_code
        except:
            raise RuntimeError("Cannot connect to qBittorrent server")

client = qBittorrent(host=host)
torrents = client.get_torrent_list()
for torrent in torrents:
    hash = torrent['hash']
    old_tracker = torrent['tracker']
    new_tracker = old_tracker.replace("http://", "https://")
    if "http://" in old_tracker:
        print("----------------------------------")
        print("Name: " + torrent['name'])
        print("Old Tracker: " + old_tracker)
        print("New Tracker: " + new_tracker)
        print("Status: " + str(client.edit_tracker(hash=hash, old_url=old_tracker, new_url=new_tracker)))
        time.sleep(0.5)
        