"""Compute population per department from the WorldPop 2025 raster."""
from pathlib import Path
import yaml
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

RAW = ROOT / config["paths"]["raw"] / "population"
INTERIM = ROOT / config["paths"]["interim"]
RASTER = RAW / config["population"]["file"]

if not RASTER.exists():
    raise FileNotFoundError(f"Population raster not found: {RASTER}")

departments = gpd.read_file(INTERIM / "departments.geojson")

with rasterio.open(RASTER) as src:
    assert src.crs.to_epsg() == 4326, f"Unexpected raster CRS: {src.crs}"
    nodata = src.nodata

    # Raster total, read block by block to save memory
    raster_total = 0.0
    for _, window in src.block_windows(1):
        block = src.read(1, window=window, masked=True)
        raster_total += float(block.sum()) if block.count() else 0.0

# Sum of population cells inside each department
stats = zonal_stats(departments, str(RASTER), stats="sum", nodata=nodata)

pop = pd.DataFrame({
    "dept_code": departments["dept_code"],
    "dept_name": departments["dept_name"],
    "region_code": departments["region_code"],
    "pop_department": [s["sum"] or 0.0 for s in stats],
})
pop["pop_year"] = config["population"]["year"]

# Checks
assert len(pop) == 58, f"Expected 58 departments, got {len(pop)}"
assert (pop["pop_department"] > 0).all(), "A department has zero population"

dept_total = pop["pop_department"].sum()
gap = abs(dept_total - raster_total) / raster_total
print(f"Raster total:      {raster_total:,.0f}")
print(f"Sum of departments:{dept_total:,.0f}")
print(f"Difference:        {gap:.2%}")
assert gap < 0.01, "Departments do not add up to the raster total (gap above 1%)"

pop.to_parquet(INTERIM / "population_departments.parquet", index=False)
print(f"Saved population for {len(pop)} departments.")