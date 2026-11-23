"""Prepare Cameroon administrative boundaries (OCHA COD-AB, v01).

Reads the official region and department shapefiles, keeps the useful
columns, checks them, and saves clean GeoJSON files to data/interim/.
"""
from pathlib import Path
import yaml
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

RAW = ROOT / config["paths"]["raw"] / "boundaries"
INTERIM = ROOT / config["paths"]["interim"]
INTERIM.mkdir(parents=True, exist_ok=True)


def load_layer(filename, keep, rename):
    """Load one layer, convert it to EPSG:4326, keep and rename columns."""
    matches = list(RAW.rglob(filename))
    if not matches:
        raise FileNotFoundError(f"{filename} not found under {RAW}")

    gdf = gpd.read_file(matches[0])

    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(4326)

    gdf = gdf[keep + ["geometry"]].rename(columns=rename)
    gdf["geometry"] = gdf.geometry.make_valid()
    return gdf


regions = load_layer(
    "cmr_admin1.shp",
    keep=["adm1_pcode", "adm1_name1", "adm1_name"],
    rename={"adm1_pcode": "region_code",
            "adm1_name1": "region_name_fr",
            "adm1_name": "region_name_en"},
)

departments = load_layer(
    "cmr_admin2.shp",
    keep=["adm2_pcode", "adm2_name1", "adm1_pcode"],
    rename={"adm2_pcode": "dept_code",
            "adm2_name1": "dept_name",
            "adm1_pcode": "region_code"},
)

# Checks: stop with a clear message rather than save bad data
assert len(regions) == 10, f"Expected 10 regions, got {len(regions)}"
assert len(departments) == 58, f"Expected 58 departments, got {len(departments)}"
assert regions["region_code"].is_unique, "Duplicate region codes"
assert departments["dept_code"].is_unique, "Duplicate department codes"
assert departments["region_code"].isin(regions["region_code"]).all(), \
    "A department points to an unknown region"

metros = config["study"]["metro_dept_codes"]
found = departments["dept_code"].isin(metros).sum()
assert found == len(metros), f"Metropolis departments found: {found} of {len(metros)}"

regions.to_file(INTERIM / "regions.geojson", driver="GeoJSON")
departments.to_file(INTERIM / "departments.geojson", driver="GeoJSON")
print(f"Saved {len(regions)} regions and {len(departments)} departments.")