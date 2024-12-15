import pickle
from numpy import array

DEFAULT_MODEL_PATH = "src/model/model.pkl"

def load_model_path(filename: str) -> None:
    """
    Loads a model from a specified file.

    Args:
        filename (str): The path to the model file that is to be loaded.

    Returns:
        object: The model object loaded from the specified file.
    """
    try:
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file '{filename}' not found.")
    except pickle.UnpicklingError:
        raise ValueError(f"Error unpickling model file '{filename}'.")

class InferenceModel():
    _model = None
    _version = 1.0

    def __new__(cls):
        if cls._model is None:
            cls._model = load_model_path(DEFAULT_MODEL_PATH)
        return super().__new__(cls)

    def inference(self, payload: dict) -> float:
        """
        Makes a prediction using the loaded model based on the provided input data.

        This method takes a dictionary of input features (`payload`), normalizes the data using the 
        model's scaler, performs prediction using the model, and then reverses the normalization of the 
        predicted value to return the final result.

        Args:
            payload (dict): A dictionary where the keys are the feature names and the values are the 
                            input data used for the model inference.

        Returns:
            float: The predicted value after transforming the model's output back to the original scale.
        """
        if not self._model:
            raise ValueError("Model is not loaded.")
        if not all(key in self._model for key in ["x_scaler", "model", "y_scaler"]):
            raise ValueError("Model components are missing.")
        
        try:
            data = array(list(payload.values())).reshape(1, -1)
            data_normalized = self._model["x_scaler"].transform(data)
            y_pred = self._model["model"].predict(data_normalized)
            y_pred = self._model["y_scaler"].inverse_transform(y_pred.reshape(-1, 1))
            return y_pred.tolist()[0][0]
        except Exception as e:
            raise ValueError(f"Inference failed: {str(e)}")
    
    @classmethod
    def update_model(cls, file_content) -> dict:
        """
        Updates the model with a new model file.

        Args:
            file_content (bytes): The content of the new model file, expected to be a pickle file.

        Returns:
            dict: A dictionary containing the status of the model update:
                - 'status' (str): The status of the update ("ok" if successful).
                - 'message' (str): A message indicating the result of the update.
        """
        try:
            new_model = pickle.loads(file_content)
            if not all(key in new_model for key in ["x_scaler", "model", "y_scaler"]):
                raise ValueError("Invalid model structure. Expected keys: 'x_scaler', 'model', 'y_scaler'.")

            cls._model = new_model
            cls._version = cls._version + 1.0
            return {"status": "ok", "message": "Model loaded successfully"}
        except pickle.UnpicklingError:
            raise ValueError("The uploaded file is not a valid pickle file.")
        except Exception as e:
            raise ValueError(f"Failed to load the model: {str(e)}")
    
    @classmethod
    def get_version(cls) -> dict:
        """
        Retrieves the current version of the model.

        Returns:
            float: the current version of the model:
        """
        return cls._version
