This project is a web dashboard for analyzing and predicting the performance of automation machines using Excel data. It provides interactive visualizations and a Linear Regression model to predict Productivity Gain based on key parameters.

🚀 Features

Month-wise Filtering – View performance metrics for a selected month.

Interactive Charts:

Robots Adopted (Bar Chart)

Cost Savings (Pie Chart)

Jobs Displaced (Bar Chart with values)

Training Hours (Box Plot)

Productivity Gain Prediction – Predicts future productivity using machine learning.

Excel Data Integration – Reads data from an .xlsx file.

📂 Usage

Place your dataset in the project folder (update the file path in the script).

Install dependencies:

pip install flask dash pandas scikit-learn plotly openpyxl


Run the app:

python app.py


Open in browser: http://127.0.0.1:8050
