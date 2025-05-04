#!/usr/bin/env python3
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.stats import gaussian_kde

# Paths relative to scripts/
ROOT_DIR     = os.path.dirname(__file__)
LOG_DIR      = os.path.join(ROOT_DIR, '..', 'logs', 'wildberry_logs')
ANALYSIS_DIR = os.path.join(ROOT_DIR, '..', 'docs', 'images', 'wildberry_analysis')
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Parse boot time from filename
def parse_boot_time(fp):
    base = os.path.basename(fp)
    raw  = base[len('wildberry_'):-len('.txt')]
    date_p, time_p = raw.split('T')
    t = time_p.replace('-', ':')
    return datetime.fromisoformat(f"{date_p}T{t}")

# Load and normalize cycles
cycles = {}
for fp in sorted(glob.glob(os.path.join(LOG_DIR, 'wildberry_*.txt'))):
    boot  = parse_boot_time(fp)
    label = boot.strftime('%Y-%m-%d %H:%M')
    df = pd.read_csv(fp, delim_whitespace=True, comment='#',
                     names=['Timestamp','Boot','Temp','CPU%','Load1m'],
                     header=None, skiprows=2)
    df['Timestamp']   = pd.to_datetime(df['Timestamp'])
    df['Temp']        = df['Temp'].str.rstrip('°C').astype(float)
    df['CPU%']        = df['CPU%'].str.rstrip('%').astype(float)
    df['Load1m']      = df['Load1m'].astype(float)
    t0 = df['Timestamp'].min()
    df['Elapsed_min'] = (df['Timestamp'] - t0).dt.total_seconds() / 60.0
    cycles[label] = df

# Precompute summary data
durations   = {label: df['Elapsed_min'].max() for label, df in cycles.items()}
avg_cpu     = {label: df['CPU%'].mean()       for label, df in cycles.items()}
avg_temp    = {label: df['Temp'].mean()         for label, df in cycles.items()}

# 1) Temperature overlay
plt.figure(figsize=(8,5))
for label, df in cycles.items():
    plt.plot(df['Elapsed_min'], df['Temp'], marker='o', linestyle='-', label=label)
plt.xlabel('Minutes since first log (≈ boot)')
plt.ylabel('CPU Temperature (°C)')
plt.title('Temperature Over Each Boot Cycle')
plt.legend(loc='best', fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, 'temperature_overlay.png'))
plt.close()

# 2) CPU% overlay
plt.figure(figsize=(8,5))
for label, df in cycles.items():
    plt.plot(df['Elapsed_min'], df['CPU%'], marker='o', linestyle='-', label=label)
plt.xlabel('Minutes since first log (≈ boot)')
plt.ylabel('CPU Utilization (%)')
plt.title('CPU% Over Each Boot Cycle')
plt.legend(loc='best', fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, 'cpu_percent_overlay.png'))
plt.close()

# 3) Load1m overlay
plt.figure(figsize=(8,5))
for label, df in cycles.items():
    plt.plot(df['Elapsed_min'], df['Load1m'], marker='o', linestyle='-', label=label)
plt.xlabel('Minutes since first log (≈ boot)')
plt.ylabel('1-Minute Load Average')
plt.title('1-Min Load Average Over Each Boot Cycle')
plt.legend(loc='best', fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, 'load_average_overlay.png'))
plt.close()

# 4) Duration bar chart labeled by avg CPU% & avg Temp
labels = [f"{label}\n{avg_cpu[label]:.1f}% CPU, {avg_temp[label]:.1f}°C" for label in durations.keys()]
times  = list(durations.values())
xpos   = range(len(labels))
plt.figure(figsize=(8,5))
plt.bar(xpos, times, edgecolor='black')
plt.xticks(xpos, labels, rotation=45, ha='right')
plt.ylabel('Cycle Duration (min)')
plt.title('Duration of Each Boot Cycle (labeled by Avg CPU% & Temp)')
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, 'cycle_durations.png'))
plt.close()

# 5) Duration distribution histogram + KDE
vals = np.array(times)
plt.figure(figsize=(8,5))
plt.hist(vals, bins=10, density=True, alpha=0.6, edgecolor='black')
if len(vals) > 1:
    kde = gaussian_kde(vals)
    x = np.linspace(vals.min(), vals.max(), 200)
    plt.plot(x, kde(x), 'r-', lw=2)
else:
    plt.text(0.5, 0.5, 'KDE requires ≥2 cycles', ha='center', va='center', transform=plt.gca().transAxes)
plt.xlabel('Cycle Duration (min)')
plt.ylabel('Density')
plt.title('Distribution of Boot Cycle Durations')
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, 'duration_histogram.png'))
plt.close()

# 6) Duration boxplot
plt.figure(figsize=(6,4))
plt.boxplot(vals, vert=False, widths=0.7)
plt.xlabel('Cycle Duration (min)')
plt.title('Boxplot of Boot Cycle Durations')
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, 'duration_boxplot.png'))
plt.close()

# Summary stats
\
total_cycles     = len(durations)
\
avg_duration     = np.mean(times)
\
min_duration     = np.min(times)
\
max_duration     = np.max(times)
\
# also in hours
\
avg_duration_hr  = avg_duration / 60.0
\
min_duration_hr  = min_duration / 60.0
\
max_duration_hr  = max_duration / 60.0
\

\
avg_cpu_overall  = np.mean(list(avg_cpu.values()))
\
avg_temp_overall = np.mean(list(avg_temp.values()))
\

\
print("Analysis complete!")
\
print(f"  Logs analyzed: {total_cycles} cycles")
\
print(f"  Avg duration: {avg_duration:.2f} min ({avg_duration_hr:.2f} hr), min: {min_duration:.2f} min ({min_duration_hr:.2f} hr), max: {max_duration:.2f} min ({max_duration_hr:.2f} hr)")
\
print(f"  Overall avg CPU%: {avg_cpu_overall:.1f}%")
\
print(f"  Overall avg Temp: {avg_temp_overall:.1f}°C")
\
print(f"PNGs saved in {ANALYSIS_DIR}")
