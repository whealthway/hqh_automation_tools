
def get_complete_name(User):
    complete_name = {
        "$cond": [
            {
                "$and": [
                    {"$eq": [
                        {"$ifNull": [{"$arrayElemAt": [f"{User}.thirdname", 0]}, ""]}, ""]},
                    {"$eq": [
                        {"$ifNull": [{"$arrayElemAt": [f"{User}.name", 0]}, ""]}, ""]},
                    {"$eq": [
                        {"$ifNull": [{"$arrayElemAt": [f"{User}.middlename", 0]}, ""]}, ""]},
                    {"$eq": [
                        {"$ifNull": [{"$arrayElemAt": [f"{User}.lastname", 0]}, ""]}, ""]}
                ]
            },
            None,
            {
                "$concat": [

                    {"$ifNull": [
                        {"$arrayElemAt": [f"{User}.thirdname", 0]}, ""]},
                    # {
                    #     "$cond": {
                    #         "if": {
                    #             "$or": [
                    #                 { "$gt": [{ "$size": f"{User}.name" }, 0] },
                    #                 { "$gt": [{ "$size": f"{User}.firstname" }, 0] }
                    #             ]
                    #         },
                    #         "then": ", ",
                    #         "else": " "
                    #     }
                    # },
                    ", ",
                    {"$ifNull": [{"$arrayElemAt": [f"{User}.name", 0]}, ""]},
                    {"$ifNull": [
                        {"$arrayElemAt": [f"{User}.firstname", 0]}, ""]},
                    " ",
                    {"$ifNull": [
                        {"$arrayElemAt": [f"{User}.middlename", 0]}, ""]},
                    " ",
                    {"$ifNull": [{"$arrayElemAt": [f"{User}.lastname", 0]}, ""]}
                ]
            }
        ]
    }

    return complete_name
