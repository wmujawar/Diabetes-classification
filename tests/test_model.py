import pytest
import os
import sys
import pandas as pd
import numpy as np
from unittest.mock import patch, mock_open, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model import DiabetesModel


class TestDiabetesModel:
    
    @pytest.fixture
    def mock_model(self):
        """Mock the XGBoost model for testing"""
        mock_xgb_model = MagicMock()
        mock_xgb_model.predict.return_value = np.array([0])
        mock_xgb_model.predict_proba.return_value = np.array([[0.7, 0.3]])
        return mock_xgb_model
    
    @pytest.fixture
    def valid_input_data(self):
        """Valid input data for testing"""
        return {
            'Pregnancies': 2,
            'Glucose': 120,
            'BloodPressure': 80,
            'SkinThickness': 25,
            'Insulin': 100,
            'BMI': 25.5,
            'DiabetesPedigreeFunction': 0.5,
            'Age': 35
        }
    
    @pytest.fixture
    def diabetes_model(self, mock_model):
        """Create a DiabetesModel instance with mocked XGBoost model"""
        with patch('builtins.open', mock_open(read_data=b'mock_model_data')), \
             patch('pickle.load', return_value=mock_model):
            return DiabetesModel()
    
    def test_model_initialization(self, diabetes_model):
        """Test that the model initializes correctly"""
        assert diabetes_model.model is not None
        assert len(diabetes_model.expected_columns) == 8
        expected_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        assert diabetes_model.expected_columns == expected_cols
    
    def test_predict_with_valid_input(self, diabetes_model, valid_input_data):
        """Test prediction with valid input data"""
        result, status_code, content_type = diabetes_model.predict(valid_input_data)
        
        assert status_code == 200
        assert content_type == {'Content-Type': 'text/plain'}
        assert result == '0'  # Mocked to return 0
    
    def test_predict_with_missing_field(self, diabetes_model):
        """Test prediction with missing required field"""
        incomplete_data = {
            'Pregnancies': 2,
            'Glucose': 120,
            'BloodPressure': 80,
            # Missing other required fields
        }
        
        result, status_code, content_type = diabetes_model.predict(incomplete_data)
        
        assert status_code == 400
        assert content_type == {'Content-Type': 'application/json'}
        assert 'errors' in result
        assert len(result['errors']) > 0
        assert any('Missing required field' in error for error in result['errors'])
    
    def test_predict_with_invalid_data_types(self, diabetes_model):
        """Test prediction with invalid data types"""
        invalid_data = {
            'Pregnancies': 'not_a_number',
            'Glucose': 120,
            'BloodPressure': 80,
            'SkinThickness': 25,
            'Insulin': 100,
            'BMI': 25.5,
            'DiabetesPedigreeFunction': 0.5,
            'Age': 35
        }
        
        result, status_code, content_type = diabetes_model.predict(invalid_data)
        
        assert status_code == 400
        assert 'errors' in result
        assert any('must be a number' in error for error in result['errors'])
    
    def test_predict_with_out_of_range_values(self, diabetes_model):
        """Test prediction with values outside valid ranges"""
        out_of_range_data = {
            'Pregnancies': -1,  # Below minimum
            'Glucose': 700,     # Above maximum
            'BloodPressure': 80,
            'SkinThickness': 25,
            'Insulin': 100,
            'BMI': 25.5,
            'DiabetesPedigreeFunction': 0.5,
            'Age': 35
        }
        
        result, status_code, content_type = diabetes_model.predict(out_of_range_data)
        
        assert status_code == 400
        assert 'errors' in result
        assert len(result['errors']) >= 2  # At least 2 out-of-range errors
    
    def test_predict_proba_with_valid_input(self, diabetes_model, valid_input_data):
        """Test prediction probabilities with valid input"""
        result = diabetes_model.predict_proba(valid_input_data)
        
        assert isinstance(result, np.ndarray)
        assert result.shape == (1, 2)  # One sample, two classes
        assert np.allclose(result, [[0.7, 0.3]])  # Mocked values
    
    def test_predict_proba_with_invalid_input(self, diabetes_model):
        """Test prediction probabilities with invalid input"""
        invalid_data = {
            'Pregnancies': 'invalid',
            'Glucose': 120,
            'BloodPressure': 80,
            'SkinThickness': 25,
            'Insulin': 100,
            'BMI': 25.5,
            'DiabetesPedigreeFunction': 0.5,
            'Age': 35
        }
        
        result, status_code, content_type = diabetes_model.predict_proba(invalid_data)
        
        assert status_code == 400
        assert 'errors' in result
    
    def test_validate_input_all_valid(self, diabetes_model, valid_input_data):
        """Test input validation with all valid data"""
        is_valid, errors = diabetes_model._validate_input(valid_input_data)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_input_boundary_values(self, diabetes_model):
        """Test input validation with boundary values"""
        # Test minimum boundary values
        min_boundary_data = {
            'Pregnancies': 0,
            'Glucose': 40,
            'BloodPressure': 20,
            'SkinThickness': 3,
            'Insulin': 10,
            'BMI': 15,
            'DiabetesPedigreeFunction': 0.0,
            'Age': 20
        }
        
        is_valid, errors = diabetes_model._validate_input(min_boundary_data)
        assert is_valid is True
        assert len(errors) == 0
        
        # Test maximum boundary values
        max_boundary_data = {
            'Pregnancies': 17,
            'Glucose': 600,
            'BloodPressure': 200,
            'SkinThickness': 150,
            'Insulin': 1000,
            'BMI': 100,
            'DiabetesPedigreeFunction': 3,
            'Age': 100
        }
        
        is_valid, errors = diabetes_model._validate_input(max_boundary_data)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_input_beyond_boundaries(self, diabetes_model):
        """Test input validation with values beyond boundaries"""
        beyond_boundary_data = {
            'Pregnancies': 18,    # Above max
            'Glucose': 39,        # Below min
            'BloodPressure': 201, # Above max
            'SkinThickness': 2,   # Below min
            'Insulin': 1001,      # Above max
            'BMI': 14,            # Below min
            'DiabetesPedigreeFunction': 3.1,  # Above max
            'Age': 19             # Below min
        }
        
        is_valid, errors = diabetes_model._validate_input(beyond_boundary_data)
        assert is_valid is False
        assert len(errors) == 8  # All fields should have errors
    
    @pytest.mark.parametrize("field,value,expected_error", [
        ('Pregnancies', 'string', 'must be a number'),
        ('Glucose', None, 'must be a number'),
        ('BMI', [], 'must be a number'),
        ('Age', {}, 'must be a number'),
    ])
    def test_validate_input_invalid_types(self, diabetes_model, valid_input_data, field, value, expected_error):
        """Test input validation with various invalid data types"""
        test_data = valid_input_data.copy()
        test_data[field] = value
        
        is_valid, errors = diabetes_model._validate_input(test_data)
        assert is_valid is False
        assert any(expected_error in error for error in errors)
    
    def test_dataframe_creation_and_column_order(self, diabetes_model, valid_input_data, mock_model):
        """Test that DataFrame is created correctly with proper column order"""
        # This test ensures the DataFrame creation and column ordering works correctly
        diabetes_model.predict(valid_input_data)
        
        # Verify that the model's predict method was called
        mock_model.predict.assert_called_once()
        
        # Get the DataFrame that was passed to the model
        call_args = mock_model.predict.call_args[0][0]
        assert isinstance(call_args, pd.DataFrame)
        assert list(call_args.columns) == diabetes_model.expected_columns
    
    def test_prediction_return_format(self, diabetes_model, valid_input_data):
        """Test that prediction returns the correct format"""
        result, status_code, content_type = diabetes_model.predict(valid_input_data)
        
        assert isinstance(result, str)
        assert isinstance(status_code, int)
        assert isinstance(content_type, dict)
        assert status_code in [200, 400]
        assert 'Content-Type' in content_type
    
    @patch('os.path.join')
    @patch('os.getcwd')
    def test_model_path_construction(self, mock_getcwd, mock_join):
        """Test that model path is constructed correctly"""
        mock_getcwd.return_value = '/fake/path'
        mock_join.return_value = '/fake/path/models/XGBoost_model.pkl'
        
        with patch('builtins.open', mock_open(read_data=b'mock_model_data')), \
             patch('pickle.load', return_value=MagicMock()):
            DiabetesModel()
        
        mock_getcwd.assert_called_once()
        mock_join.assert_called_once_with('/fake/path', 'models', 'XGBoost_model.pkl')