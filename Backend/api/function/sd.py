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
