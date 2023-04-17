import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from utils import scroll_to_page_end, extract_comments_data

driver = webdriver.Chrome()
url = "https://www.youtube.com/watch?v=zghBofrKv7s&ab_channel=EhmadZubair"
driver.get(url)

scroll_to_page_end(driver)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

comments_data = extract_comments_data(soup)

driver.quit()

video_title = soup.title.string

file_name = f"{video_title}.csv"

df = pd.DataFrame(comments_data, columns=['User Name', 'Thumbnail URL', 'Comment Time', 'Likes', 'Comment Text'])
df.to_csv(file_name, index=False)

print("Data successfully saved to CSV file.")
