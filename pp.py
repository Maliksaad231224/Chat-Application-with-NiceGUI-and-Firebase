import requests
import pandas as pd

r = requests.get("https://oec.world/olap-proxy/data?time=time.latest&Trade+Flow=2&cube=trade_s_usa_port_m_hs&drilldowns=Time,Product,Trade+Flow&measures=Trade+Value&token=YOUR_API_TOKEN")
df = pd.DataFrame(r.json()["data"])
print(df.head())