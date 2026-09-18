# Data

DataCo and Brunel, the shared case every session teaches and labs
against. Fetched, not committed, see `.gitignore`.

## DataCo

The "DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS" dataset
(Constante, Silva and Pereira), a single wide table of supply chain
order transactions: orders, products, customers, shipping mode, and
delivery status, around 180,000 rows. Available on Kaggle under
multiple mirrors, for example
[`shashwatwork/dataco-smart-supply-chain-for-big-data-analysis`](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis).
Requires a (free) Kaggle account and API token to download
programmatically.

## Brunel

The "Supply Chain Logistics Problem Dataset," published by Brunel
University London on Figshare:
[brunel.figshare.com/articles/dataset/Supply_Chain_Logistics_Problem_Dataset/7558679](https://brunel.figshare.com/articles/dataset/Supply_Chain_Logistics_Problem_Dataset/7558679).
Seven related tables (order list, freight rates, warehouse costs and
capacities, products per plant, VMI customers, plant-port links),
which is what makes it a genuine multi-table integration and
referential-structure exercise rather than a single flat file.

## Fetching

Run `python data/fetch_data.py` from the repository root. It checks
for a Kaggle API token (`~/.kaggle/kaggle.json`) before attempting the
DataCo download and prints clear instructions if one is not configured;
the Brunel dataset downloads directly, no account needed.

## Licensing

Check each dataset's own licence on its source page before any use
beyond this course's own lab exercises, and cite both in any published
material, per the course's own "licence literacy" policy.
