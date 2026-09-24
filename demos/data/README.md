# Data

DataCo and Brunel, the shared case every session teaches and labs
against. Fetched, not committed (see `demos/.gitignore`).

## Fetching

From the `demos/` folder: `python data/fetch_data.py`. No account or
token needed. Every file is checked against the checksum its publisher
lists. Needs `openpyxl` for the Brunel CSV export (`pip install openpyxl`).
Verified working on 2026-09-22.

## DataCo (`data/dataco/`)

"DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS" (Constante, Silva and
Pereira), Mendeley Data, DOI 10.17632/8gx2fvg2k6.5, CC BY 4.0.

- `DataCoSupplyChainDataset.csv`: one wide table, **180,519 order lines,
  53 columns** (order, customer, product, shipping mode, scheduled and
  real shipping days, delivery status, late delivery risk). Latin-1
  encoded. Customer name, email and password columns exist in the file;
  never show them on a slide.
- `DescriptionDataCoSupplyChain.csv`: the publisher's own data
  dictionary, one line per column.

## Brunel (`data/brunel/`)

"Supply Chain Logistics Problem Dataset", Brunel University London,
Figshare article 7558679 version 2, CC BY 4.0. One workbook,
`Supply chain logistics problem.xlsx`, exported to one CSV per sheet:

| File | Rows | What one row is |
|---|---|---|
| `OrderList.csv` | 9,215 | an order: origin port, carrier, plant, destination port, weight |
| `FreightRates.csv` | 1,540 | a carrier's price for a lane and weight band |
| `WhCosts.csv` | 20 | a warehouse's cost per unit |
| `WhCapacities.csv` | 19 | a plant's daily capacity |
| `ProductsPerPlant.csv` | 2,036 | a product a plant can make |
| `VmiCustomers.csv` | 14 | a customer a plant serves under vendor managed inventory |
| `PlantPorts.csv` | 22 | a port a plant is allowed to ship through |

The seven tables are what make Brunel a real multi table integration
exercise, unlike DataCo's single flat file.

## Licensing

Both are CC BY 4.0: reuse is allowed with attribution. Cite both in any
published material, per the course's licence literacy policy.
