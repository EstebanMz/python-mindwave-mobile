# app.py
# @author: Esteban Martinez
# @github: EstebanMz

# This module reads data from the Mindwave Mobile EEG headset 
# and stores it as a CSV file inside "output_files" folder.
# The length of the output files depends on "OUTPUT_LENGTH" value
# at the beginning of the code (line 25).
# The data saved from the sensor is: 
# - EEG Power Bands (Delta, Theta, Low Alpha, High Alpha, Low Beta, High Beta, Low Gamma, Mid Gamma)
# - Raw Data
# - Meditation
# - Attention
# - Blink (Only displays "None")
# - Amount of Noise (also known as Poor Signal Level)

import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint, PoorSignalLevelDataPoint, AttentionDataPoint, MeditationDataPoint, BlinkDataPoint, EEGPowersDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
from MindwaveWriteData import writeData
import os

# Length (rows) for output CSV files.
OUTPUT_LENGTH = 50

# Main execution block.
# Initializes the MindwaveDataPointReader, starts the connection,
# and continuously reads and prints data points.
if __name__ == '__main__':

    # Clear console
    os.system('clear')

    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()

    if (mindwaveDataPointReader.isConnected()):
        # Initialize all variables
        rawValue = attention = meditation = amountOfNoise = blink = None
        delta = theta = lowAlpha = highAlpha = lowBeta = highBeta = lowGamma = midGamma = None

        # eeg_power = [Delta,Theta,LowAlpha,HighAlpha,LowBeta,HighBeta,LowGamma,MidGamma]
        dataHeader = "eeg_power;raw_value;attention;meditation;blink;amount_of_noise"
        data = [dataHeader]

        print("Data reading is starting now!")

        # Program will end after "data" array reaches OUTPUT_LENGTH size
        while(len(data) <= OUTPUT_LENGTH):

            # DataPoint is the class that reads the next data point from the headset.
            dataPoint = mindwaveDataPointReader.readNextDataPoint()

            # Checks if the dataPoint object belongs to one of the specified
            # data point classes. If the dataPoint is an instance of one 
            # of these classes, the code then proceeds to extract 
            # the specific data value from that data point object.
            if isinstance(dataPoint, (PoorSignalLevelDataPoint, AttentionDataPoint, 
                                      MeditationDataPoint, BlinkDataPoint, 
                                      RawDataPoint, EEGPowersDataPoint)):
                
                if isinstance(dataPoint, PoorSignalLevelDataPoint):
                    amountOfNoise = dataPoint.amountOfNoise

                elif isinstance(dataPoint, AttentionDataPoint):
                    attention = dataPoint.attentionValue

                elif isinstance(dataPoint, MeditationDataPoint):
                    meditation = dataPoint.meditationValue

                elif isinstance(dataPoint, BlinkDataPoint):
                    blink = dataPoint.blinkValue

                elif isinstance(dataPoint, RawDataPoint):
                    rawValue = dataPoint.rawValue

                elif isinstance(dataPoint, EEGPowersDataPoint):
                    delta, theta = dataPoint.delta, dataPoint.theta 
                    lowAlpha, highAlpha = dataPoint.lowAlpha, dataPoint.highAlpha
                    lowBeta, highBeta = dataPoint.lowBeta, dataPoint.highBeta
                    lowGamma, midGamma = dataPoint.lowGamma, dataPoint.midGamma
                    
                    # Stores a row of data values
                    dataRow = f"[{delta},{theta},{lowAlpha},{highAlpha},"\
                        f"{lowBeta},{highBeta},{lowGamma},{midGamma}];"\
                        f"{rawValue};{attention};{meditation};{blink};{amountOfNoise}"
                    data.append(dataRow)

        # Create an instance of the class
        exportData = writeData(data)

        # Call the method to write data to CSV
        exportData.writeFile()
        
    
    # Error message when device is not connected or couldn't be found.
    else:
        print(
            "Exiting because the program could not connect "\
            "to the MindWave Mobile device."
            )
