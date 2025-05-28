import pandas as pd

try:
    totaldata = pd.read_csv('data/tracks.csv')
except: 
    print("make sure to run sortbytrack.py first!")
    exit()

sum = totaldata["ms_played"].sum()
years = sum//1000//3600//24//365
months = (sum//1000//3600//24%365)//30
weeks = (sum//1000//3600//24%365)%30//7
days = (sum//1000//3600//24%365)%30%7
hours = (sum//1000//3600%24)
minutes = (sum//1000//60%60)
seconds = (sum//1000%60)
print(
    years, "years" if years > 1 else "year", 
    months, "months" if months > 1 else "month", 
    weeks, "weeks" if weeks > 1 else "week", 
    days, "days" if days > 1 else "day", 
    hours, "hours" if hours > 1 else "hour", 
    minutes, "minutes" if minutes > 1 else "minute", 
    seconds, "seconds" if seconds > 1 else "second"
)