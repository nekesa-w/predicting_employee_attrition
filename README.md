# Predicting Employee Attrition

An end-to-end machine learning pipeline for predicting employee attrition, using the IBM HR Analytics workforce dataset covering demographics, compensation, satisfaction, and tenure.

## Research Question

Which employee attributes are most associated with attrition, and can attrition be predicted from workforce data.

## Problem Statement

Employee attrition creates hiring costs, knowledge loss, and lower team stability. Understanding the drivers of attrition helps a company target retention efforts before employees leave.

## Dataset

- **Source:** IBM HR Analytics Employee Attrition dataset
- **File:** `attrition_dataset.csv`
- **Coverage:** 1470 employee records with 35 workforce attributes, including age, department, income, satisfaction scores, tenure, and attrition status.

## Methodology

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis
4. Statistical Analysis
5. Feature Engineering
6. Feature Encoding
7. Feature Scaling
8. Model Training
9. Cross Validation
10. Hyperparameter Tuning
11. Model Evaluation
12. SHAP Interpretation

### Data Cleaning
- Checked for missing values and duplicate rows, both zero
- Created title case display labels for department, job role, gender, and overtime status, kept separately from the raw values used for modeling

### Exploratory Data Analysis
- Attrition rate by department
- Attrition rate by job role
- Age distribution by attrition status

### Statistical Analysis
- **Welch's t test** comparing monthly income for employees who left versus stayed, statistic -7.483, p < 0.001
- **Chi square test** for association between overtime and attrition, statistic 87.564, p < 0.001

### Feature Engineering
- Created a binary attrition target flag
- Computed a tenure ratio, years at company relative to total working years
- Computed income per job level

### Modeling
- Categorical features one hot encoded, 47 features after encoding
- Numeric features standardized with `StandardScaler`
- Stratified train and test split, 80 percent train, 20 percent test, 1176 training rows, 294 testing rows
- Baseline model: `RandomForestClassifier`
- Five fold cross validation on the baseline model
- Hyperparameter tuning via `RandomizedSearchCV` over n_estimators, max_depth, min_samples_split, and min_samples_leaf

### Model Evaluation
| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Baseline, five fold cross validation | 0.862 (± 0.009) | — | — | — |
| Tuned, held out test set | 0.837 | 0.455 | 0.106 | 0.172 |

Randomized search selected the following hyperparameters as best on cross validation: `n_estimators=200`, `min_samples_split=2`, `min_samples_leaf=2`, `max_depth=None`. The tuned model reaches similar accuracy to the baseline but has low recall, meaning it correctly flags only a small share of employees who actually leave. This is a common effect of class imbalance, since only about 16 percent of employees in the dataset left the company, and would need to be addressed with class weighting or resampling before the model is used for real retention decisions.

### Interpretability, SHAP
SHAP was used to interpret the tuned model:
- Mean absolute SHAP value bar chart of the top twelve features

The **overtime status** feature was the most influential, followed by age, stock option level, total working years, and monthly income, indicating that workload and career stage are the strongest drivers of predicted attrition.

## Results Summary

The tuned model reaches 0.837 accuracy on a held out test set, close to the 0.862 mean accuracy from cross validation, but its recall of 0.106 means it misses most employees who actually leave. SHAP analysis identifies overtime status as the single most influential feature, followed by age and compensation related features, showing that workload and career stage patterns are the strongest drivers of predicted attrition.

## Limitations

The dataset represents a single company snapshot, so results may not generalize to other organizations. Some workforce factors such as manager quality or team culture are not captured in the data. The tuned model also has low recall for the attrition class, so it should not be used alone to make retention decisions without further tuning for class imbalance.

## Real World Uses

- Explore attrition patterns interactively using the included `dashboard.py` app
- Flag employees at higher attrition risk to prioritize retention conversations
- Guide staffing and compensation planning using department and role level patterns
- Support human resource teams in monitoring overtime load as a retention risk factor

## Usage

1. Open and run `predicting_employee_attrition.ipynb`.
2. Open and run `dashboard.py`, or view the dashboard with the link in the description.

## Project Structure

```
.
├── predicting_employee_attritiom.ipynb
├── dashboard.py
├── attrition_dataset.csv
├── requirements.txt
└── README.md
```
