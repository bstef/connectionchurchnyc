"""Regenerate the single static hero map. Optional maintenance dependency: Pillow.

Map data and tiles: https://www.openstreetmap.org/copyright
The website uses the checked-in WebP and makes no tile requests at runtime.
"""

import io
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

ZOOM = 14
WIDTH, HEIGHT = 650, 740
CENTER = (40.7735, -73.925)
# Location supplied by the site owner in the Connection Church Google Maps link.
CHURCH = (40.7567285, -73.9053766)
OUTPUT = Path(__file__).resolve().parents[1] / 'assets/astoria-location-map.webp'


def project(latitude, longitude):
    """Convert WGS84 coordinates into global Web Mercator tile pixels."""
    world_size = 256 * 2**ZOOM
    x = (longitude + 180) / 360 * world_size
    y = (1 - math.asinh(math.tan(math.radians(latitude))) / math.pi) / 2 * world_size
    return x, y


def fetch_tile(position):
    x, y = position
    url = f'https://tile.openstreetmap.org/{ZOOM}/{x}/{y}.png'
    request = urllib.request.Request(url, headers={
        'User-Agent': 'ConnectionChurchNYC-static-map/1.0 (https://github.com/bstef/connectionchurchnyc)',
    })
    with urllib.request.urlopen(request, timeout=25) as response:
        data = response.read()
    with Image.open(io.BytesIO(data)) as tile:
        if tile.size != (256, 256):
            raise ValueError(f'Unexpected tile dimensions: {tile.size}')
        return x, y, tile.convert('RGB')


def main():
    center_x, center_y = project(*CENTER)
    left, top = round(center_x - WIDTH / 2), round(center_y - HEIGHT / 2)
    min_x, min_y = left // 256, top // 256
    max_x, max_y = (left + WIDTH - 1) // 256, (top + HEIGHT - 1) // 256
    canvas = Image.new('RGB', ((max_x - min_x + 1) * 256, (max_y - min_y + 1) * 256))
    positions = [(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]
    # Fetch only this map's visible tiles, with limited concurrency.
    with ThreadPoolExecutor(max_workers=2) as pool:
        for x, y, tile in pool.map(fetch_tile, positions):
            canvas.paste(tile, ((x - min_x) * 256, (y - min_y) * 256))
    offset_x, offset_y = left - min_x * 256, top - min_y * 256
    canvas = canvas.crop((offset_x, offset_y, offset_x + WIDTH, offset_y + HEIGHT))
    canvas.save(OUTPUT, quality=90)
    pin_x, pin_y = project(*CHURCH)
    # Use these percentages in .hero-map-pin if changing the map framing.
    print(json.dumps({
        'pin_left_percent': (pin_x - left) / WIDTH * 100,
        'pin_top_percent': (pin_y - top) / HEIGHT * 100,
        'image_dimensions': canvas.size,
    }, indent=2))


if __name__ == '__main__':
    main()
