"""Entity resolution across two sources describing the same real
suppliers, differently: DataCo's own supplier list and Brunel's, never
sharing a key, sometimes not even sharing a spelling of the name.

Reports precision and recall against a small hand-labeled sample
(labels.csv), not a single accuracy figure, per this session's
deliverable: accuracy alone hides which kind of error a threshold
trades away.

Run:
    python3 -m venv .venv-er && source .venv-er/bin/activate
    pip install splink pandas
    python3 run_splink.py
"""

from pathlib import Path

import pandas as pd
import splink.comparison_library as cl
from splink import DuckDBAPI, Linker, SettingsCreator, block_on

HERE = Path(__file__).resolve().parent


def load():
    dataco = pd.read_csv(HERE / "dataco_suppliers.csv")
    brunel = pd.read_csv(HERE / "brunel_suppliers.csv")
    labels = pd.read_csv(HERE / "labels.csv")
    dataco["unique_id"] = dataco["supplier_id"]
    brunel["unique_id"] = brunel["supplier_id"]
    dataco["source_dataset"] = "dataco"
    brunel["source_dataset"] = "brunel"
    return dataco, brunel, labels


def build_linker(dataco, brunel):
    settings = SettingsCreator(
        link_type="link_only",
        comparisons=[
            # Names rarely match exactly across two independently kept
            # supplier lists ("Cedars Cargo" vs "Cedars Cargo Services"),
            # so a fuzzy string comparison carries this rule, not
            # cl.ExactMatch.
            cl.JaroWinklerAtThresholds("name", [0.9, 0.7]),
            cl.ExactMatch("city"),
            cl.ExactMatch("country"),
        ],
        blocking_rules_to_generate_predictions=[block_on("country")],
    )
    return Linker(
        [dataco, brunel],
        settings,
        db_api=DuckDBAPI(),
        input_table_aliases=["dataco", "brunel"],
    )


def train(linker):
    # Blocking on name here would fail: near-duplicate names rarely
    # match byte-for-byte, so the random-match-probability estimate
    # collapses to zero and every downstream score follows it to zero.
    # City plus country gives it real matches to anchor on.
    linker.training.estimate_probability_two_random_records_match(
        [block_on("city", "country")], recall=0.9
    )
    linker.training.estimate_u_using_random_sampling(max_pairs=1e6)
    linker.training.estimate_parameters_using_expectation_maximisation(
        block_on("country")
    )


def score(linker, labels, threshold):
    preds = linker.inference.predict(threshold_match_probability=threshold)
    df = preds.as_pandas_dataframe()
    df = df[df["source_dataset_l"] != df["source_dataset_r"]]

    pred_pairs = set()
    for _, row in df.iterrows():
        if row["source_dataset_l"] == "dataco":
            pred_pairs.add((row["unique_id_l"], row["unique_id_r"]))
        else:
            pred_pairs.add((row["unique_id_r"], row["unique_id_l"]))

    true_pairs = {
        (r.dataco_id, r.brunel_id) for r in labels.itertuples() if r.is_match == 1
    }

    tp = len(pred_pairs & true_pairs)
    fp = len(pred_pairs - true_pairs)
    fn = len(true_pairs - pred_pairs)
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")

    print(f"\n=== threshold {threshold} ===")
    print(f"True positives:  {tp}")
    print(f"False positives: {fp}  {sorted(pred_pairs - true_pairs)}")
    print(f"False negatives: {fn}  {sorted(true_pairs - pred_pairs)}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    return precision, recall


if __name__ == "__main__":
    dataco, brunel, labels = load()
    linker = build_linker(dataco, brunel)
    train(linker)
    # Run both, live, in the room: 0.5 (Splink's own default) shows the
    # false-positive cost, 0.8 shows the fix. Change this to try your
    # own team's threshold once you have your own labeled sample.
    score(linker, labels, threshold=0.5)
    score(linker, labels, threshold=0.8)
