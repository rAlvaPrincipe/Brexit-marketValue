import sys
from pymongo import MongoClient

# PRINT ALL THE DAYS ON CONSOLE
#########
# lines = open('days.txt').read().split("\n")
#
# #[
# output = "["
#
# # "YYYY-MM-DD",
# counter = 0
# for line in lines:
#     counter = counter + 1
#     if line != "":
#         output = output + "\'" + str(line) + "\', "
#     if counter % 5 == 0:
#         output = output + "\n\t\t\t\t "
#
# output = output[:-2]
#
# # ]
# output = output + "]"
#
# print output


# LIST

lines = open('days.txt').read().split("\n")
days = {}

for line in lines:
    if line != "":
        days[str(line)] = 0

try:
    client = MongoClient('localhost', 27017)
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to server: %s" % e

db = client.experiments

print("\nreading:")
for day in days:
    count = db.tweets.find({"site":"twitter.com", "date":{"$regex": day}}, { "text": 1, "date": 1}).count()
    days[day] = int(count)
    print(day+": "+str(count))


print("\n\n saving:")
out_file = open("days_count.txt", "w")
for day in days:
    out_file.write(day + "\t" + str(days[day]) + "\n")
    print("saving:" + day+":" + str(days[day]))

out_file.close()
