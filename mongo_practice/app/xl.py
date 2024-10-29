import asyncio
from database import get_database

gd = get_database()

# gd["users"].insertOne(
# gd.users.insert_one(
#    { 
#        "_id" : 4,
#        "name": "kapil",
#        "email" : "example@gmail.com",
#        "company_name" : "bridgefix1"
#     }

# )


# gd.items.insert_one(
#     {
#         "_id" : 9,
#         "name" : "mobiel",
#         "price" : 100,
#         "working" : ["run","hang"]

#     }
# )

# class Item(BaseModel):
#     _id: int
#     name: str
#     description: Optional[str] = None
#     price: float
#     date_: date = None

# pipeline = [
#         {
#             "$facet": {
#                 "total_count": [
#                     { "$count": "count" }
#                 ],
#                 "average_price": [
#                     { "$group": { "_id": None, "averagePrice": { "$avg": "$price" } } }
#                 ],
#                 "items_by_name": [
#                     { "$group": { "_id": "$name", "count": { "$sum": 1 } } },
#                     { "$sort": { "count": -1 } }
#                 ]
#             }
#         }
#     ]
# results = gd.items.aggregate(pipeline).to_list(length=None)
# print(results)

# async def fetch_data():
#     pipeline = [
#         {
#             "$facet": {
#                 "total_count": [
#                     {"$count": "count"}
#                 ],
#                 "average_price": [
#                     {"$group": {"_id": None, "averagePrice": {"$avg": "$price"}}}
#                 ],
#                 "items_by_name": [
#                     {"$group": {"_id": "$name", "count": {"$sum": 1}}},
#                     {"$sort": {"count": -1}}
#                 ]
#             }
#         }
#     ]
#     # import pdb;pdb.set_trace()
#     results = await gd.items.aggregate(pipeline).to_list(length=None)
#     print(results)
#     print("=======================================")
# =============================
    # total_count_pipeline = [
    #     {"$count": "count"}
    # ]

    # # Second stage: Calculate average price
    # average_price_pipeline = [
    #     {"$group": {"_id": "$name", "averagePrice": {"$avg": "$price"}}}
    # ]

    # # Third stage: Count items by name
    # items_by_name_pipeline = [
    #     {"$group": {"_id": "$name", "count": {"$sum": 1}}},
    #     {"$sort": {"count": -1}}
    # ]

    # # Execute each pipeline separately and handle results accordingly
    # total_count_result = await gd.items.aggregate(total_count_pipeline).to_list(length=None)
    # average_price_result = await gd.items.aggregate(average_price_pipeline).to_list(length=None)
    # items_by_name_result = await gd.items.aggregate(items_by_name_pipeline).to_list(length=None)

    # result = [items_by_name_result, average_price_result, total_count_result]
    # print(result)
# =================
# Run the async function
# if __name__ == "__main__":
#     asyncio.run(fetch_data())


async def unwind():
    pipeline = [
        {
            "$unwind" : "$working"
        },
        {
            "$group" : {"_id" : "$working"}
        }
    ]
    result = await gd.items.aggregate(pipeline).to_list(length=None)
    print(result)
    print(gd.command('collStats', "items"))
if __name__ == "__main__":
    asyncio.run((unwind()))
