
from src import PinterestScraper, PinterestConfig
import time

keyword = "winter" # 검색 키워드
base_folder = "/Users/james/Desktop/temp" #저장하고 싶은 폴더 위치
configs = PinterestConfig(search_keywords=keyword, # input Search word
                          file_lengths=100,     # 스캔하고 필터링할 이미지 갯수(이만큼을 다운한다는건 아님) (default = "100")
                          image_quality="orig", 
                          bookmarks="")         
start = time.time()

PinterestScraper(configs).download_images(keyword, base_folder) 

end = time.time()

processing_time = end - start

print(f"took {processing_time:.2f} to finish crawling process")


