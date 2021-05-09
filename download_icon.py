from argparse import ArgumentParser
from pathlib import Path
from os import PathLike
from platform import system
from sys import argv
from urllib.request import urlopen
from PIL import Image


def download_icon(icon_url: str, destination_path: PathLike) -> None:
    if system() == "Windows" and not Path(destination_path).suffix.lower() == ".ico":
        raise ValueError("Windows only supports .ico icons")

    with urlopen(icon_url) as response:
        Image.open(response).save(Path(destination_path))

if __name__ == "__main__":
    parser = ArgumentParser(description="Downloads and converts an image file to an icon file")
    parser.add_argument("url", help="URL of an image file to convert")
    parser.add_argument("destination", help="Path to save converted icon file to")

    args = parser.parse_args(argv[1:])
    
    
    download_icon(args.url, args.destination)
