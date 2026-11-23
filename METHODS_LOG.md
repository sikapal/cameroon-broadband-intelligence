# Methods Log

## 2026-11-23 – Study period starts in 2024 Q1
- **Decision:** Analyse Ookla data from 2024 Q1 to the latest published quarter.
- **Reason:** Gives more than two years of quarterly data, enough to see a trend.
  The latency-under-load columns exist since 2022 Q4, so they are available
  for the whole period.
- **Alternative rejected:** Starting in 2019 (first Ookla release). More history,
  but older quarters lack latency under load, and 2020–2021 are distorted by COVID.

## 2026-11-23 – Metropolises defined as Wouri and Mfoundi
- **Decision:** The "metropolis" group for RQ2 is the Wouri (Douala) and
  Mfoundi (Yaoundé) departments.
- **Reason:** They contain Cameroon's two largest cities. Fixed before looking
  at any results, so the definition cannot be tuned to fit the findings.
- **Alternative rejected:** Using GHSL "urban centres". More objective, but would
  include smaller cities and blur the comparison with the two capitals.

  ## 2026-11-23 – Department as the main unit of analysis
- **Decision:** Results are computed and reported mainly at department level
  (58 departments), with regions (10) and the national level as summaries.
- **Reason:** Regions are too coarse: a single region mixes a large city with
  remote rural areas and hides the gaps we want to measure. Departments are
  fine enough to show local differences while most still have enough speed
  tests to give reliable averages. Departments are also an administrative
  level used by the State, so results map onto real decision-making units.
- **Alternative rejected:** Arrondissements (about 360). Finer, but many would
  have too few tests per quarter to be reliable, so a large part of the map
  would be flagged as low confidence.

## 2026-11-23 – Test-weighted averages instead of simple means
- **Decision:** When combining tiles into a department, region or country,
  each tile's average is weighted by its number of tests.
- **Reason:** Ookla provides one average per tile, but tiles have very
  different numbers of tests. A simple mean would give a tile with 2 tests
  the same weight as a tile with 2,000 tests, letting a few unrepresentative
  measurements distort the result. Weighting by tests reproduces the average
  over all individual tests, which is what the area really experienced.
- **Alternative rejected:** Simple mean of tile averages (statistically biased),
  and median of tile averages (more robust to outliers, but still ignores how
  many tests each tile represents).

## 2026-11-23 – Minimum number of tests
- **Decision:** A department-quarter with fewer than 30 tests is flagged
  "low confidence" and not used for conclusions. A tile with fewer than 5
  tests is kept in totals but never shown on its own on a map.
- **Reason:** An average based on very few tests can be driven by one or two
  unusual measurements. 30 is a common rule of thumb for a reasonably stable
  average. At tile level, 5 tests filters out the noisiest tiles while keeping
  most of the data.
- **Alternative rejected:** No threshold (fragile results in sparse areas), or
  a higher threshold such as 50 (more reliable but excludes more rural areas,
  which are exactly the ones this study cares about). The effect of choosing
  30 versus 50 will be tested in the sensitivity analysis.

## 2026-11-23 – Usability tiers and thresholds
- **Decision:** Each tile is classified into one of four tiers, checked from
  the top down, a tile needing to meet all conditions of a tier:
  Good (≥ 10 Mbps down, ≥ 3 Mbps up, < 50 ms), Usable (≥ 3 Mbps down,
  ≥ 1 Mbps up, < 100 ms), Basic (≥ 1 Mbps down), Poor (below that).
- **Reason:** Raw speeds mean little to citizens or decision-makers. Tiers
  translate them into what people can actually do online: stream, make video
  calls, use mobile money. Upload and latency are included because video
  calls and online classes depend on them, not only on download speed.
  Sources to be added: published bandwidth requirements of common
  applications (e.g. Zoom, Google Meet, YouTube).
- **Alternative rejected:** Using a single national broadband definition such
  as the US FCC 100/20 Mbps. Designed for a different market, it would
  classify almost all of Cameroon as unserved and hide meaningful differences
  between areas.

  ## 2026-11-23 – Administrative boundaries source
- **Decision:** Use OCHA COD-AB for Cameroon (version v01, valid from 2019-01-04),
  standard layers cmr_admin1 (regions) and cmr_admin2 (departments).
- **Reason:** Official boundary set used by the UN, with stable P-codes for every
  region and department. Joining on codes avoids errors from spelling and accents.
  Standard layers used, not the edge-matched (_em) ones, which are meant for
  cartography. Downloaded from HDX on <date>.
- **Alternative rejected:** GADM 4.1. Widely used, but joins would rely on names,
  and its license restricts commercial reuse.

## 2026-11-23 – Metropolises identified by code
- **Decision:** Metropolis departments are referenced by P-code in config.yaml:
  CM005004 (Wouri, Douala) and CM002007 (Mfoundi, Yaoundé).
- **Reason:** Codes are stable and independent of spelling or accents, unlike names.

## 2026-11-23 – Population source and year
- **Decision:** Use WorldPop constrained 100 m population, release R2025A,
  year 2025 (cmr_pop_2025_CN_100m_R2025A_v1.tif). Population summed per
  department with zonal statistics (cells counted where their centre falls).
- **Reason:** Constrained estimates place people only where buildings exist,
  which suits a country with large forested and sparsely settled areas.
  2025 is the middle of the study period. Raster total: <your number>;
  UN 2025 estimate: 29,879,337. Downloaded on <date>.
- **Alternative rejected:** Unconstrained WorldPop (spreads people into
  uninhabited areas), and a separate population year per quarter (adds
  complexity for little gain over a 2–3 year period).