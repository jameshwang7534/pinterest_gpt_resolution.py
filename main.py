
from src import PinterestScraper, PinterestConfig
import time

configs = PinterestConfig(search_keywords="kitchen product", # input Search word
                          file_lengths=100,     # total number of images to scan and filter(doesn't mean you download this much image) (default = "100")
                          image_quality="orig", # image quality (default = "orig")
                          bookmarks="")         # next page data (default= "")
start = time.time()

PinterestScraper(configs).download_images("kitchen product")     # folder name you want to create in your directory

end = time.time()

processing_time = end - start

print("done processing!!!!!-----------------------!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!")

print(f"took {processing_time:.2f} to finish crawling process")

#print(PinterestScraper(configs).get_urls())     # just bring image links
