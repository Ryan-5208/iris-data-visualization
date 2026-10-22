#!/usr/bin/env python3
"""Create before, improved, and comparison figures from the Iris dataset.

Usage (from project root): python src/visualize_iris.py
Dataset: scikit-learn's corrected Fisher Iris data, shipped as data/iris_fisher.csv.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'figures'
OUTPUT.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(ROOT / 'data' / 'iris_fisher.csv')

COLORS = {'Setosa': '#2366B5', 'Versicolor': '#008B75', 'Virginica': '#BA4B6E'}
MARKERS = {'Setosa': 'o', 'Versicolor': 's', 'Virginica': '^'}


def before(ax):
    """Baseline: a correct but minimally informative scatterplot."""
    ax.scatter(df['petal_length_cm'], df['petal_width_cm'], s=28,
               color='#6682A0', alpha=.7)
    ax.set_xlabel('Petal length (cm)', fontsize=11)
    ax.set_ylabel('Petal width (cm)', fontsize=11)
    ax.set_xlim(.65, 7.2)
    ax.set_ylim(-.08, 2.85)
    ax.set_title('Before  |  All flowers together', loc='left', fontsize=15, weight='semibold', pad=16)
    ax.grid(False)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=10)


def after(ax, detailed=True):
    """Improvement: encode species by shape and color, with useful labels."""
    ax.set_facecolor('#FAFBFD')
    for species in ['Setosa', 'Versicolor', 'Virginica']:
        subset = df[df.species == species]
        ax.scatter(subset['petal_length_cm'], subset['petal_width_cm'],
                   c=COLORS[species], marker=MARKERS[species],
                   s=48, alpha=.82, edgecolors='white', linewidths=.65,
                   label=f'{species} (n={len(subset)})', zorder=3)
    ax.set_xlabel('Petal length (cm)', fontsize=11, labelpad=8)
    ax.set_ylabel('Petal width (cm)', fontsize=11, labelpad=8)
    ax.set_xlim(.65, 7.2)
    ax.set_ylim(-.08, 2.85)
    ax.grid(color='#DFE5EF', alpha=.75, linewidth=.65, zorder=0)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#AAB6C4')
    ax.tick_params(labelsize=10, color='#AAB6C4')
    ax.set_title('After  |  Species revealed', loc='left', fontsize=15, weight='semibold', pad=16)
    ax.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='white',
              edgecolor='#E0E5EE', markerscale=1.08)
    if detailed:
        ax.annotate('Setosa is distinctly separated', xy=(1.7, .3),
                    xytext=(1.22, 1.07), color='#154D88', fontsize=10, weight='medium',
                    arrowprops=dict(arrowstyle='->', color='#154D88', lw=1.2,
                                    connectionstyle='arc3,rad=-.16'), zorder=4)
        ax.annotate('Some overlap between these species', xy=(4.95, 1.65),
                    xytext=(2.85, 2.48), color='#596574', fontsize=10,
                    arrowprops=dict(arrowstyle='->', color='#596574', lw=1.2,
                                    connectionstyle='arc3,rad=.22'), zorder=4)


# Standalone "before" image
fig, ax = plt.subplots(figsize=(8.1, 5.35), dpi=160)
fig.patch.set_facecolor('white')
before(ax)
fig.subplots_adjust(left=.12, right=.96, bottom=.15, top=.87)
fig.savefig(OUTPUT / 'before.png', dpi=180, facecolor='white')
plt.close(fig)

# Standalone "after" image
fig, ax = plt.subplots(figsize=(9.2, 5.7), dpi=160)
fig.patch.set_facecolor('white')
after(ax)
fig.suptitle('Petal measurements distinguish iris species', fontsize=20,
             weight='bold', x=.1, ha='left', y=.985, color='#16253A')
fig.text(.10, .925, '150 flowers  •  3 species  •  Each point is one flower',
         fontsize=10.5, color='#596777')
fig.text(.10, .025, 'Data: Fisher Iris (corrected version via scikit-learn). Measurements in centimeters.',
         fontsize=9, color='#6D7887')
fig.subplots_adjust(left=.10, right=.96, bottom=.16, top=.81)
fig.savefig(OUTPUT / 'after.png', dpi=180, facecolor='white')
plt.close(fig)

# Side-by-side picture for direct submission to the class assignment.
fig, axs = plt.subplots(1, 2, figsize=(15.2, 6.0), dpi=160)
fig.patch.set_facecolor('white')
before(axs[0])
after(axs[1], detailed=False)
fig.suptitle('From an unlabeled scatterplot to a meaningful comparison',
             x=.055, y=.985, ha='left', fontsize=19, weight='bold', color='#16253A')
fig.text(.055, .915,
         'The improved chart identifies each species by both color and shape, making the natural groups visible.',
         color='#556273', fontsize=11)
fig.text(.055, .038,
         'Dataset: Fisher Iris (corrected version distributed with scikit-learn)  |  150 flowers, 50 of each species.',
         fontsize=9.2, color='#667485')
fig.subplots_adjust(left=.07, right=.98, wspace=.25, top=.81, bottom=.16)
fig.savefig(OUTPUT / 'before_after_comparison.png', dpi=180, facecolor='white')
plt.close(fig)
print('Saved:', *(str(p) for p in OUTPUT.glob('*.png')), sep='\n')
