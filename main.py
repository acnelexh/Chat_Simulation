from openai import OpenAI
from engine import Engine
from pathlib import Path
import time


# client = OpenAI()

# # tmp
# CONTENT_SYSTEM = "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."
# CONTENT_USER = "Compose a poem that explains the concept of recursion in programming."

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": CONTENT_SYSTEM},
#     {"role": "user", "content": CONTENT_USER}
#   ]
# )

# # check output dir 
# output_dir = Path("output")
# if output_dir.exists() == False:
#   output_dir.mkdir()
# with open(output_dir / f"chat_{time.time()}.json", "w") as f:
#   f.write(completion.json())

# print(completion.choices[0].message.content)

def main():
    # init engine
    engine = Engine(save_dir="output")
    # start simulation
    engine.start()
  
if __name__ == "__main__":
    main()