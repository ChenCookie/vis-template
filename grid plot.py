import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm

df_40_file = pd.read_csv('/Users/cookie/Downloads/gpu_usage.csv')
df_40log_file = pd.read_csv('/Users/cookie/Downloads/workflow_time.csv')

df_40_file.columns = df_40_file.columns.str.strip()
df_40log_file.columns = df_40log_file.columns.str.strip()

# double check for time formet
df_40_file['time'] = pd.to_datetime(df_40_file['time'])
df_40log_file['start_time'] = pd.to_datetime(df_40log_file['start_time'])
df_40log_file['end_time'] = pd.to_datetime(df_40log_file['end_time'])


df_dict = {
    'Time': list(df_40_file['time']),
    'GPU_usage_percentage': list(df_40_file['GPU_usage_percentage']),
    'u2': list(df_40_file['u2'])
}

for teak_num in np.unique(df_40log_file['workflow']):
    df_workflow_filtered = df_40log_file[df_40log_file['workflow'] == teak_num]
    time_mask = pd.Series([False] * len(df_40_file))
    for _, row in df_workflow_filtered.iterrows():
        time_mask |= (df_40_file['time'] >= row['start_time']) & (df_40_file['time'] <= row['end_time'])
    df_dict ['in_workflow_' + str(teak_num) + '_time'] = list(time_mask) 
df_plot = pd.DataFrame(df_dict)




fig, axs = plt.subplots(2, 1, figsize=(15, 8), sharex=True)


workflow_ids = sorted(np.unique(df_40log_file['workflow']))
colors = cm.get_cmap('tab10', len(workflow_ids))
workflow_color_map = {wid: colors(i) for i, wid in enumerate(workflow_ids)}

# lolipop plot
for _, row in df_40log_file.iterrows():
    wid = row['workflow']
    color = workflow_color_map[wid]
    axs[0].plot([row['start_time'], row['end_time']], [wid, wid], color=color, marker='o', linewidth=2, label=f'workflow {wid}')

handles, labels = axs[0].get_legend_handles_labels()
by_label = dict(zip(labels, handles))
axs[0].set_ylabel('workflow number')
axs[0].set_title('workflow time length')
axs[0].legend(by_label.values(), by_label.keys(), title="Workflow")


axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
axs[0].xaxis.set_tick_params(rotation=45)

# line plot
axs[1].plot(df_plot['Time'], df_plot['GPU_usage_percentage'], label='GMP (%)', linewidth=1)
if 'u2' in df_plot.columns:
    axs[1].plot(df_plot['Time'], df_plot['u2'], label='u2', linewidth=1)
axs[1].set_ylabel('Usage')
axs[1].set_title('GPU Usage')
axs[1].legend()

axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
axs[1].xaxis.set_tick_params(rotation=45)

plt.tight_layout()
plt.show()