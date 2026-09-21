"""Session 6 lab, step 6 -- tabular baseline on the flattened join, for
the SAME late-delivery node classification task and the SAME random
70/15/15 order split (same seed) as train_node_classification.py, so
the graph-vs-tabular comparison in the README is honest and
apples-to-apples.

Library: XGBoost (`xgboost.XGBClassifier`). Gradient-boosted trees are
the standard, hard-to-beat baseline for tabular supply-chain/logistics
prediction in industry, need no feature scaling, and are explicitly
one of the two options this session's syllabus names.

The "flattened join" = one row per order, with the order's own fields
PLUS its supplier's/product's/carrier's/port's/plant's static features
denormalized onto that row -- exactly what SQL joining the order fact
table to its dimension tables would produce. Deliberately the same
information the GNN can reach in 1-2 hops, just without the
relational/message-passing structure.

Run:
    python3 tabular_baseline.py
"""
import argparse
import json
from pathlib import Path

import pandas as pd
from xgboost import XGBClassifier

from build_heterodata import load_or_build
from train_node_classification import SEED, make_splits, metrics

HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "data" / "tabular_baseline_results.json"


def flatten_join(dataset):
    suppliers, products, plants, ports, carriers = (
        dataset["suppliers"], dataset["products"], dataset["plants"],
        dataset["ports"], dataset["carriers"],
    )
    rows = []
    for o in dataset["orders"]:
        s_name, s_region = suppliers[o["supplier_idx"]]
        p_name, p_cat, p_fragile = products[o["product_idx"]]
        pl_name, pl_region = plants[o["plant_idx"]]
        port_name, port_region, port_base_congestion = ports[o["port_idx"]]
        c_name, c_sla, c_base_late_rate = carriers[o["carrier_idx"]]

        rows.append(dict(
            po_id=o["po_id"], order_value=o["order_value"], quantity=o["quantity"],
            sla_days=o["sla_days"], supplier_name=s_name, supplier_region=s_region,
            product_category=p_cat, product_fragile=int(p_fragile), plant_region=pl_region,
            port_name=port_name, port_region=port_region, port_base_congestion=port_base_congestion,
            carrier_name=c_name, carrier_sla_days=c_sla, carrier_base_late_rate=c_base_late_rate,
            late=o["late"],
        ))
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=SEED,
                         help="Must match train_node_classification.py's --seed for an honest comparison.")
    parser.add_argument("--n-estimators", type=int, default=200)
    parser.add_argument("--max-depth", type=int, default=3)
    args = parser.parse_args()

    dataset, _ = load_or_build()
    df = flatten_join(dataset)
    print(f"Flattened join table: {df.shape[0]} rows x {df.shape[1]} columns")
    print(df.head(3).to_string())

    y = df["late"].values
    X = df.drop(columns=["po_id", "late"])
    cat_cols = X.select_dtypes(include=["object", "str"]).columns.tolist()
    X_enc = pd.get_dummies(X, columns=cat_cols)
    print(f"\nAfter one-hot encoding categoricals {cat_cols}: {X_enc.shape[1]} feature columns")

    n = len(df)
    # SAME split protocol (same seed, same ratios) as
    # train_node_classification.py's make_splits(), so the order at
    # position i here is the order at position i in build_graph()'s
    # 'order' node ordering too (build_dataset() is deterministic).
    train_mask, val_mask, test_mask = make_splits(n, seed=args.seed)
    train_mask, val_mask, test_mask = train_mask.numpy(), val_mask.numpy(), test_mask.numpy()

    X_train, y_train = X_enc[train_mask], y[train_mask]
    X_val, y_val = X_enc[val_mask], y[val_mask]
    X_test, y_test = X_enc[test_mask], y[test_mask]
    print(f"\ntrain={X_train.shape[0]}  val={X_val.shape[0]}  test={X_test.shape[0]}")

    clf = XGBClassifier(
        n_estimators=args.n_estimators, max_depth=args.max_depth, learning_rate=0.05,
        subsample=0.9, colsample_bytree=0.9, eval_metric="logloss", random_state=args.seed,
    )
    clf.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

    train_m = metrics(y_train, clf.predict(X_train))
    val_m = metrics(y_val, clf.predict(X_val))
    test_m = metrics(y_test, clf.predict(X_test))

    print(f"\n[XGBoost baseline] train: {train_m}")
    print(f"[XGBoost baseline] val:   {val_m}")
    print(f"[XGBoost baseline] test:  {test_m}")

    importances = sorted(zip(X_enc.columns, clf.feature_importances_), key=lambda kv: -kv[1])[:10]
    print("\nTop 10 feature importances:")
    for name, imp in importances:
        print(f"  {name:<28} {imp:.4f}")

    results = dict(
        n_features=X_enc.shape[1], train=train_m, val=val_m, test=test_m,
        top_features=[dict(name=n_, importance=float(i_)) for n_, i_ in importances],
    )
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH.relative_to(HERE)}")


if __name__ == "__main__":
    main()
