import os
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from utils import scroll_to_page_end, extract_comments_data, get_channel_directory, get_video_links


channel_url = input("Enter the URL of the YouTube channel: ")
channel_url += "/videos"

driver = webdriver.Chrome()
driver.get(channel_url)

time.sleep(5)

scroll_to_page_end(driver)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

channel_dir = get_channel_directory(channel_url)
video_links = get_video_links(soup)

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
