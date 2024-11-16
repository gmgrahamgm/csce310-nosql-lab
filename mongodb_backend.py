import os
from dotenv import load_dotenv
from pymongo import MongoClient


class Mongodb:
    def __init__(self):
        load_dotenv()
        db_password = os.getenv('DB_PASSWORD')
        if not db_password:
            raise ValueError(
                "DB_PASSWORD is not set in the environment variables.")

        connection_string = f"mongodb+srv://grahamd:{
            db_password}@cluster0.dxb95.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        self.client = MongoClient(connection_string)
        self.db = self.client['Votes']

    def get_all_candidates(self):
        try:
            candidates = list(self.db.candidates.find(
                {}, {"_id": 0, "candidateName": 1}))
            return [candidate['candidateName'] for candidate in candidates]
        except Exception as e:
            print(f"Error fetching candidates: {e}")
            return []

    def post_ballot(self, voterID, regPIN, firstChoice, secondChoice, thirdChoice):
        try:
            ballot = {
                "voterID": voterID,
                "regPIN": regPIN,
                "firstChoice": firstChoice,
                "secondChoice": secondChoice,
                "thirdChoice": thirdChoice
            }
            self.db.ballots.insert_one(ballot)
            print("Ballot successfully posted.")
        except Exception as e:
            print(f"Error posting ballot: {e}")
