# MindwaveWriteData.py
# @author: Esteban Martinez
# @github: EstebanMz

# Converts an array into a CSV file which gets stored as "filename" value.
import pandas as pd
import datetime

class writeData:
    def __init__(self, data_array):
        self.data_array = data_array

    def writeFile(self):
        # Generate filename with date and time
        now = datetime.datetime.now()
        filename = now.strftime("output_files/%Y-%m-%d %H_%M_%S-MindwaveData.csv")
        
        # Create a DataFrame from the data
        df = pd.DataFrame([x.split(',') for x in self.data_array])

        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False, header=False)

        print(f"Data saved to {filename}")