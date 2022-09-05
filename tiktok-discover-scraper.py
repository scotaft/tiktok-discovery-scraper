import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

# Connect to Data
file = 'urls.csv'
urls = pd.read_csv(file)
urls = urls.iloc[:,0].values.tolist()

# Check number of URLs
len(urls)

# Check response of URLs
code_count = 0
code_error_count = 0
for url in urls:
    response = requests.get(url)
    if response.ok:
        code_count +=1
    else:
        code_error_count +=1
    time.sleep(5)
print('Success: '+str(code_count))
print('Errors: '+str(code_error_count))

# Scrape video list
discover_urls = []
VideoTitles = []
VideoLinks = []
VideoLikes = []
VideoViews = []
VideoUserNames = []
VideoCommentCount = []
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    DivVideoSection = soup.find('div',{"class":"tiktok-dtihlr-DivVideoSection"})
    VideoCovers = soup.findAll('div',{"class":"tiktok-1njxovi-DivCover"})
    for v in VideoCovers:
        discover_urls.append(url)
        VideoTitles.append(v.get("title"))
    for a in DivVideoSection.findAll('a',{"class":"tiktok-1rzor5f-StyledVideoLink"}):
        VideoLinks.append("https://www.tiktok.com" + a.get('href'))
    for l in DivVideoSection.findAll('strong',{"class":"tiktok-ksk56u-StrongLikes"}):
        VideoLikes.append(l.contents[0])
    for v in DivVideoSection.findAll('span',{"class":"tiktok-16f548v-SpanViews"}):
        VideoViews.append(v.contents[0])
    for u in DivVideoSection.findAll('h3',{"data-e2e":"video-user-name"}):
        VideoUserNames.append(u.contents[0])
    time.sleep(5)

# Create DataFrame for video list output
df = pd.DataFrame({
    "discover_url": discover_urls,
    "VideoTitle": VideoTitles,
    "VideoLink": VideoLinks,
    "VideoLikes": VideoLikes,
    "VideoViews": VideoViews,
    "VideoUserName": VideoUserNames
})

# Publish video list DataFrame to csv
df.to_csv('exports/tiktok_videos.csv')

# Scrape page global data
discovery_urls = []
KeywordTitles = []
KeywordViews = []
KeywordDesc = []
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    discovery_urls.append(url)
    KeywordTitles.append(soup.find('h1',{"data-e2e":"keyword-name"}).contents[0])
    KeywordViews.append((soup.find('h2',{"data-e2e":"keyword-vv"}).contents[0]).replace(" views",""))
    KeywordDesc.append(soup.find('h2',{"data-e2e":"keyword-desc"}).contents[0])
    time.sleep(5)
    
# Create DataFram for page global data
Page_df = pd.DataFrame({
    "discovery_url": discovery_urls,
    "KeywordTitle": KeywordTitles,
    "KeywordViews": KeywordViews,
    "KeywordDescription": KeywordDesc
})

# Publish page global data to csv
Page_df.to_csv('exports/tiktok_pages.csv')
