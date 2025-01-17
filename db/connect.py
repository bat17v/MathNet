import pymongo
import configparser
import datetime
import verification
from bson import ObjectId


class NoProblemText(Exception):
    pass


class MongoService:
    def __init__(self):
        configload = configparser.RawConfigParser()
        configload.read('../server.properties')
        self.client = pymongo.MongoClient(configload.get('db', 'mongourl'))

    def create_user(self, login, name, password, email):
        db = self.client.math_net
        users_collection = db.users

        now = datetime.datetime.utcnow()
        query = {"login": login}
        cursor = users_collection.find(query)
        q = 0
        for doc in cursor:
            q += 1
        if q >= 1:
            print('login already used')
            return 'Error'
        new_user = {
            "login": login,
            "name": name,
            "created": now,
            "last_login": now,
            "password": password,
            "email": email
        }
        print(verification.send_email('morcik155@gmail.com'))

        result = users_collection.insert_one(new_user)


        document_id = result.inserted_id
        print(f"_id of inserted document: {document_id}")
        return document_id

    def add_problem(
            self,
            user: str,
            text: str,
            solution: str = '',
            answer: str = '',
            answerIsSolution: bool = False
    ):
        db = self.client.math_net
        problems_collection = db.problems

        now = datetime.datetime.utcnow()

        if text.isspace():
            raise NoProblemText()

        new_problem = {
            'user': ObjectId(user),
            'text': text,
            'tags': [],
            'image': None,
            'creationDate': now,
            'solution': solution,
            'answer': answer,
            'answerIsSolution': answerIsSolution,
            'open': False,
            'moderators': [],
            'likes': [],
            'comments': []
        }

        result = problems_collection.insert_one(new_problem)

        document_id = result.inserted_id
        print(f"_id of inserted document: {document_id}")
        return document_id

    def update_problem(
            self,
            problem_id: str,
            text: str,
            solution: str = '',
            answer: str = '',
            answerIsSolution: bool = False
    ):
        db = self.client.math_net
        problems_collection = db.problems

        if text.isspace():
            raise NoProblemText()

        correction = {
            'text': text,
            'solution': solution,
            'answer': answer,
            'answerIsSolution': answerIsSolution
        }

        problems_collection.update_one({'_id': ObjectId(problem_id)}, {'$set': correction})

    def add_like(self, problem_id: str, user: str, delete_like: bool):
        db = self.client.math_net
        problems_collection = db.problems

        if delete_like:
            problems_collection.update_one({'_id': ObjectId(problem_id)}, {'&pull': ObjectId(user)})
        else:
            problems_collection.update_one({'_id': ObjectId(problem_id)}, {'$addToSet': ObjectId(user)})
