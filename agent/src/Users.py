from pymongo import MongoClient

class MongoHandler:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def getUserData(self, username):
        return self.collection.find_one({"username": username})

    def generateUserDataPrompt(self, user_data):
        if user_data:
            prompt = f"""
User Data:
- Username: {user_data.get('username')}
- Age: {user_data.get('age')}
- Weight: {user_data.get('weight')}
- Height: {user_data.get('height')}
- IMC: {user_data.get('imc')}
- Sex: {user_data.get('sex')}
- Body Fat: {user_data.get('body_fat')}
- Average Working Hours: {user_data.get('avg_working_hours')}
- Average Sleep Hours: {user_data.get('avg_sleep_hours')}
- Physical Activity: {user_data.get('physical_activity')}
- Type: {user_data.get('type')}
- Smoking: {user_data.get('smoking')}
- Alcohol Consumption: {user_data.get('alcohol_consumption')}
- Diseases: {', '.join(user_data.get('diseases', []))}
- Medication: {', '.join(user_data.get('medication', []))}
- Allergies: {', '.join(user_data.get('allergies', []))}
- Diet: {', '.join(user_data.get('diet', []))}
- Other: {user_data.get('other')}\n
            """
            return prompt
        return ""
    