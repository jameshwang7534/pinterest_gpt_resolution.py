import base64
import json
import requests
import time

api_key = "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"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# change the prompt you want to ask gpt 
def make_payload(image_base64):
    return {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Look at this product image and answer the following questions:
                        1. Does the image contain a human?
                        2. Is the image a photo grid or a photo collage?
                        3. Does the image clearly show a product?
                        Provide the answers in the following JSON format:
                        {
                            "contains_human": boolean,
                            "composition_photo": boolean,
                            "product_clearly_shown": boolean
                        }
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

def request_info(image_base64):
    payload = make_payload(image_base64)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()

def get_product_info_from_image(image_path):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    max_retries = 3
    for attempt in range(max_retries):
        try:
            json_response = request_info(image_base64)
            json_str = json_response['choices'][0]['message']['content'].strip()
            return evaluate_conditions(json_str)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(3)  # Wait for 3 seconds before retrying
            else:
                print(f"Retry failed after {max_retries} attempts: {e}")
                return False

# add json value here according to your prompt
def evaluate_conditions(json_str):
    json_string = json_str.replace('\n','').replace('```json','').replace('```','').replace('\\','')
    parsed_dict = json.loads(json_string)
    contains_human = parsed_dict['contains_human']
    composition_photo = parsed_dict['composition_photo']
    product_clearly_shown = parsed_dict['product_clearly_shown']
    
    return not contains_human and not composition_photo and product_clearly_shown

def is_valid_image(image_path):
    return get_product_info_from_image(image_path)
