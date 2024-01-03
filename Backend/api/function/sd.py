

# 封裝 OpenAI 相關操作
class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_sentence(self, word_input):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an English teacher."},
                {"role": "user", "content": f"Craft a vivid sentence focusing on '{word_input}', ensuring a clear understanding of its meaning (within 15 words)."}
            ],
            max_tokens=30
        )
        
        return response
# 初始化 OpenAI 客户端
openai_client = OpenAIClient(api_key="sk-n2NyHG6Z2CUdEY3CeORAT3BlbkFJ2WbBGga2RuHTvGMZtVN")

class SentenceAPIView(APIView):
    def post(self, request):
        serializer = SentenceSerializer(data=request.data)
        if serializer.is_valid():
            word_input = serializer.validated_data['word']

            # 檢查資料庫中是否已存在句子
            try:
                word_sentence = WordSentence.objects.get(word=word_input)
                generated_sentence = word_sentence.sentence
                print(f"句子 '{generated_sentence}' 已經存在，無需再次生成。")
                serializer = SentenceSerializer(word_sentence)
                return Response({"status": "success", "sentence": serializer.data})
            except WordSentence.DoesNotExist:
                pass

            # 使用 OpenAI API 生成句子
            response = openai_client.generate_sentence(word_input)
            generated_sentence = response.choices[0].message.content

            # 保存生成的句子到資料庫
            WordSentence.objects.create(word=word_input, sentence=generated_sentence)
            print(f"Generated Sentence: {generated_sentence}")

            serializer = SentenceSerializer({'word': word_input, 'sentence': generated_sentence})
        
            return Response({"status": "success", "sentence": serializer.data})
        else:
            return Response({"status": "error", "message": serializer.errors}, status=400)

class ImageAPIView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            word_input = serializer.validated_data['word']
            sentence_input = serializer.validated_data['sentence']

            # 檢查資料庫中是否已存在圖片
            try:
                word_image = WordImage.objects.get(word=word_input)
                image_url = word_image.image.name
                print(f"圖片 '{image_url}' 已經存在，無需再次生成。")
                serializer = ImageSerializer(word_image)
                return Response({"status": "success", "image": serializer.data})
            except WordImage.DoesNotExist:
                pass

            # 使用外部 API 生成圖片
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
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            image_url = response_data.get("output")[0] if "output" in response_data else None

            if image_url:
                # 保存到資料庫
                WordImage.objects.create(word=word_input, image=f'word_images/{word_input}.png')
                serializer = ImageSerializer({'word': word_input, 'image': f'word_images/{word_input}.png'})
                return Response({"status": "success", "image": serializer.data})
            else:
                return Response({"status": "error", "message": "生成失敗"})
        else:
            return Response({"status": "error", "message": serializer.errors}, status=400)