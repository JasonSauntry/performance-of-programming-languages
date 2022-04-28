#!/usr/bin/env python3
import os.path

import matplotlib as mpl
import numpy as np
import pandas as pd
from cycler import cycler
from matplotlib import pyplot as plt

pretty_names = {
    "matmul_naïve": "Matrix Multiplication (Naïve)",
    "matmul_optimized": "Matrix Multiplication (Optimized)",
    "sort_stdlib": "Sorting (Standard Library)",
    "heap": "Heap-implemented Priority Queue",
}


def plot_runtime(data, op_ax):
    def post(ax):
        ax.set_ylabel("Runtime (ms)")
        ax.set_title("Runtime by input size")
        # ax.set_xscale("log", base=2)
        # ax.set_yscale("log", base=2)

    plot_field(data, op_ax, "time", post)


def plot_memory(data, op_ax):
    def post(ax):
        ax.set_ylabel("Memory (KiB)")
        ax.set_title("Peak memory usage by input size")
        # ax.set_xscale("log", base=2)
        # ax.set_yscale("log", base=2)

    plot_field(data, op_ax, "memory", post)


def plot_memory_base(data, op_ax):
    def post(ax):
        ax.set_ylabel("Memory (KiB)")
        ax.set_title("Marginal Peak memory usage by input size")
        # ax.set_xscale("log", base=2)
        # ax.set_yscale("log", base=2)

    def find_min(data, op, lang):
        min_mem = data[(data["operation"] == op) & (data["language"] == lang)][
            "memory"
        ].min()
        return min_mem

    def find_adj(row):
        op = row["operation"]
        lang = row["language"]
        min_mem = find_min(data, op, lang)
        return row["memory"] - min_mem

    data["mem_adj"] = data.apply(find_adj, axis=1)
    plot_field(data, op_ax, "mem_adj", post)


def plot_field(data, op_ax, field, post_hook=lambda ax: None):
    for operation, ax in op_ax:
        for lang in data["language"].unique():
            d = (
                data[
                    (data["operation"] == operation)
                    & (data["language"] == lang)
                    & (data[field].isnull() == False)
                ]
                .groupby("input_size")
                .mean()
            )

            ax.plot(
                d.index,
                d[field],
                "x-",
                label=f"{pretty_names[operation]}, {lang}",
            )
        ax.legend()
        ax.set_xlabel("n")
        post_hook(ax)


path = os.path.join(os.path.dirname(__file__), "./results-4.tsv")

data = pd.read_csv(path, sep="\t")

# KiB
data["memory"] = data["memory"] / 1024

# fig, axs = plt.subplots(4, 2)


def show_op(op, show=True):
    fig, axs = plt.subplots(
        1,
        3,
        figsize=(14, 8),
    )
    fig.title = pretty_names[op]

    plot_runtime(data, [(op, axs[0])])
    plot_memory(data, [(op, axs[1])])
    plot_memory_base(data, [(op, axs[2])])

    if show:
        plt.show()

    return fig


show_mat = lambda: show_op("matmul_naïve")
show_opt = lambda: show_op("matmul_optimized")
show_srt = lambda: show_op("sort_stdlib")
show_hep = lambda: show_op("heap")

if __name__ == "__main__":
    for op in data["operation"].unique():
        show_op(op, False).savefig(f"{op}-plot.png")

    plt.show()
