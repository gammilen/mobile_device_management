import pandas as pd
import matplotlib.pyplot as plt

def make_time_traffic_plot(df):
	idx = pd.to_datetime(df["ts"])
	df2 = pd.DataFrame(list(df["ibyt"]), index=idx)
	
	plt.xlabel("time")
	plt.ylabel("traffic")
	labels = [pd.Timestamp('2020-02-25 11:50:00'), pd.Timestamp('2020-02-25 11:55:00'), pd.Timestamp('2020-02-25 12:00:00'), pd.Timestamp('2020-02-25 12:05:00'), pd.Timestamp('2020-02-25 12:10:00'), pd.Timestamp('2020-02-25 12:15:00'), pd.Timestamp('2020-02-25 12:20:00'), pd.Timestamp('2020-02-25 12:25:00'), pd.Timestamp('2020-02-25 12:30:00')]
	plt.xticks(labels, [str(i)[11:16] for i in labels], rotation=60)
	plt.scatter(df2.index, df2, s=1)
	plt.show()

def make_duration_traffic_plot(df):
	plt.xlabel("duration")
	plt.ylabel("traffic")
	plt.scatter(df["td"], df["ibyt"], s=1)
	plt.show()