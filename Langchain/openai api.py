TEMPERATURE: float = 2.0
MAX_TOKENS: int = 2000
TOP_P: float = 0.1
FREQUENCY_PENALTY: float = 1
PRESENCE_PENALTY: float = -1
MODEL_NAME: str = "gpt-3.5-turbo"


prompt: str = "Make short workout plan, that is one hour long"

completion = client.chat.completions.create(
  model=MODEL_NAME,
  messages=[
    {"role": "system", "content": "You are a personal trainer. add '\n' after every '.' ."},
    {"role": "user", "content": "Create a limerick about Large Language Models"}
  ]
)
completion = client.chat.completions.create(
  model=MODEL_NAME,
  temperature=TEMPERATURE,
  frequency_penalty=FREQUENCY_PENALTY,
  presence_penalty=PRESENCE_PENALTY,
  messages=[
    {"role": "user", "content": f"{prompt} add '\n' after every '.'"}
  ],
)

output = completion.choices[0].message.content
print(f"The Model responded with: '{output}'")