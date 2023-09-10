from .templates import classes
from typing import Union
from PIL import Image
import io
import base64
import gzip
import io

def decode(raw:Union[str, io.TextIOWrapper]) -> Image:
    if isinstance(raw, str):
        raw = open(raw, "r").read()
    elif isinstance(raw,io.TextIOWrapper):
        raw = raw.read()
    # print(raw)
    metadata, pixels = raw.split("\n\n")
    rawData=metadata.split("\n")
    data = {}
    
    parsedLines = [x.split(": ") for x in rawData]
    for a in parsedLines:
        data[a[0]] = a[1]
    if not ("Width" in data.keys() and "Height" in data.keys()):
        raise KeyError("Height or width missing in OPG file. Make sure the file is an OPG file, it is not corrupted and the data is properly capitalized")
    
    if "Base64" in data.keys():
       if data["Base64"] == "1":
           pixels = base64.b64decode(pixels)
    if "Gzip" in data.keys():
        if data["Gzip"] == "1":
            pixels = gzip.decompress(pixels).decode()
            
            
    img = Image.new("RGB", (int(data["Width"]), int(data["Height"])))
    rawPixels = pixels.split(" ")
    pixels = [x.split(",") for x in rawPixels]
    currentwidth = 0
    currentheight = 0
    

    for x in pixels:
        if currentwidth == int(data["Width"]):
            currentwidth = 0
            currentheight += 1
        img.putpixel((currentwidth, currentheight), (int(x[0]), int(x[1]), int(x[2])))
        currentwidth += 1
    return img

def encode(img:Union[bytes,io.TextIOWrapper,str]) -> str:
    
    if isinstance(img, bytes):
        img = Image.frombytes(img)
    elif isinstance(img,io.TextIOWrapper):
        img = Image.open(img.name)
    elif isinstance(img,str):
        img = Image.open(img)
    pixels = []
    w = img.width
    h = img.height
    metadata = {"Width": w, "Height": h, "Base64": "1", "Gzip": "1"}
    data = [f"{x}: {metadata[x]}" for x in metadata]
    for x in img.getdata():
        pixels.append(f"{x[0]},{x[1]},{x[2]}") 
    imgbody = "\n".join(data) + "\n\n"
    pixelsbody = str(" ".join(pixels))
    pixelsbody = gzip.compress(pixelsbody.encode())
    print(pixelsbody)
    pixelsbody = base64.b64encode(pixelsbody).decode()
    imgbody += pixelsbody
    return imgbody
