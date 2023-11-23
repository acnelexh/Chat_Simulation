from openai import OpenAI
from engine import Engine
from pathlib import Path
import time

def main():
    # init engine
    engine = Engine(save_dir=f"output/{time.time()}")
    # start simulation
    engine.start()
  
if __name__ == "__main__":
    main()