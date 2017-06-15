from pymongo import MongoClient
# client = MongoClient('mongodb://localhost:27017/')


def drop_table():
    client = MongoClient()
    db = client.fraud_db
    coll = db.fraud_coll
    coll.drop()
    return True


def create_db():
    client = MongoClient()
    db = client.fraud_db
    coll = db.fraud_coll
    return True


if __name__ == '__main__':
    drop_table()
    create_db()
