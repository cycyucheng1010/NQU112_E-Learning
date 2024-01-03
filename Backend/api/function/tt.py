
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
        
        sentence_filename = os.path.join(word_sentence_folder, f"{word_input}.txt")

        if os.path.exists(sentence_filename):
            with open(sentence_filename, 'r') as file:
                generated_sentence = file.read()
                print(f"句子 '{generated_sentence}' 已經存在，無需再次生成。")
                return JsonResponse({"status": "success", "sentence": generated_sentence})

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

import requests
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
        response = post(url, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            image_url = response_data.get("output")[0] if "output" in response_data else None

            if image_url:
                # 直接在 generate_image 函數中下載圖片
                image_filename = os.path.join(word_pic_folder, f"{word_input}.png")
                response_image = get(image_url)

                with open(image_filename, 'wb') as img_file:
                    img_file.write(response_image.content)

                return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

        return JsonResponse({"status": "error", "message": "生成失敗"})
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)})


from .models import WordSentence

@csrf_exempt
@api_view(['POST'])
def generate_sentence(request):
    try:
        sentence_list = []

        data = request.data
        word_input = data.get('word')
        
        sentence_filename = os.path.join(word_sentence_folder, f"{word_input}.txt")

        if os.path.exists(sentence_filename):
            with open(sentence_filename, 'r') as file:
                generated_sentence = file.read()
                print(f"句子 '{generated_sentence}' 已經存在，無需再次生成。")
                return JsonResponse({"status": "success", "sentence": generated_sentence})

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

        # 保存生成的句子到資料庫
        word_sentence, created = WordSentence.objects.get_or_create(word=word_input)
        word_sentence.sentence = generated_sentence
        word_sentence.save()

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
        response = post(url, headers=headers, json=payload)


        if response.status_code == 200:
            response_data = response.json()
            image_url = response_data.get("output")[0] if "output" in response_data else None

            if image_url:
                # 保存到資料庫
                word_image, created = WordImage.objects.get_or_create(word=word_input)
                word_image.image.name = f'word_images/{word_input}.png'
                word_image.save()

                # 直接在 generate_image 函數中下載圖片
                image_filename = os.path.join(word_pic_folder, f"{word_input}.png")
                response_image = get(image_url)

                with open(image_filename, 'wb') as img_file:
                    img_file.write(response_image.content)

                return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

        return JsonResponse({"status": "error", "message": "生成失敗"})
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)})


