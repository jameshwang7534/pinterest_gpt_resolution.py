
from src import PinterestScraper, PinterestConfig

configs = PinterestConfig(search_keywords="food product", # input Search word
                          file_lengths=5,     # total number of images to scan and filter(doesn't mean you download this much image) (default = "100")
                          image_quality="orig", # image quality (default = "orig")
                          bookmarks="")         # next page data (default= "")


PinterestScraper(configs).download_images("lol")     # folder name you want to create in your directory
print("done processing!!!!!-----------------------!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!")
#print(PinterestScraper(configs).get_urls())     # just bring image links
