from bing_image_urls import bing_image_urls
import pandas as pd

df = pd.read_csv(r"csv\prodotti.csv", delimiter=';')
data = df.to_dict(orient='records')
for e in data:
    if isinstance(e["image_url"], float):
        e["image_url"] = bing_image_urls(e["product_name"], limit=1)
    new_df = pd.DataFrame.from_dict(e, orient='index')
new_df.to_csv(r"csv\prodotti2.csv")