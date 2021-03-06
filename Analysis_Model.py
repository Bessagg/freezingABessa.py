import os
import glob
import h2o
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
current_dir = os.getcwd()
temp_dir = os.path.join(current_dir, "temp")
h2o.init()
folders = os.listdir(temp_dir)
models = dict()
for folder in folders:
    files = os.listdir(os.path.join(temp_dir, folder))
    files.sort(key=lambda x: x.split("_")[-2])
    files.sort(key=lambda x: x.split("_")[-1])
    models[folder] = h2o.load_model(os.path.join(temp_dir, folder, files[-1]))

AutoML = models['AutoML_model']
DRF_model = models['best_DRF_model']
GBM_model = models['best_GBM_model']

df = pd.DataFrame()
df_var_importance = pd.DataFrame()
for model in models:
    data = dict()
    data['model'] = model
    data['mae'] = models[model].mae()
    data['mae_v'] = models[model].mae(valid=True)
    data['r2'] = models[model].r2()
    data['r2_v'] = models[model].r2(valid=True)
    new_row = df.from_dict([data])
    df = pd.concat([df, new_row], ignore_index=True)
    if models[model].varimp() is not None:
        var_importance = models[model].varimp(True)
        var_importance['model'] = model
        df_var_importance = pd.concat([df_var_importance, var_importance], ignore_index=True)
        print(var_importance)

g = sns.catplot(data=df_var_importance, kind="bar", x="variable", y="scaled_importance", hue="model")
g.fig.set_size_inches(18, 5)
sns.move_legend(g, "upper left")


