from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("linkdin_Job_data_mini.csv")
profile = ProfileReport(df)
profile.to_file("report_timeseries.html")
print("done")