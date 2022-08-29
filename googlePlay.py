from google_play_scraper import Sort, reviews
from adapter_rate_item import AdapterRateItem
from review import Review
from datetime import datetime
from google_play_scraper import app
from urllib.parse import urlparse
import ssl
import http.client
import json
import sys

errMessage = (
    "Argument error ex:python googlePlay.py PACKAGE_NAME REVIEW_COUNT WEBHOOK_URL"
)

if len(sys.argv) != 4:
    raise IndexError(errMessage)

PACKAGE_NAME = sys.argv[1]
REVIEW_COUNT = int(sys.argv[2])
WEBHOOK_URL = sys.argv[3]
o = urlparse(WEBHOOK_URL)
DOMAIN = o.netloc
PATH = o.path

ssl._create_default_https_context = ssl._create_unverified_context

appInfoResult = app(
    PACKAGE_NAME,
    lang="zh_TW",  # defaults to 'en'
    country="tw",  # defaults to 'us'
)

# broken can't fetch title
# appTitle = appInfoResult["title"]
# print("App:" + appTitle)
print("Scrapy reviews...")

result, continuation_token = reviews(
    PACKAGE_NAME,
    lang="zh_TW",  # defaults to 'en'
    country="tw",
    sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
    count=REVIEW_COUNT,  # defaults to 100
    filter_score_with=None,  # defaults to None(means all score)
)

# result, _ = reviews(
#     PACKAGE_NAME,
#     # defaults to None(load from the beginning)
#     continuation_token=continuation_token,
# )

print("Scrapy reviews done.")

adapterRateItem = AdapterRateItem()


def postPayload(payload):
    conn = http.client.HTTPSConnection(DOMAIN)
    headers = {"Content-Type": "application/json"}
    conn.request(
        "POST",
        PATH,
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


print("Prepare post to Teams...")
reviewsItem = []
for item in result:
    userName = item.get("userName")
    userImage = item.get("userImage")
    content = item.get("content")
    score = item.get("score")
    appVersion = item.get("reviewCreatedVersion")
    at = item.get("at")
    atStr = datetime.strftime(at, "%Y-%m-%d %H:%M:%S")
    review = Review(userName, userImage, content, score, appVersion, atStr)
    print(review)
    adapter = adapterRateItem.generateRateAdapter(review)
    reviewsItem.append(adapter)

payload = json.dumps(adapterRateItem.generateRate(reviewsItem))
postPayload(payload)
print("Post to Teams done.")
