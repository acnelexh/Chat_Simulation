from openai import OpenAI
from engine import Engine
from pathlib import Path
import time
import argparse
    

def create_output_dir(output_dir: Path):
    # glob all dir
    all_dir = [x for x in output_dir.glob("*") if x.is_dir()]
    # get max index
    max_index = 0
    for dir in all_dir:
        try:
            max_index = max(max_index, int(dir.name))
        except:
            pass
    # create new dir
    output_dir = output_dir / str(max_index + 1)
    return str(output_dir)

def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", type=str, default=None, help="resume simulation")
    parser.add_argument("--save_dir", type=str, default=f'{create_output_dir(Path("output"))}', help="save directory")
    args = parser.parse_args()
    # init engine
    engine = Engine(args.save_dir, Path(args.resume) if args.resume is not None else None)
    # start simulation
    engine.start()
  
if __name__ == "__main__":
    main()