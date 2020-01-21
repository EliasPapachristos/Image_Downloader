import os
import json
# If you have problems with "requests" and "bs4" just
# pip3 install
import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML

# user can input a topic and a number
# download first n images from google image search

GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string
# that allows the network protocol peers to identify the application type,
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                  'Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

SAVED_IMAGES_FOLDER = 'images'


def main():
    if not os.path.exists(SAVED_IMAGES_FOLDER):
        os.mkdir(SAVED_IMAGES_FOLDER)
    download_images()


def download_images():
    # ask for user input
    data = input('What images are you looking for? ')
    number_of_images = int(input('How many images do you want? '))

    print(f'You are searching for {number_of_images} images of {data}.')
    print('Start searching...')

    # get url query string
    search_url = GOOGLE_IMAGE + 'q=' + data
    print(search_url)

    # request url, without usr_agent the permission gets denied
    response = requests.get(search_url, headers=usr_agent)
    html = response.text

    # find all divs where class='rg_meta'
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('div', {'class': 'rg_meta'}, limit=number_of_images)

    # extract the link from the div tag
    image_links = []
    for re in results:
        text = re.text  # this is a valid json string
        text_dict = json.loads(text)  # deserialize json to a Python dict
        link = text_dict['ou']
        # image_type = text_dict['ity']
        image_links.append(link)

    print(f'Found {len(image_links)} images')
    print('Start downloading...')

    for i, image_link in enumerate(image_links):
        # open image link and save as file
        response = requests.get(image_link)

        image_name = SAVED_IMAGES_FOLDER + '/' + data + str(i + 1) + '.jpg'
        with open(image_name, 'wb') as file:
            file.write(response.content)

    print('Done')


if __name__ == '__main__':
    main()
