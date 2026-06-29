import os
from dotenv import load_dotenv
from openai import OpenAI

# runtime vars
running = True
messages = [{"role": "system", "content": "When the user asks to end the chat write /end to let the system know the user requested to end the chat"}]
model = "gemma"

# load vars from env file
load_dotenv()

# set up openai client
client = OpenAI(
    api_key=os.environ["NRP_LLM_TOKEN"],
    base_url=os.environ["NRP_LLM_BASE_URL"],
)

print(f"Welcome to chatbox. My name is {model}. How can I help?")
print(f"When you want to end the chat tell {model} that you would like to end the chat.")
while running:
    user_input = input("you: ")
    messages.append({"role": "user", "content": user_input})
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    print(f"{model}: ", end="", flush=True)
    
    collected_chunks = []
    for chunk in stream:
        content = None
        if len(chunk.choices) > 0:
            content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
            collected_chunks.append(content)
    response = "".join(collected_chunks)
    print()
            
    messages.append({"role": "assistant", "content": response})
    
    if (response.endswith("/end")):
        print(f"{model} has ended the chat")
        running = False