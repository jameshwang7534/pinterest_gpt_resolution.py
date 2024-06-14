import requests
import json
import os
import urllib
from PIL import Image
from io import BytesIO
from src.check_gpt import is_valid_image

class Scraper:

    def __init__(self, config, image_urls=[]):
        self.config = config
        self.image_urls = image_urls

    # Set config for bookmarks (next page)
    def setConfig(self, config):
        self.config = config

    # Download images
    def download_images(self, keyword):
        # the folder you want to save
        base_folder = "/Users/james/Desktop" #input folder directory
        folder = os.path.join(base_folder, keyword.replace(" ", "_"))
        number = 0
        
        # prev get links
        results = self.get_urls()
        try:
            os.makedirs(folder)
            print("Directory ", folder, " Created ")
        except FileExistsError:
            pass
        
        arr = os.listdir(folder)
        for url in results:
            if str(url.split("/")[-1] + ".jpg") not in arr:
                try:
                    if self.check_image_resolution(url):
                        file_name = url.split("/")[-1] + ".jpg"
                        download_path = os.path.join(folder, file_name)
                        print("Download ::: ", url)
                        urllib.request.urlretrieve(url, download_path)
                        if is_valid_image(download_path):
                            number += 1
                        else:
                            os.remove(download_path)
                            print(f"Invalid image removed: {download_path}")
                except Exception as e:
                    print(e)

    # get_urls return array
    def get_urls(self):
        SOURCE_URL = self.config.source_url
        DATA = self.config.image_data
        URL_CONSTANT = self.config.search_url
        
        r = requests.get(URL_CONSTANT, params={
            "source_url": SOURCE_URL, "data": DATA
        })
        jsonData = json.loads(r.content)
        resource_response = jsonData["resource_response"]
        data = resource_response["data"]
        results = data["results"]
        
        for i in results:
            self.image_urls.append(i["images"][self.config.image_quality]["url"])

        if len(self.image_urls) < int(self.config.file_length):
            self.config.bookmarks = resource_response["bookmark"]
            print("Creating links", len(self.image_urls))
            self.get_urls()
        
        return self.image_urls[0:self.config.file_length]

    # fix resolution
    def check_image_resolution(self, url):
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            #input resolution here
            if width >= 500 and height >= 500:
                return True
            else:
                print(f"Image skipped due to resolution: {width}x{height}")
                return False
        except Exception as e:
            print(f"Error checking image resolution: {e}")
            return False
