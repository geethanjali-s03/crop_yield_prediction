import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, base64
from io import BytesIO

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=110, facecolor='white')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_b64

def get_palette():
    return ['#2E7D32','#388E3C','#43A047','#66BB6A','#A5D6A7','#1565C0','#1976D2','#2196F3','#F9A825','#EF6C00']

def eda_summary(df):
    summary = {
        'shape': df.shape,
        'missing': int(df.isnull().sum().sum()),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'describe': df.describe().round(2).to_dict()
    }
    return summary

def plot_yield_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df['Yield_Per_Hectare'], bins=40, kde=True, ax=axes[0], color='#2E7D32')
    axes[0].set_title('Yield Per Hectare Distribution', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Yield (kg/ha)')
    sns.boxplot(data=df, x='Crop', y='Yield_Per_Hectare', ax=axes[1], palette=get_palette())
    axes[1].set_title('Yield by Crop Type', fontsize=13, fontweight='bold')
    axes[1].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig_to_base64(fig)

def plot_rainfall_yield(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    crops = df['Crop'].unique()[:6]
    palette = get_palette()
    for i, crop in enumerate(crops):
        sub = df[df['Crop'] == crop]
        ax.scatter(sub['Rainfall'], sub['Yield_Per_Hectare'], label=crop,
                   alpha=0.5, s=20, color=palette[i % len(palette)])
    ax.set_xlabel('Rainfall (mm)', fontsize=11)
    ax.set_ylabel('Yield Per Hectare (kg)', fontsize=11)
    ax.set_title('Rainfall vs Crop Yield', fontsize=13, fontweight='bold')
    ax.legend(fontsize=8)
    plt.tight_layout()
    return fig_to_base64(fig)

def plot_correlation_heatmap(df):
    num_df = df.select_dtypes(include=[np.number])
    fig, ax = plt.subplots(figsize=(10, 7))
    mask = np.triu(np.ones_like(num_df.corr(), dtype=bool))
    sns.heatmap(num_df.corr(), mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
                ax=ax, linewidths=0.5, annot_kws={'size': 9})
    ax.set_title('Feature Correlation Heatmap', fontsize=13, fontweight='bold')
    plt.tight_layout()
    return fig_to_base64(fig)

def plot_model_comparison(results: dict):
    names = list(results.keys())
    r2s = [results[n]['R2'] for n in names]
    maes = [results[n]['MAE'] for n in names]
    palette = get_palette()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    bars = axes[0].barh(names, r2s, color=palette[:len(names)])
    axes[0].set_xlabel('R² Score', fontsize=11)
    axes[0].set_title('Model R² Comparison', fontsize=13, fontweight='bold')
    axes[0].set_xlim(0, 1.05)
    for bar, val in zip(bars, r2s):
        axes[0].text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.4f}', va='center', fontsize=9)

    bars2 = axes[1].barh(names, maes, color=palette[:len(names)])
    axes[1].set_xlabel('MAE (kg/ha)', fontsize=11)
    axes[1].set_title('Model MAE Comparison (lower=better)', fontsize=13, fontweight='bold')
    for bar, val in zip(bars2, maes):
        axes[1].text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}', va='center', fontsize=9)

    plt.tight_layout()
    return fig_to_base64(fig)

def plot_crop_season_yield(df):
    pivot = df.groupby(['Crop','Season'])['Yield_Per_Hectare'].mean().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 5))
    pivot.plot(kind='bar', ax=ax, colormap='tab10')
    ax.set_title('Average Yield by Crop and Season', fontsize=13, fontweight='bold')
    ax.set_xlabel('Crop')
    ax.set_ylabel('Avg Yield (kg/ha)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Season', bbox_to_anchor=(1.01, 1))
    plt.tight_layout()
    return fig_to_base64(fig)

def plot_feature_importance(df):
    """Compute a simple correlation-based feature importance with yield."""
    num_df = df.select_dtypes(include=[np.number])
    target = 'Yield_Per_Hectare'
    if target not in num_df.columns:
        return None
    corr = num_df.corr()[target].drop(target).abs().sort_values(ascending=True)
    palette = get_palette()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(corr.index, corr.values, color=palette[:len(corr)])
    ax.set_xlabel('|Correlation| with Yield', fontsize=11)
    ax.set_title('Feature Importance (Correlation-based)', fontsize=13, fontweight='bold')
    plt.tight_layout()
    return fig_to_base64(fig)
