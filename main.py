from openai import OpenAI
from engine import Engine
from pathlib import Path
import time
import argparse
    

def main():
    # parse args
    time_now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", type=str, default=None, help="resume simulation")
    parser.add_argument("--save_dir", type=str, default=f'output/{time_now}', help="save directory")
    args = parser.parse_args()
    # init engine
    engine = Engine(args.save_dir, Path(args.resume) if args.resume is not None else None)
    # start simulation
    engine.start()
  
if __name__ == "__main__":
    main()