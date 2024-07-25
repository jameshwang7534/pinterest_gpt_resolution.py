
## 1. 설명
  -핀터레스트에서 이미지를 스캔하면서 resolution 및 gpt 로 필터링을 거친후 저장하는 프로그램, 사진은 검색 키워드로 생성된 폴더에 저장됨.

## 2. 사용 방법
  -main.py 에서 keyword는 크롤링 하고 싶은 검색 키워드, base_folder는 저장하고 싶은 폴더 위치를 입력.
  -file_length는 스캔하고 싶은 이미지 갯수 입력 *스캔하는 이미지 숫자이지 다운해야되는 이미지 숫자 X, 필터링 조건이 엄격할수록 사진이 덜 저장됨.
  -설정 후 main.py 실행
  
## 3. gpt 필터링 값 조정

![image](https://github.com/user-attachments/assets/79a1cae7-5db3-426b-b59c-acc9c1fa1548)
  - /src/check_gpt.py 파일에 들어가서 make_payload 함수의 content 부분을 gpt에게 필터링을 해주고 싶은대로 수정한다. 답은 boolean으로 제공하도록 한다.

![image](https://github.com/user-attachments/assets/7033faa2-49f0-486b-bbd5-28ddf6810752)
  - /src/check_gpt.py 파일의 evaluate_conditions 함수에서 변수들을 선언하고 boolean true/false에 맞게 리턴값을 조절한다.
  - 리턴값이 true일때만 해당 이미지를 저장한다

## 4. resolution 필터링 값 조정

![image](https://github.com/user-attachments/assets/ca795988-e176-46c5-96b0-4d9f6eb56af3)

  -/src/scraper.py 파일에 들어가서 check_image_resolution 함수의 width 와 height를 원하는 resolution 값으로 조절하면 된다. 입력한 width나 height보다 큰 값들의 이미지들만 저장한다.


