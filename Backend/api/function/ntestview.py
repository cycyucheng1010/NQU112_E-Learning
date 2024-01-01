

client = OpenAI(api_key="sk-n2NyHG6Z2CUdEY3CeORAT3BlbkFJ2WbBGga2RuHTvGMZtVN")

@api_view(['POST'])
def generate_sentence(request):
    try:
        data = request.data
        word_input = data.get('word')
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a English teacher."},
                {"role": "user", "content": f"Craft a vivid sentence focusing on '{word_input},' ensuring a clear understanding of its meaning (within 15 words)."}
            ],
            max_tokens=30
        )

        generated_sentence = response.choices[0].message.content

        return JsonResponse({"status": "success", "sentence": generated_sentence})
        
    except Exception as e:
        traceback.print_exc() 
        return JsonResponse({"status": "error", "message": str(e)})
#@api_view(['POST'])
#def generate_sentence(request):
#    data = request.data  # 使用 request.data 可以直接解析 JSON 數據
#    word_input = data.get('word')
#    fixed_sentence = "this is a"
##    sentence_input = data.get('sentence')

#    return JsonResponse({"status": "success", "sentence": f"{fixed_sentence} {word_input}"})

##    return JsonResponse({"status": "success", "sentence": f"((({word_input})))"})

#
#@api_view(['POST'])
#def generate_image(request):
#    data = json.loads(request.body)
#    word_input = data.get('word')
#    sentence_input = data.get('sentence')

#    wordpic_folder = "./function/wordpic"
#    os.makedirs(wordpic_folder, exist_ok=True)
#    image_filename = os.path.join(wordpic_folder, f"{word_input}.png")
#
#    if os.path.exists(image_filename):
#        print(f"圖片 '{image_filename}' 已經存在，無需再次生成。")
#        return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

#    prompt = f"{sentence_input.replace(word_input, f'((({word_input})))')}"
#    response = send_api_request(prompt)

#    if response and response.status_code == 200:
#        image_url = extract_image_url(response)

#        if image_url:
#            download_image(image_url, image_filename)
#            return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

#   return JsonResponse({"status": "error", "message": "生成失敗"})

#def send_api_request(prompt):
#    url = "https://stablediffusionapi.com/api/v3/text2img"
#    payload = {
#        "key": "kRdhAtCe7TqcTgUkpoBeWB569nwAO7UnvR3BGvVGBj2zJtKbsapxWka0sPQ2",
#        "prompt": prompt,
#        "width": "512",
#        "height": "512",
#        "samples": "1",
#        "num_inference_steps": "20",
#        "guidance_scale": 7.5,
#       "safety_checker": "yes",
#        "multi_lingual": "no",
#        "panorama": "no",
#        "self_attention": "no",
#        "upscale": "no",
#        "embeddings_model": None,
#        "webhook": None,
#        "track_id": None
#    }

#    headers = {'Content-Type': 'application/json'}

#    return post(url, headers=headers, json=payload)

#def extract_image_url(response):
#    response_data = response.json()
#    return response_data.get("output")[0] if "output" in response_data else None

#def download_image(image_url, image_filename):
#    response_image = get(image_url)
#    with open(image_filename, 'wb') as img_file:
#        img_file.write(response_image.content)

import os
import traceback
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from openai import OpenAI
from requests import post, get  # 导入 post 和 get 模块

# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-n2NyHG6Z2CUdEY3CeORAT3BlbkFJ2WbBGga2RuHTvGMZtVN")

# 定义文件路径
word_sentence_folder = "./function/wordsentence"
word_pic_folder = "./function/wordpic"

# 确保目录存在
os.makedirs(word_sentence_folder, exist_ok=True)
os.makedirs(word_pic_folder, exist_ok=True)

@csrf_exempt
@api_view(['POST'])
def generate_sentence(request):
    try:
        sentence_list = []

        # 从请求数据中获取单词和句子
        data = request.data
        word_input = data.get('word')
        sentence_input = data.get('sentence')

        # 使用 OpenAI API 生成句子
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an English teacher."},
                {"role": "user", "content": f"Craft a vivid sentence focusing on '{word_input}', ensuring a clear understanding of its meaning (within 15 words)."}
            ],
            max_tokens=30
        )
        
        generated_sentence = response.choices[0].message.content
        sentence_list.append(generated_sentence)

        # 保存生成的句子到文件
        sentence_filename = os.path.join(word_sentence_folder, f"{word_input}.txt")
        with open(sentence_filename, 'w') as file:
            file.write(generated_sentence)

        # 输出生成的句子并返回给前端
        print(f"Generated Sentence: {generated_sentence}")
        
        return JsonResponse({"status": "success", "sentence": generated_sentence})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "error"})


@api_view(['POST'])
def generate_image(request):
    try:
        data = json.loads(request.body)
        word_input = data.get('word')
        sentence_input = data.get('sentence')

        image_filename = os.path.join(word_pic_folder, f"{word_input}.png")

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

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)})

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