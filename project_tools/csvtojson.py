import pandas as pd
csvFile = './data/UpdatedResumeDataSet.csv'
dataframe = pd.read_csv(csvFile, sep=',')
outputFile = './data/BasicDataset.json'

dataframe.to_json(outputFile, orient='records', lines=True)
print("CSV to JSON conversion completed.")