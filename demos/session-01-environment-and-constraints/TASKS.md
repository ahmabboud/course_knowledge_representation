# Your steps in this lab

This lab is not a test. It shows you, on real data, what a hidden rule looks
like and how we write one down. Every step has a command to run, something to
look at, and what you should see. If your numbers match, you understood it.

About 60 minutes. Nothing here needs you to write code.

## Step 1. Check your setup (about 5 minutes)

```text
python smoke_test.py
```

**You should see** OK for Python, Java, Docker and Protégé. If one fails, say
so now; later labs need all four.

## Step 2. Get the data (about 5 minutes)

From `DEMO_ROOT`:

```text
python data/fetch_data.py
```

**You should see** CSV files in `data/dataco/` and `data/brunel/`.

## Step 3. Build the profiles (about 5 minutes, then keep reading)

```text
python profiling.py
```

The DataCo profile takes several minutes and looks as if it hung. It has not.
Start Step 5 while it runs.

## Step 4. Read the profiles (about 10 minutes)

Open the HTML reports. Look at three things and say each aloud to a neighbour:

1. **One row means one order line.** DataCo has 180,519 rows but only 65,752
   orders, because one order has several lines.
2. **Some columns are empty or constant.** Look for `Product Description`
   (always empty) and `Customer Password` (the same value everywhere). A column
   that never changes holds no information.
3. **Some values are missing.** `Order Zipcode` is missing in most rows.

**What this shows:** a profile counts what is in the data. It does not tell
you what the data means. A person has to read it.

## Step 5. Run the rule checks (about 10 minutes)

```text
python rule_checks.py
```

It prints six checks. For each one, read the **Result** and the **Meaning**
and check they make sense to you:

| Check | What it asks | What you should see |
|---|---|---|
| 1 | Does every order leave through a port linked to its plant? | 0 of 9,215 break it |
| 2 | Does every order ask a plant for a product it makes? | 0 of 9,215 break it |
| 3 | Which carrier uses which service level? | Each carrier uses one level, except V444_0 |
| 4 | Do all orders have a freight rate? | 854 do not |
| 5 | Does Delivery Status match the days? | Yes for three statuses, not for "Shipping canceled" |
| 6 | Are near-identical city names the same city? | No: different countries |

**What this shows:** some rules always hold (1 and 2), and the schema never
stated them. Some rules hold with exceptions (4 and 5), and the exceptions are
the interesting part.

## Step 6. Cluster Order City in OpenRefine (about 15 minutes)

1. Start OpenRefine and create a project from `DataCoSupplyChainDataset.csv`.
2. On the **Order City** column choose *Edit cells*, then *Cluster and edit*.
   Use *Key collision* with the *fingerprint* method.
3. You should see **three clusters**: Los Angeles / Los Ángeles,
   Vitoria / Vitória, and Macon / Mâcon.
4. For each one, look at **Order Country** beside the values. Do not merge
   until you have looked.

**What this shows:** two spellings that look the same can be two different
places (Los Angeles in the United States, Los Ángeles in Chile). A tool finds
the candidates; a person decides. This is why Check 6 matters.

## Step 7. Record what you found (about 10 minutes)

Open `constraint_inventory_template.csv`. It already holds the rules from the
six checks, with the numbers you just saw. Do two things:

1. Read each row and check its numbers against your own output.
2. Add **one rule of your own** if you can: something you noticed in the
   profile or in OpenRefine. If nothing comes to mind, that is fine.

Each rule has three parts: the rule itself, the count that supports it, and
where it came from. A rule with no count is only a guess.

## Finish

Save the file and commit it to your team repository. Then answer for
yourself: *which result surprised you, and would a table schema ever have
told you?*
