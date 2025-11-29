import anthropic

'''
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: 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" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data \
'{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
'''

client = anthropic.Anthropic(
    api_key="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"  # 실제 키로 교체
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=20000,
    temperature=1,
    messages=[]
)
print(message.content)