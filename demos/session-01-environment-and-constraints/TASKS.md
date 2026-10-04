# Your tasks in this lab

Running the scripts is only the setup. The lab itself is the **hunt for
rules**: you look at the data, form a guess, check it with a count, and write
it down. You finish with **at least five rules**, each with evidence and a
source, in `constraint_inventory_template.csv`.

Work in this order. Times are a guide for the 60 minute lab.

| By minute | You should have |
|---|---|
| 15 | Part A done: smoke test passes, data fetched, profiles written |
| 35 | Parts B and C done: DataCo profile read, Order City clustered |
| 60 | Part D done: five rules or more, each with evidence, committed |

## Part A. Setup (about 15 minutes)

1. Run `python smoke_test.py`. **You are done when** every line says OK.
   If one fails, fix it now; later labs need all four tools.
2. Run `python data/fetch_data.py` from `DEMO_ROOT`. **You are done when**
   `data/dataco/` and `data/brunel/` hold CSV files.
3. Run `python profiling.py`. The DataCo profile takes several minutes and
   looks as if it hung. It has not. Start on Part B while it runs.

## Part B. Read the profile (about 20 minutes)

Open `profiling_report_dataco.html` and the Brunel reports. For each question,
**write the answer in a notes file** (a plain text file is fine). These notes
become evidence.

1. How many rows and columns does DataCo have? What does **one row** mean?
   (Hint: look at `Order Id` and `Order Item Id`. Is `Order Id` unique?)
2. Which columns are **empty or constant**? A column that never changes holds
   no information, and one that is always null may be a column nobody uses.
   Name each one you find.
3. Which columns have **missing values**? Roughly how many? Is the gap a
   problem, or just a column that only applies sometimes?
4. Pick the three columns you find least clear and write, in one sentence
   each, **what you think they mean**. Guess first. We check the guesses in
   Session 3.
5. Open the Brunel `OrderList` profile. Which columns look like codes
   (plant, port, carrier, service level)? How many distinct values has each?

## Part C. Cluster Order City in OpenRefine (about 15 minutes)

1. Start OpenRefine and create a project from `DataCoSupplyChainDataset.csv`.
2. On the **Order City** column choose *Edit cells, Cluster and edit*.
   Try the methods *Key collision, fingerprint* and *Nearest neighbour*.
3. **Check every cluster before you merge it.** For each one, look at the
   **Order Country** beside it. Two spellings of one city should be in one
   country. Two cities that share a name in different countries are **not** a
   duplicate; merging them would damage the data.
4. Write down, for each cluster: the values, the counts, the country, and
   your decision (merge or keep apart) with one sentence of reason.

This is a rule in disguise: "a city name is only unique together with its
country". Writing it down properly is one of your five rules.

## Part D. Find and test rules (about 25 minutes)

A rule is a statement the data always obeys, such as "a shipment is never
delivered before it is dispatched". Your job is to find rules the schema does
**not** already state, and to count how often each one holds.

Open `profiling.py` in JupyterLab or VS Code and add cells at the bottom, or
open a new notebook. Test each idea with `pandas`, for example:

```python
import pandas as pd
orders = pd.read_csv("../data/brunel/OrderList.csv")
links = pd.read_csv("../data/brunel/PlantPorts.csv")

# Does every order leave through a port its plant is linked to?
pairs = set(zip(links["Plant Code"], links["Port"]))
bad = orders[[ (p, o) not in pairs
               for p, o in zip(orders["Plant Code"], orders["Origin Port"]) ]]
print(len(bad), "of", len(orders), "orders break the rule")
```

Try at least five of the ideas below. Each one is a question, not an answer;
the data decides.

| # | Question to test | Where to look |
|---|---|---|
| 1 | Does every Brunel order leave through a port its plant is linked to? | `OrderList` against `PlantPorts` |
| 2 | Does every order ask a plant for a product that plant makes? | `OrderList` against `ProductsPerPlant` |
| 3 | Is any DataCo order shipped before it was ordered? | DataCo order date and shipping columns |
| 4 | Does DataCo's `Delivery Status` always agree with real days against scheduled days? Which status breaks it? | DataCo `Delivery Status`, `Days for shipping (real)`, `Days for shipment (scheduled)` |
| 5 | Does every order's carrier, origin, destination and service level have a rate in `FreightRates`? How many have none? | `OrderList` against `FreightRates` |
| 6 | Does every order weight fall inside a rate band? Is there a gap between two bands? | `OrderList.Weight` against `FreightRates` min and max weight |
| 7 | Which carrier uses which service level, and is it ever mixed? | `OrderList` Carrier and Service Level |
| 8 | Which columns are text that looks like a number, or hold stray spaces or mixed spellings? | `FreightRates.mode_dsc`, `WhCapacities` headers, `Order ID` |
| 9 | Do two columns that should agree (Customer Country and Order Country, for example) ever differ? | DataCo country columns |
| 10 | Your own idea. Look for a link the data always follows that no column says. | Anywhere |

## How to write one rule in the inventory

Open `constraint_inventory_template.csv`. Each row has three parts, and a row
with fewer than three is **not a finding**:

| Column | What goes in it | Example |
|---|---|---|
| `rule` | One sentence you could turn into a check later | "An order leaves only through a port linked to its plant" |
| `evidence_in_data` | The **count** you measured, and any exceptions | "0 of 9,215 orders break it" |
| `source_column_or_table` | Where the evidence came from | "Brunel OrderList.Plant Code, Origin Port; PlantPorts" |

Two habits earn the marks:

- **Write the exceptions down.** A rule that holds in 99.9 percent of rows is
  still a rule, but the 0.1 percent is a finding. Do not delete it.
- **Skip the trivial.** "Order Id is unique" is already stated by the schema.
  A good rule is one the schema does *not* state.

Be honest about the difference between three things (see `OVERVIEW.md`): a
**source fact** (a value in the file), a **profiling result** (a count from a
tool), and a **modelling decision** (a rule you propose). Your inventory
holds the third, backed by the first two.

## Finish

Save the inventory, run `git add` and `git commit` in your team repository,
and make sure you can answer in one sentence: *which rule surprised you
most, and why would a table schema never have told you?*

Reference numbers are in `reference-outputs/`. Check yours **after** you
have your own, not before; the aim is to find the rules, not to copy them.
