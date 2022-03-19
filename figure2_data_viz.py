from pathlib import Path

import pandas as pd
import seaborn as sns
from scipy.io import loadmat

FIGURE_2_DATA = Path(__file__).parent / "ame1_ben_data.mat"
sns.set(
    font_scale=2,
    rc={"text.usetex": True, "figure.figsize": (6.5, 5), "savefig.dpi": 600},
    style="whitegrid",
)
conditions: list[str] = ["untreated", "ben20", "ben100"]
pretty_conditions: list[str] = ["Untreated", r"$68 \ \mu M$", r"$313 \ \mu M$"]
fig_2_metrics: list[str] = ["sLengthsnm", "kHnm", "sHnm"]
ylabels: dict = {
    "sLengthsnm": "Spindle Length (nm)",
    "kHnm": "Ame1 signal width (nm)\n transverse to spindle axis",
    "sHnm": "Spc42 signal width (nm)\n transverse to spindle axis",
}
plot_data: list[dict] = []
struct_dict = loadmat(FIGURE_2_DATA)
ame1 = struct_dict["ame1"]
for treatment in conditions:
    for metric in ame1[treatment][0][0].dtype.names:
        if metric in fig_2_metrics:
            for value_list in ame1[treatment][0][0][metric][0][0]:
                for value in value_list:
                    data: dict = {
                        "condition": treatment,
                        "metric": metric,
                        "value": value,
                    }
                    plot_data.append(data)

df = pd.DataFrame(plot_data)
for fig_metric in fig_2_metrics:
    ax = sns.violinplot(
        x="condition", y="value", data=df.loc[df["metric"] == fig_metric]
    )
    ax.set_ylabel(ylabels[fig_metric])
    ax.set_xticklabels(pretty_conditions)
    ax.set_xlabel(None)
    fig = ax.get_figure()
    fig.subplots_adjust(left=0.2)
    fig.savefig(f"./{fig_metric}.tif")

    ax.clear()
