import opglib
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--mode", "-m", type=str, help="mode")
ap.add_argument("-i", "--input", type=str,  help="Input filename")
ap.add_argument("-o", "--output", type=str, help="Output filename")
args = ap.parse_args()
if __name__ == "__main__":
    match args.mode:
        case "encode":
            f = open(args.output, "wb")
            encoded = opglib.encode(args.input)
            f.write(encoded)
            print(f"Finished encoding {args.input} and saved to {args.output}")
        case "decode":
            f = open(args.output, "wb")
            decoded = opglib.decode(args.input)
            decoded.save(args.output)
            print(f"Finished decoding {args.input} and saved to {args.output}")
        case _:
            print("Please specify a valid mode")
        
