import pandas as pd
csvFile = './data/skills/job_skills.csv'
dataframe = pd.read_csv(csvFile, sep=',')
outputFile = './data/skills/job_skills.json'

dataframe.to_json(outputFile, orient='records', lines=True)
print("CSV to JSON conversion completed.")