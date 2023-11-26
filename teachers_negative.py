import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('./dataset/teacherdb.csv')

# Initialize an empty DataFrame for negative feedback
negative_feedback_df = pd.DataFrame()

# Loop through columns to check for negative sentiment scores
for col in df.columns:
    if col.endswith('score'):
        sentiment_column = col
        feedback_column = col.replace('score', '')
        negative_feedback_df = pd.concat(
            [negative_feedback_df, df[df[sentiment_column] == -1][feedback_column]],
            axis=1
        )

# Rename the columns in the new DataFrame
negative_feedback_df.columns = [f'Negative Feedback {i}' for i in range(
    1, len(negative_feedback_df.columns) + 1)]

# Specify the name of the new CSV file for negative feedback
output_csv_file = 'negative_feedback.csv'

# Write the negative feedback DataFrame to the new CSV file
negative_feedback_df.to_csv(output_csv_file, index=False)

print(f"Negative feedback has been extracted and saved to {output_csv_file}")
