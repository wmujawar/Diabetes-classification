# Diabetes Risk Detector

## About Dataset

### Context
This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. The objective is to predict, based on diagnostic measurements, whether a patient has diabetes.

#### Dataset Features

| Feature | Description | Unit/Range |
|---------|-------------|------------|
| **Pregnancies** | Number of times pregnant | Count |
| **Glucose** | Plasma glucose concentration at 2 hours in an oral glucose tolerance test | mg/dL |
| **BloodPressure** | Diastolic blood pressure | mm Hg |
| **SkinThickness** | Triceps skin fold thickness | mm |
| **Insulin** | 2-Hour serum insulin | mu U/ml |
| **BMI** | Body mass index | kg/m² |
| **DiabetesPedigreeFunction** | Diabetes pedigree function | Score |
| **Age** | Age | Years |
| **Outcome** | Class variable (0=No diabetes, 1=Has diabetes) | 0 or 1 |

### Dataset Statistics
- **Number of Instances**: 2768
- **Number of Attributes**: 8 plus class
- **Missing Attribute Values**: Yes
- **Class Distribution**: Class value 1 is interpreted as "tested positive for diabetes"

### Objective

The primary objective of this project is to develop a machine learning classification model that can accurately predict whether a patient has diabetes based on their diagnostic measurements. Using the Pima Indians Diabetes Database, we aim to:

- Build and train classification algorithms to identify diabetes risk
- Evaluate model performance using appropriate metrics (accuracy, precision, recall, F1-score)
- Compare different machine learning approaches to determine the most effective method
- Provide insights into which diagnostic features are most predictive of diabetes
- Create a reliable tool that could assist healthcare professionals in early diabetes detection

## Getting Started
---
### Prerequisites
To set up this project and install all the required dependencies, use the following steps.

1. **Clone the repository**:
    ```bash
    git clone https://github.com/wmujawar/Diabetes-classification.git
    cd Diabetes-classification
    ```

2. **Setup uv package manager:**
    
    Follow the [instruction](https://docs.astral.sh/uv/getting-started/installation/) to setup uv package manager

3. **Install the dependencies:**

    ```bash
    uv venv -p python3.12
    ```

4. **Create a virtual environment**
    ```bash
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

5. **Install dependencies:**
    ```bash
    uv sync
    ```

6. **Testing:**
    ```bash
    pytest
    ```

7. **Run Flask App:**

    To start flask api, run

    ```bash
    python src/app.py
    ```

## Docker Setup: Build and run docker container

To containerize the application and ensure it runs in any environment, you can use Docker. Below are the steps to build a Docker image and run a container.

### 1. **Build the Docker Image**

In the terminal, navigate to the directory containing the `Dockerfile` and run the following command to build the Docker image:

```bash
docker build -t diabetes-risk-predictor .
```
This command tells Docker to build an image with the tag `diabetes-risk-predictor` using the current directory (denoted by `.`) as the context.

### 2. **Run the Docker Container**

After the image is built, run the container:

```bash
docker run --name diabetes-predictor -d -p 5000:5000 diabetes-risk-predictor
```

This command starts a Docker container based on the `diabetes-risk-predictor` image and maps port 5000 of the container to port 5000 on your local machine. The Flask API will be accessible at `http://localhost:5000`.

