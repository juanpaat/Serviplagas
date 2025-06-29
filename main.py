from data_processing.data_loader import load_data
from visualisations.Preventivos import generate_histogram
from summarizer.stats_generator import generate_summary
from summarizer.llm_narrator import summarize_with_llm
from reports.report_builder import build_report

from io import StringIO






# main.py

import pandas as pd
from transforms.roedores_transformer import transform_roedores_df

if __name__ == "__main__":
    roedores = pd.read_csv("data/roedores_raw.csv")
    transformed_roedores = transform_roedores_df(roedores)
    transformed_roedores.to_csv("data/roedores_transformed.csv", index=False)





# main.py

import pandas as pd
from transforms.lamparas_transformer import transform_lamparas_df

if __name__ == "__main__":
    lamparas = pd.read_csv("data/lamparas_raw.csv")
    transformed = transform_lamparas_df(lamparas)
    transformed.to_csv("data/lamparas_transformed.csv", index=False)