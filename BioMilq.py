# Abrar Mahi

import pandas as pd
import matplotlib.pyplot as plt

# function that parses data
def parse(sheetname):
    # reading sheet 1
    df = pd.read_excel('data.xlsx', sheet_name=sheetname)

    # removing all rows with null Avg Glucose values and putting it into new data frame (data cleanup)
    df1 = df.dropna(subset=["Avg. Glucose (mg/dL)"])
    df1['Avg. Glucose (mg/dL)'] = df1['Avg. Glucose (mg/dL)'].round()

    # tracking how much glucose has been consumed in each period/ the rate of change
    df1['Rate'] = df1['Avg. Glucose (mg/dL)'].diff()

    #print(df1['Glucose Utilization Rate'])

    # finding the difference in days from each day of glucose monitoring
    df1['new'] = df1['Days of Culture'].diff()

    # creating a new column which trackes the daily loss in glucose
    df1['Daily change in Glucose (mg/dL)'] = df1['Rate'] / df1['new']

    #print(df1['Daily change in Glucose (mg/dL)'])

    # iteratting through df1
    for i in df1.index:
       
        # if the value is non negative(the day the glucose was reidministered): then delete the cell (data cleanup)
        if (df1['Daily change in Glucose (mg/dL)'][i] > 0):
            del df1['Daily change in Glucose (mg/dL)'][i]
            del df1['Days of Culture'][i]

    print("Daily change in Glucose (mg/dL)",
          df1['Daily change in Glucose (mg/dL)'])

    # iteratting through df1
    for index, row in df1.iterrows():
        # condition for lactating (rate of change is -22 during the remaining 75 days)
        if(row['Daily change in Glucose (mg/dL)'] <= -22 and index >= 25):
            print("Bioreactor status at day ", index, ": lactating")
        
        # condition for steady state (rate of change is -13 for atleast 3 days)
        elif(-13 >= row['Daily change in Glucose (mg/dL)'] > -22 and index < 25):
            print("Bioreactor status at day ", index, ": steady state")
        
        # condition for proliferation stage
        elif(row['Daily change in Glucose (mg/dL)'] > -13 and index <= 15):
            print("Bioreactor status at day ", index, ": proliferative phase")

    # creating a graph that displays the Daily change in Glucose (mg/dL) in glucose and displaying it
    df1.plot(kind="bar", x="Days of Culture",
             y='Daily change in Glucose (mg/dL)')
    plt.show()


if __name__ == "__main__":
    val = input("enter the sheet (A, B, C): ")
    parse(val)
