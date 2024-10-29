import asyncio
from database import get_database

gd = get_database()


# gd["users"].insertOne(
# gd.users.insert_one(
#    { 
#        "_id" : 4,
#        "name": "kapil",
#        "email" : "example@gmail.com",
#        "company_name" : ""
#     }

# )


# gd.items.insert_one(
#     {
#         "_id" : 6,
#         "name" : "mobiel",
#         "price" : 100
#     }
# )

def update_():
    update_one = gd.items.update_many({"name" : "mobile"}, {"$set" : {"price" :1110}})
    return (update_one)
# print(update_())

def find_():
    find_all = gd.items.find()
    import pdb;pdb.set_trace()
    return find_all
# print(find_())combinations_with_replacement



async def bucket_():
    pipeline = [
{
                # "price":[
                #     {
                        "$bucket": {
                            "groupBy": "$price",
                            "boundaries": [100, 1500],
                             "default": "Other",
                            "output": {
                                "count": {"$sum": 1},
                                "include_fields": {"$push": {"name": "$name", "price": "$price"}},
                                "average_price": {"$avg": "$price"}
                            }
                        }
                #     }
                # ]
                
            } 
    ]
    
    res =  await gd.items.aggregate(pipeline).to_list(length=None)
    return res

# def main():
#     result = asyncio.run(bucket_())
#     print(result)

# if __name__ == "__main__":
#     main()


async def lookup_():
    pipleline = [
                    {
                    "$lookup": {
                            "from": "users",
                            "localField": "_id",
                            "foreignField": "_id",  
                            "as": "user_info"  
                        }
                    },
                    {
                        "$unwind": "$user_info"
                    }
                ]
    res = await gd.items.aggregate(pipleline).to_list(length=None)
    return res

def main():
    result = asyncio.run(lookup_())
    print(result)

if __name__ == '__main__':
    main()                
