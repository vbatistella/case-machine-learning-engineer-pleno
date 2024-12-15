from mongomock.mongo_client import MongoClient
from datetime import datetime, timezone

class InMemoryDatabase:
    _instance = None

    def __new__(cls) -> MongoClient:
        if cls._instance is None:
            client = MongoClient()
            cls._instance = client.get_database('memory_db')
        return super().__new__(cls)
    
    def add_inference(self, payload: dict, score: float, version: float) -> None:
        """
        Adds a new inference record to the database, including the input features, predicted score, 
        timestamp, and model version.

        Args:
            payload (dict): A dictionary containing the input features used for the model inference.
            score (float): The predicted score returned by the model.
            version (float): The version of the model used for generating the prediction.
        """
        data = {}
        data["features"] = payload
        data["score"] = score
        data["datetime"] = datetime.now(timezone.utc).isoformat()
        data["model"] = version
        self._instance["data_capture"].insert_one(data)
    
    def get_history(self) -> list:
        """
        Retrieves the history of all recorded inferences from the database.

        Returns:
            list: A list of dictionaries, where each dictionary represents a record of a previous 
                  inference
        """
        return list(self._instance["data_capture"].find())