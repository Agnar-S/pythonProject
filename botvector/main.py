import requests

url = "http://localhost:8005/stream/"


def test():
    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(None, decode_unicode=True):
            if chunk:
                print(chunk, end='', flush=True)


test()
