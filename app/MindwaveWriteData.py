# MindwaveWriteData.py
# @author: Esteban Martinez
# @github: EstebanMz

import datetime
import os
import pandas as pd

class writeData:
    def __init__(self, data_array):
        self.data_array = data_array



    # Converts an array into a CSV file which gets stored as "filename" value.
    def writeFile(self):
        # Generate filename with date and time
        now = datetime.datetime.now()
        test_filename = now.strftime("output_files/%Y-%m-%d %H_%M_%S-MindwaveData.csv")
        
        # Create a DataFrame from the data
        df = pd.DataFrame([x.split(',') for x in self.data_array])

        # Save the DataFrame to a CSV file
        df.to_csv(test_filename, index=False, header=False)

        print(f"Data saved to {test_filename}")



    # Writes personal data to history.csv.
    def writePersonalData(self):
        # Generate filename for history file.
        history_filename = "output_files/history.csv"
        # last_name: The last name of the person.
        # first_name: The first name of the person.
        # age: The age of the person.
        # gender: The gender of the person (F or M)
        print('\n\n\nCOMPLETE LA SIGUIENTE INFORMACIÓN PARA TERMINAR EL EXAMEN')
        first_name = input("Ingrese su nombre: ")
        last_name = input("Ingrese su apellido: ")
        age = input("Ingrese su edad: ")
        gender = input("Ingrese su genero (F/M): ")

        # Gets current time.
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Defines a dictionary with user data.
        new_data = {
            "register_date": timestamp,
            "last_name": last_name,
            "first_name": first_name,
            "age": age,
            "gender": gender
        }

        # Checks if history file doesn't exist, then creates a new file.
        if not os.path.exists(history_filename):
            df = pd.DataFrame([new_data])

        # If history.csv is found, registers the personal data by 
        # concatenating the input data with the read version.
        else:
            df = pd.read_csv(history_filename)
            new_df = pd.DataFrame([new_data])
            df = pd.concat([df, new_df], ignore_index=True)

        # Saves history.csv
        df.to_csv(history_filename, index=False)
        print(f"Personal data saved to {history_filename}")
        