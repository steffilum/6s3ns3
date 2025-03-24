from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

df = get_most_recent_df_of_date("GDP", "2020-01-01", fred)
df = pct_chg(df)
df.plot(y = "pct_chg")
plt.show()


#prediction using mean = 
print(df.pct_chg.mean())

#Prediction of new values for the model