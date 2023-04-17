import os
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from utils import scroll_to_page_end, extract_comments_data


channel_url = input("Enter the URL of the YouTube channel: ")
channel_url += "/videos"

channel_name = channel_url.split("/")[-2].replace('@', '')
channel_dir = os.path.join(os.getcwd(), channel_name)
if not os.path.exists(channel_dir):
    os.mkdir(channel_dir)

driver = webdriver.Chrome()
driver.get(channel_url)

time.sleep(5)

scroll_to_page_end(driver)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

video_links = []
for video in soup.find_all('ytd-rich-grid-media'):
    video_url = 'https://www.youtube.com' + video.find('a', {'id': 'video-title-link'}).get('href')
    video_links.append(video_url)

for video_link in video_links:
    driver.get(video_link)

    time.sleep(5)

    scroll_to_page_end(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    comments_data = extract_comments_data(soup)

    video_name = soup.title.string.split(" - YouTube")[0]
    video_title = video_name.replace('/', '-')

    file_name = video_title + '.csv'
    file_path = os.path.join(channel_dir, file_name)
    df = pd.DataFrame(comments_data, columns=['User Name', 'Thumbnail URL', 'Comment Time', 'Likes', 'Comment Text'])
    df.to_csv(file_path, index=False)
    print(f"Comments for video {video_title} saved to CSV file {file_name}")

driver.quit()

print("Data successfully saved to CSV file.")
