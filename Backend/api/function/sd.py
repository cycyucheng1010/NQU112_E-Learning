import os
import requests
import json

def generate_image(word, sentence, wordpic):
    # 1. 檢查是否已經生成過圖片
    image_filename = os.path.join(wordpic, f"{word}.png")
    if os.path.exists(image_filename):
        print(f"圖片 '{image_filename}' 已經存在，無需再次生成。")
        return

    # 2. 根據輸入的單字和句子生成 prompt
    prompt = f"{sentence.replace(word, f'((({word})))')}"

    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = json.dumps({
        "key": "kRdhAtCe7TqcTgUkpoBeWB569nwAO7UnvR3BGvVGBj2zJtKbsapxWka0sPQ2",
        "prompt": prompt,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
    })

    headers = {
        'Content-Type': 'application/json'
    }

    # 3. 發送 API 請求
    response = requests.request("POST", url, headers=headers, data=payload)

    # 4. 檢查狀態碼是否為成功
    if response.status_code == 200:
        response_data = response.json()
        image_url = response_data.get("output")[0]

    if image_url:
    # 5. 下載圖片到指定資料夾
        response_image = requests.get(image_url)
        with open(image_filename, 'wb') as img_file:
            img_file.write(response_image.content)

    print("Generated Image URL:", image_url)
## wb=word binary以二進位方式處理文件，這在處理像圖片不會對數據進行任何文本編碼轉換，而是將原始的二進位數據直接寫入文件。
# 6. 測試
def main():
    word_input = input("請輸入單字: ")
    sentence_input = input("請輸入句子: ")

    # 指定目標資料夾
    wordpic = "./function/wordpic"

    # 7. 增加判定，如果已生成過圖片，不再重複生成
    generate_image(word_input, sentence_input, wordpic)

if __name__ == "__main__":
    main()








from openai import OpenAI

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.decorators import action
import traceback
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
import os
'''
client = OpenAI(
    api_key=os.environ.get("sk-n2NyHG6Z2CUdEY3CeORAT3BlbkFJ2WbBGga2RuHTvGMZtVN"),
)'''
client = OpenAI(api_key="sk-n2NyHG6Z2CUdEY3CeORAT3BlbkFJ2WbBGga2RuHTvGMZtVN")

#class GPTView(APIView): 
class GPTView(viewsets.ViewSet): 
    @csrf_exempt
    @action(detail=False, methods=['GET','POST'], url_path='gpt')
    def gpt (self, request):
        if request.method =='POST':
            try:
                list = []
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=[
                        {"role": "system", "content": "You are a English teacher."},
                        {"role": "user", "content": "Craft a vivid sentence focusing on 'tea,' ensuring a clear understanding of its meaning (within 15 words)."}
                    ],
                    max_tokens=30
                )
                
                data = response.choices[0].message.content
                sentence_list.append(data)

                # Print the sentence and output to sentence_input
                print(f"Sentence: {data}")
                sentence_input = data  # 賦值給 sentence_input 或進行其他處理

                return JsonResponse({"msg": "success", "data": sentence_list})

            except Exception as e:
                traceback.print_exc()
                return JsonResponse({"msg": "error"})

#gpt_view = GPTView.as_view()



@api_view(['POST'])
def generate_sentence(request):
    data = request.data  # 使用 request.data 可以直接解析 JSON 數據
    word_input = data.get('word')

    sentence_input = data.get('sentence')



    return JsonResponse({"status": "success", "sentence": f"((({word_input})))"})


@api_view(['POST'])
def generate_image(request):
    data = json.loads(request.body)
    word_input = data.get('word')
    sentence_input = data.get('sentence')

    wordpic_folder = "./function/wordpic"
    os.makedirs(wordpic_folder, exist_ok=True)
    image_filename = os.path.join(wordpic_folder, f"{word_input}.png")

    if os.path.exists(image_filename):
        print(f"圖片 '{image_filename}' 已經存在，無需再次生成。")
        return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

    prompt = f"{sentence_input.replace(word_input, f'((({word_input})))')}"
    response = send_api_request(prompt)

    if response and response.status_code == 200:
        image_url = extract_image_url(response)

        if image_url:
            download_image(image_url, image_filename)
            return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

    return JsonResponse({"status": "error", "message": "生成失敗"})

def send_api_request(prompt):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    payload = {
        "key": "kRdhAtCe7TqcTgUkpoBeWB569nwAO7UnvR3BGvVGBj2zJtKbsapxWka0sPQ2",
        "prompt": prompt,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
    }

    headers = {'Content-Type': 'application/json'}

    return post(url, headers=headers, json=payload)

def extract_image_url(response):
    response_data = response.json()
    return response_data.get("output")[0] if "output" in response_data else None

def download_image(image_url, image_filename):
    response_image = get(image_url)
    with open(image_filename, 'wb') as img_file:
        img_file.write(response_image.content)

