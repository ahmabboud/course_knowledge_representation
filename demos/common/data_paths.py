"""Central place naming where DataCo and Brunel live once
data/fetch_data.py has run. Import this instead of hardcoding a path
in every session's notebook.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

DATACO_CSV = DATA_DIR / "dataco" / "DataCoSupplyChainDataset.csv"

# The seven Brunel tables, per the Brunel University London "Supply
# Chain Logistics Problem Dataset" (see data/README.md for the source).
BRUNEL_DIR = DATA_DIR / "brunel"
BRUNEL_TABLES = {
    "order_list": BRUNEL_DIR / "OrderList.csv",
    "freight_rates": BRUNEL_DIR / "FreightRates.csv",
    "wh_costs": BRUNEL_DIR / "WhCosts.csv",
    "wh_capacities": BRUNEL_DIR / "WhCapacities.csv",
    "products_per_plant": BRUNEL_DIR / "ProductsPerPlant.csv",
    "vmi_customers": BRUNEL_DIR / "VmiCustomers.csv",
    "plant_ports": BRUNEL_DIR / "PlantPorts.csv",
}
