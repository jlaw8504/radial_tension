from pathlib import Path

import pandas as pd
import seaborn as sns
from numpy import ndarray
from scipy.io import loadmat

FIGURE_3_DATA = Path(__file__).parent / "intensity_metrics.mat"
sns.set(
    font_scale=2,
    rc={"text.usetex": True, "figure.figsize": (6.5, 5), "savefig.dpi": 600},
    style="whitegrid",
)
conditions: list[str] = ["untreated", "ben20", "ben100"]
pretty_conditions: list[str] = ["Untreated", r"$68 \ \mu M$", r"$313 \ \mu M$"]
fig_2_metrics: list[str] = ["sLengthsnm", "kHnm", "sHnm"]
ylabels: dict = {
    "c1_sum_bgsub_array": "Total Signal\nIntegrated Intensity (AU)",
    "c1_mean_bgsub_array": "Total Signal\nMean Intensity (AU)",
    "c1_int_vol_array": "Total Signal\n Mean Intensity/" + r"$\mu$$m^3$",
    "c1_ints_bg_sub": "Kinetochore Spot\nMaximum Intensity(AU)",
}
data: dict = loadmat(FIGURE_3_DATA)
S: ndarray = data["S"]
# these metrics are present for all conditions
metrics = S[0][0][conditions[0]][0][0].dtype.names
parsed_data: list[dict] = []
for metric in ylabels.keys():
    for condition in conditions:
        for value in S[0][0][condition][0][0][metric].flat:
            parsed_data.append(
                {"metric": metric, "condition": condition, "value": value}
            )
df = pd.DataFrame(parsed_data)
for fig_metric, pretty_ylabel in ylabels.items():
    ax = sns.violinplot(
        x="condition", y="value", data=df.loc[df["metric"] == fig_metric]
    )
    ax.set_ylabel(pretty_ylabel)
    ax.set_xticklabels(pretty_conditions)
    ax.set_xlabel(None)
    fig = ax.get_figure()
    fig.subplots_adjust(left=0.3)
    fig.savefig(f"./{fig_metric}.tif")

    ax.clear()
