from openai import OpenAI

client = OpenAI(api_key="")
def gpt_process(string_value):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a English teacher, explain the answer in easy words"},
        {"role": "user", "content": string_value}
    ]
    )

    return str(completion.choices[0].message.content)