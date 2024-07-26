import cv2
import numpy as np
import requests
import base64
import os

def remove_background(image_path):
    url = "https://plng-api-utils.photio.io/remove-background"
    headers = {
        "Content-Type": "application/json",
    }
    
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    data = {
        "image": image_base64,
        "url_result_flag": False
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        base64_image = response_data['image']
        
        image_data = base64.b64decode(base64_image)
        
        nparr = np.frombuffer(image_data, np.uint8)
        
        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        
        return image
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 바운딩 박스 가져오기
def get_bounding_box_and_diagonal(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    
    diagonal_length = np.sqrt(w**2 + h**2)
    
    return (x, y, w, h), diagonal_length



def fit_product_b_according_to_a(image_a_shape, image_b, bbox_a, diagonal_length_a):
    x, y, w, h = bbox_a
    
    h_b, w_b = image_b.shape[:2]
    
    diagonal_length_b = np.sqrt(w_b**2 + h_b**2)
    scaling_factor = diagonal_length_a / diagonal_length_b
    
    new_w = int(w_b * scaling_factor)
    new_h = int(h_b * scaling_factor)
    
    if new_w > w or new_h > h:
        scaling_factor = min(w / w_b, h / h_b)
        new_w = int(w_b * scaling_factor)
        new_h = int(h_b * scaling_factor)

    # 이미지 리사이즈
    image_b_resized = cv2.resize(image_b, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # 이미지 B의 위치 계산
    bottom_middle_x = x + w // 2
    bottom_middle_y = y + h
    top_left_x = bottom_middle_x - new_w // 2
    top_left_y = bottom_middle_y - new_h
    
    result_image = np.zeros(image_a_shape, dtype=np.uint8)

    result_image[top_left_y:top_left_y+new_h, top_left_x:top_left_x+new_w] = image_b_resized
    
    return result_image


def process_images(product_a_path, product_b_path, output_folder):
    product_a_no_bg = remove_background(product_a_path)
    if product_a_no_bg is None:
        return
    
    # Read product B image
    product_b = cv2.imread(product_b_path, cv2.IMREAD_UNCHANGED)
    
    # 제품 A의 바운딩 박스와 대각선 길이 계산
    bbox_a, diagonal_length_a = get_bounding_box_and_diagonal(product_a_no_bg)
    
    result_image = fit_product_b_according_to_a(product_a_no_bg.shape, product_b, bbox_a, diagonal_length_a)
    
    os.makedirs(output_folder, exist_ok=True)
    
    output_filename = os.path.splitext(os.path.basename(product_a_path))[0] + "_replaced.png"
    output_path = os.path.join(output_folder, output_filename)
    
    cv2.imwrite(output_path, result_image)
    print(f"Result image saved to {output_path}")


product_a_path = "/Users/james/Downloads/화장품 레퍼런스 (1)/remove-background/3.jpg" # 배경있는 제품 이미지
product_b_path = "/Users/james/Downloads/cosmetic/05ebd4d5-212f-406f-b27a-3ab682838698.png" #배경 없는 다른 제품 이미지
output_folder = "/Users/james/Desktop/result" # 저장할 폴더

process_images(product_a_path, product_b_path, output_folder)
