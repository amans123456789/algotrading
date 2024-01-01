from config import config
from download_functions.download import daily_data, minute_data

fin_min, res_min, vx_min = (minute_data(config["tickers_NS"] ,"2023-12-21", "2023-12-24"))
fin_day, res_day, vx_day = (daily_data(config["tickers_NS"],"2023-12-21", "2023-12-24"))

fin_min.to_csv("market_data/fin_min.csv")
fin_day.to_csv("market_data/fin_day.csv")
