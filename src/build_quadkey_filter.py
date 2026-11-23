"""Building the list of zoom-8 quadkeys covering Cameroon.

Used later to keep only tiles near Cameroon when reading
Ookla's global files.
"""
import json
from pathlib import Path
import yaml
import geopandas as gpd
import mercantile
from shapely.geometry import box

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

INTERIM = ROOT / config["paths"]["interim"]
ZOOM = config["ookla"]["filter_zoom"]

departments = gpd.read_file(INTERIM / "departments.geojson")
country = departments.geometry.union_all()   # one shape for all of Cameroon

west, south, east, north = departments.total_bounds
print(f"Bounding box: lon {west:.2f} to {east:.2f}, lat {south:.2f} to {north:.2f}")

# All zoom-8 squares touching the bounding box
candidates = list(mercantile.tiles(west, south, east, north, zooms=ZOOM))

# We Keep only squares that touch Cameroon itself, not just its bounding box
kept = []
for t in candidates:
    b = mercantile.bounds(t)
    if box(b.west, b.south, b.east, b.north).intersects(country):
        kept.append(mercantile.quadkey(t))

kept = sorted(kept)

# Checks
assert all(len(q) == ZOOM for q in kept), "Unexpected quadkey length"
assert len(set(kept)) == len(kept), "Duplicate quadkeys"

out = INTERIM / f"cameroon_quadkeys_z{ZOOM}.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(kept, f, indent=2)

print(f"Squares in bounding box: {len(candidates)}")
print(f"Squares touching Cameroon: {len(kept)}")
print(f"Saved to {out.name}")