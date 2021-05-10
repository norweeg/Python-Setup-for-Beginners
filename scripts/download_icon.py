from argparse import ArgumentParser
from io import BytesIO
from os import PathLike
from pathlib import Path
from platform import system
from sys import argv, stderr
from urllib.request import urlopen

from cairosvg import svg2png
from PIL import Image, UnidentifiedImageError


def download_icon(icon_url: str, destination_path: PathLike) -> None:
    if system() == "Windows" and not Path(destination_path).suffix.lower() == ".ico":
        raise ValueError("Windows only supports .ico icons")

    with urlopen(icon_url) as response:
        try:
            Image.open(response).save(Path(destination_path))
        except UnidentifiedImageError:
            buffer = BytesIO()
            svg2png(url=response.url, write_to=buffer)
            Image.open(buffer).save(Path(destination_path))


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Downloads and converts an image file to an icon file"
    )
    parser.add_argument("url", help="URL of an image file to convert")
    parser.add_argument("destination", help="Path to save converted icon file to")

    args = parser.parse_args(argv[1:])

    try:
        download_icon(args.url, args.destination)
    except Exception as e:
        print(f"Failed to download and convert {args.url}", file=stderr)
        exit(1)
