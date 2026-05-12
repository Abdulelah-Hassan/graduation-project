from openai import OpenAI

def NLPResponse(details):
    null = None
    false = False
    true = True

    dct = details


    client = OpenAI(api_key="SET YOUR API KEY HERE", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Of course! Please provide the JSON text that describes the Instagram account, and I'll analyze it for you. I'll look at factors"},
            {"role": "user", "content": "(Keep it short, tell me how much trusted is, red/green flags, Use HTML format)\n\n" + str(dct)},
        ],
        stream=False
    )

    return response.choices[0].message.content