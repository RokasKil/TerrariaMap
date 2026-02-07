import os
import re
import pyvips

TILES_DIR = "tiles"
OUTPUT_DIR = "output_tiles"
TILE_SIZE = 256

FILENAME_RE = re.compile(r"(-?\d+)-(-?\d+)\.(png|jpg|jpeg)", re.IGNORECASE)

# -------------------------------------------------------------------
# Load images and parse coordinates
# -------------------------------------------------------------------
entries = []

for fname in os.listdir(TILES_DIR):
    match = FILENAME_RE.match(fname)
    if not match:
        continue

    gx = int(match.group(1))
    gy = int(match.group(2))
    path = os.path.join(TILES_DIR, fname)

    img = pyvips.Image.new_from_file(path, access="sequential")

    if img.bands == 3:
        img = img.bandjoin(255)

    entries.append({
        "gx": gx,
        "gy": gy,
        "img": img,
        "file": fname
    })

if not entries:
    raise RuntimeError("No valid tiles found")

# -------------------------------------------------------------------
# Group into rows by Y coordinate
# -------------------------------------------------------------------
rows = {}
for e in entries:
    rows.setdefault(e["gy"], []).append(e)

sorted_ys = sorted(rows.keys())

# -------------------------------------------------------------------
# Compute world positions
# -------------------------------------------------------------------
current_y = 0
placements = []
world_width = 0

for gy in sorted_ys:
    row = rows[gy]
    row.sort(key=lambda e: e["gx"])

    current_x = 0
    row_height = 0

    for e in row:
        placements.append({
            "img": e["img"],
            "x": current_x,
            "y": current_y
        })

        # There is a two block overlap hence the -2*16
        current_x += e["img"].width - 2 * 16
        row_height = max(row_height, e["img"].height - 2 * 16)

    world_width = max(world_width, current_x)
    current_y += row_height

world_height = current_y

print(f"World size inferred: {world_width} x {world_height}")

# -------------------------------------------------------------------
# Composite into world image
# -------------------------------------------------------------------
world = pyvips.Image.black(world_width, world_height, bands=4)
world = world.copy(interpretation="srgb")
world = world.new_from_image([0, 0, 0, 0]) 
for p in placements:
    world = world.composite(
        p["img"],
        mode="over",
        x=p["x"],
        y=p["y"]
    )

# -------------------------------------------------------------------
# Generate tile pyramid
# -------------------------------------------------------------------
print("Generating tile pyramid...")
world.dzsave(
    OUTPUT_DIR,
    layout="google",
    tile_size=TILE_SIZE,
    overlap=0,
    suffix=".png",
    background=[0, 0, 0, 0]
)

print("Done.")
