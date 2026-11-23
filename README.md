# Cameroon Broadband Quality Intelligence

**Where is the internet in Cameroon too poor to be truly useful, how is that
changing over time, and where would improving it help the most people?**

Coverage maps show where a signal exists, not whether the connection is good
enough for a video call, an online class or a mobile money transaction.
National averages mix Douala and Yaoundé with rural departments and hide large
local gaps. This project uses open speed-test data to measure **usable**
internet quality across Cameroon's 58 departments, quarter by quarter, for
fixed and mobile networks, and to identify where investment is most needed.

> **Status:** Phase 1 (data pipeline) in progress.

## Research questions

| ID | Question |
|----|----------|
| RQ1 | What share of the measured population has a usable connection, and how does it vary across departments? |
| RQ2 | Is the quality gap between the two metropolises (Douala, Yaoundé) and the rest of the country narrowing between 2024 and 2026? |
| RQ3 | How well do speed tests represent the population, and where are the unmeasured areas? |
| RQ4 | Which areas should be prioritised for investment, and is that ranking robust? |

## Project phases

1. **Data pipeline:** collect, clean and join open datasets into a reproducible, department-level dataset.
2. **Exploratory analysis:** quality gaps, trends, and data representativeness.
3. **Modelling:** area clustering, forecasting, and an investment prioritisation score with sensitivity analysis.
4. **Delivery:** interactive dashboard, blog post and scientific article.

## Data sources

| Dataset | Provider | License |
|---------|----------|---------|
| [Speedtest® by Ookla® Global Fixed and Mobile Network Performance Maps](https://registry.opendata.aws/speedtest-global-performance/) | Ookla | CC BY-NC-SA 4.0 |
| [Cameroon Subnational Administrative Boundaries (COD-AB)](https://data.humdata.org/dataset/cod-ab-cmr) | OCHA / INC | Public |
| [Constrained population, 100 m, R2025A](https://hub.worldpop.org/geodata/listing?id=100) | WorldPop | CC BY 4.0 |
| [GHS-SMOD R2023A, Degree of Urbanisation](https://human-settlement.emergency.copernicus.eu/ghs_smod2023.php) | European Commission, JRC | Free reuse with attribution |

Raw data is not stored in this repository. The pipeline downloads and rebuilds
everything from the original sources.

## Repository structure

```
├── data/            # raw, interim, processed (not in Git)
├── notebooks/       # exploration only
├── src/             # one script per pipeline step
├── reports/         # data quality report and figures
├── config.yaml      # all parameters: period, thresholds, paths
├── METHODS_LOG.md   # every methodological decision and its reason
└── FINDINGS.md      # observations recorded during the analysis
```

## How to run

```bash
git clone https://github.com/<your-username>/cameroon-broadband-intelligence.git
cd cameroon-broadband-intelligence
py -m venv .venv
.venv\Scripts\activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

<!-- Pipeline command to be added at the end of Phase 1 -->

## Methodology notes

- Averages are **weighted by number of tests**, never simple means.
- Speeds are translated into **usability tiers** (Good, Usable, Basic, Poor)
  based on what people can do online.
- Areas with too few tests are flagged as **low confidence**.
- Full reasoning for every choice is in [`METHODS_LOG.md`](METHODS_LOG.md).

## Limitations

- Speed tests are run voluntarily, so they over-represent connected, urban users.
- An area with no tests is not necessarily an area with no coverage.
- Ookla provides averages per tile, not medians or full distributions.

## Attribution

Speedtest® by Ookla® Global Fixed and Mobile Network Performance Maps. Based on
analysis by Ookla of Speedtest Intelligence® data for <period>. Provided by
Ookla and accessed <date>. Ookla trademarks used under license and reprinted
with permission.

## License

Code: <choose a license, e.g. MIT>. Data remains under each provider's license
listed above; derived Ookla data is shared under CC BY-NC-SA 4.0.

## Author

Sikapa Lucien – Telecommunications Engineer · www.sikapal.org