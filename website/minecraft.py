import os

days = int(input("How old is you minecraft world?   "))
print(days,"days, wow!")

minutes = (days*20)
hours = (minutes/60.000)
days = (hours/24)
weeks = (days/7)


played = "You've played"
print(played,minutes, "minutes of Minecraft")
print(played,"%.2f" % hours, "hours of Minecraft")
print(played,"%.2f" % days, "days of Minecraft")
print(played,"%.2f" % weeks, "weeks of Minecraft")

os.system("pause")


