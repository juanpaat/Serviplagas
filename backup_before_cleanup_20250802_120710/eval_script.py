from data_processing.data_loader import load_data
from data_processing.data_cleaner import transform_preventivos_df

from visualisations.Preventivos import (
    generate_order_area_plot,
    generate_plagas_timeseries_facet,
    generate_total_plagas_trend_plot)

import matplotlib.pyplot as plt

df_preventivo = transform_preventivos_df(load_data('data/Preventivos.csv'))


fig = generate_total_plagas_trend_plot(df_preventivo)
plt.show()
