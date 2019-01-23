from pymongo import MongoClient

client = MongoClient("serval.desy.de", 27017)
#client = MongoClient("")

db = client.primer

coll = db.dataset1


from datetime import datetime

#result = db.restaurants.delete_many({"borough": "Manhattan"})
#print("deleted {} entries".format(result.deleted_count))


result = db.restaurants.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Zulu",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)

result = db.restaurants.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Bronx",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)


print(result.inserted_id)


#cursor = db.restaurants.find()
#cursor = db.restaurants.find({"address.zipcode": "10075"})
#cursor = db.restaurants.find({"grades.score": {"$gt": 30}})
#cursor = db.restaurants.find({"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]})

#cursor = db.restaurants.find().sort([
#    ("borough", pymongo.ASCENDING),
#    ("address.zipcode", pymongo.ASCENDING)
#])


result = db.restaurants.update_one(
    {"name": "Vella"},
    {
        "$set": {
            "cuisine": "American (New)"
        },
        "$currentDate": {"lastModified": True}
    }
)

'''
result = db.restaurants.update_many(
    {"address.zipcode": "10016", "cuisine": "Other"},
    {
        "$set": {"cuisine": "Category To Be Determined"},
        "$currentDate": {"lastModified": True}
    }
)
'''

print("updateed {} entries".format(result.matched_count))

cursor = db.restaurants.find({"cuisine": "American (New)"})

for document in cursor:
    print(document)


cursor = db.restaurants.aggregate(
    [
        {"$group": {"_id": "$borough", "count": {"$sum": 1}}}
    ]
)

for document in cursor:
    print(document)

# multiple stages
cursor = db.restaurants.aggregate(
    [
        {"$match": {"borough": "Bronx", "cuisine": "Italian"}},
        {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}}
    ]
)

print("2-stage query")

for document in cursor:
    print(document)


#db.restaurants.drop()
