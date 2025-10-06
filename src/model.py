import os
import pickle
import pandas as pd

class DiabetesModel:
    def __init__(self):
        
        self.expected_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
        # Load the model
        model_path = os.path.join(os.getcwd(), 'models', 'random_forest_model.pkl')
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)
        
    def predict(self, input_data):
        """
        Make predictions on input data
        
        Args:
            X: Input features (array-like) containing:
               [Pregnancies, Glucose, BloodPressure, SkinThickness, 
                Insulin, BMI, DiabetesPedigreeFunction, Age]
        
        Returns:
            Predictions array (0 for non-diabetic, 1 for diabetic)
        """

        is_valid, errors = self._validate_input(input_data)
        if not is_valid:
            return {"errors": errors}, 400, {'Content-Type': 'application/json'}

        X = pd.DataFrame.from_dict(input_data, orient='index').T
        X = X[self.expected_columns]  # Ensure correct column order
        
        prediction = self.model.predict(X)
        return str(prediction[0]), 200, {'Content-Type': 'text/plain'}
    
    def predict_proba(self, input_data):
        """
        Get prediction probabilities
        
        Args:
            X: Input features (array-like)
        
        Returns:
            Probability array
        """

        is_valid, errors = self._validate_input(input_data)
        if not is_valid:
            return {"errors": errors}, 400, {'Content-Type': 'application/json'}

        X = pd.DataFrame.from_dict(input_data, orient='index').T
        X = X[self.expected_columns]  # Ensure correct column order
            
        return self.model.predict_proba(X)
    
    def _validate_input(self, input_data):
        """
        Validate input data
        
        Args:
            input_data: Dictionary containing input features
            
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # Define valid ranges for each feature
        valid_ranges = {
            'Pregnancies': (0, 17),
            'Glucose': (40, 600),
            'BloodPressure': (20, 200),
            'SkinThickness': (3, 150),
            'Insulin': (10, 1000),
            'BMI': (15, 100),
            'DiabetesPedigreeFunction': (0.0, 3),
            'Age': (20, 100)
        }
        
        for column in self.expected_columns:
            if column not in input_data:
                errors.append(f"Missing required field: {column}")
                continue
                
            value = input_data[column]
            min_val, max_val = valid_ranges[column]
            
            if not isinstance(value, (int, float)):
                errors.append(f"{column} must be a number")
            elif value < min_val or value > max_val:
                errors.append(f"{column} must be between {min_val} and {max_val}")
        
        return len(errors) == 0, errors