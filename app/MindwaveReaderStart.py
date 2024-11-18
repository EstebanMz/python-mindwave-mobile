# MindwaveReaderStart.py
# @author: Esteban Martinez
# @github: EstebanMz

# This module reads data from the Mindwave Mobile EEG headset and stores it 
# as a CSV file inside "output_files" folder. The length of the output files 
# depends on the argument of function writeDataPoints() that is called 
# in the Main Execution block as many times as it's needed.

# The data saved from the sensor is: 
# - EEG Power Bands (Delta, Theta, Low Alpha, High Alpha, 
#   Low Beta, High Beta, Low Gamma, Mid Gamma)
# - Raw Data
# - Meditation
# - Attention
# - Blink (Only displays "None")
# - Amount of Noise (also known as Poor Signal Level)

import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint, PoorSignalLevelDataPoint, AttentionDataPoint, MeditationDataPoint, BlinkDataPoint, EEGPowersDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
from MindwaveWriteData import writeData
from playsound import playsound
import threading
import time
import os

# Length (rows) for output CSV files.
SHORT_OUTPUT_LENGTH = 120
LONG_OUTPUT_LENGTH = 240



# Plays a beep of 0.5 seconds
def playBeep():
    while True:
        playsound("app/beep.wav")
        time.sleep(5)



# Returns an array with the data read from the sensor.
# Its size depends on the value of its input argument.
def getDataPoints(readingTime):

    # Initialize all variables
    rawValue = attention = meditation = amountOfNoise = blink = None
    delta = theta = lowAlpha = highAlpha = lowBeta = highBeta = lowGamma = midGamma = None

    # Initialize the array that stores the sensor readings
    eegPower = "delta,theta,low_alpha,high_alpha,low_beta,high_beta,low_gamma,mid_gamma"
    dataHeader = f"{eegPower},raw_value,attention,meditation,blink,amount_of_noise"
    dataPointsArray = [dataHeader]

    input("Press Enter key to continue...")
    print(f"Data reading is starting now for {readingTime/60} minutes!")

    # Sound thread
    soundThread = threading.Thread(target = playBeep)
    soundThread.daemon = True
    soundThread.start()
    
    # Program will end after "data" array reaches "readingTime" size
    while(len(dataPointsArray) <= readingTime):

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
                dataRow = f"{delta},{theta},{lowAlpha},{highAlpha},"\
                    f"{lowBeta},{highBeta},{lowGamma},{midGamma},"\
                    f"{rawValue},{attention},{meditation},{blink},{amountOfNoise}"
                
                # Adds sensor data as a new row
                dataPointsArray.append(dataRow)
    
    # Returns the array with all the readings
    return dataPointsArray



# Inputs the DataPoints array and outputs the CSV file.
def writeDataPoints(readingTime):

    # Executes getDataPoints() function and stores the return result in data
    data = getDataPoints(readingTime)

    # Create an instance of writeData() class
    exportData = writeData(data)

    # Call the method to write data to CSV
    exportData.writeFile()



# Main Execution block.
if __name__ == '__main__':

    # Clears console
    os.system('clear')

    # Initializes the MindwaveDataPointReader, starts the connection,
    # and continuously reads and prints data points.
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    
    # Calls writeDataPoints() function, which writes the CSV file,
    # inside this if as many times as its needed.
    if (mindwaveDataPointReader.isConnected()):

        print("\nMotor imagination for left foot, short test.")
        writeDataPoints(SHORT_OUTPUT_LENGTH)

        print("\nMotor imagination for right foot, short test.")
        writeDataPoints(SHORT_OUTPUT_LENGTH)

        print("\nResting, short test.")
        writeDataPoints(SHORT_OUTPUT_LENGTH)

        print("\nMotor imagination for left foot, long test.")
        writeDataPoints(LONG_OUTPUT_LENGTH)

        print("\nMotor imagination for right foot, long test.")
        writeDataPoints(LONG_OUTPUT_LENGTH)

        print("\nResting, long test.")
        writeDataPoints(LONG_OUTPUT_LENGTH)
        
    # Error message when device is not connected or couldn't be found.
    else:
        print(
            "Exiting because the program could not connect "\
            "to the MindWave Mobile device."
            )
