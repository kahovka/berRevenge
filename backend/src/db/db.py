import pymongo


def connect_db(db_connection_string):
    try:
        db_client = pymongo.MongoClient(db_connection_string).birdWatch
        return db_client
    except NameError as e:
        print("Could not connect to db. {}".format(e))
