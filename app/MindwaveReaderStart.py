# MindwaveReaderStart.py
# @author: Esteban Martinez
# @github: EstebanMz

# This module reads data from the Mindwave Mobile EEG headset and stores it 
# as a CSV file inside "output_files" folder. The length of the output files 
# depends on the argument of the function writeDataPoints(), which is called 
# in the Main Execution block by reading testQueueArray, written at the start. 
# 
# Duration of tests is tied by the fact that the MindWave Mobile records a packet of 
# data at a pace of once per second. That means if you set SHORT_TEST_LENGTH to 120, 
# any test with that input value will last 120 seconds, or 2 minutes.

# The data saved from the sensor is: 
# - Time of DataPoint reading
# - EEG Power Bands (Delta, Theta, Low Alpha, High Alpha, 
#   Low Beta, High Beta, Low Gamma, Mid Gamma)
# - Raw Data
# - Meditation
# - Attention
# - Blink (Only displays "None")
# - Amount of Noise (also known as Poor Signal Level)

import bluetooth
import datetime
from mindwavemobile.MindwaveDataPoints import RawDataPoint, PoorSignalLevelDataPoint, AttentionDataPoint, MeditationDataPoint, BlinkDataPoint, EEGPowersDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
from MindwaveWriteData import writeData
import os

# Length (rows) for output CSV files.
SHORT_TEST_LENGTH = 120
LONG_TEST_LENGTH = 240

# Defines an array with the tests that will be held in the moment
# the MindWave is connected to this device.
# - test[0]: Name or description of the event.
# - test[1]: Is a resting test? (read printTestInfo() for context).
# - test[2]: Length of the test, determined by one of the 
#            selected values above.
testsQueueArray = [
    [f'Prueba corta para Imaginación motora del pie Derecho.', False, SHORT_TEST_LENGTH],
    [f'Prueba corta para Imaginación motora del pie Izquierdo.', False, SHORT_TEST_LENGTH],
    [f'Descanso corto.', True, SHORT_TEST_LENGTH],
    [f'Prueba larga para Imaginación motora del pie Derecho.', False, LONG_TEST_LENGTH],
    [f'Prueba larga para Imaginación motora del pie Izquierdo.', False, LONG_TEST_LENGTH],
    [f'Descanso largo.', True, LONG_TEST_LENGTH]
]



# Prints the following info when getDataPoints() is running:
# - A block of text every 5 seconds that tells the volunteer
#   to think in the correspondent imaginary movement. It takes
#   in mind to not send this visual signal when it's a resting test.
# - A notification when there are 5 seconds left for a running test.
def printTestInfo(arrayLength, isResting, readingTime):

    if arrayLength % 5 == 0 and isResting == False:
        print('\n'*10 + 'X'*50 + '\n' + 'X'*50 + '\n' + 'X'*50)
    elif (arrayLength - 1) % 5 == 0 and isResting == False:
        print('')

    if arrayLength == (readingTime - 5):
        print('\n'*9 + 'X'*50 + '\n' + 'X'*50)
        print('La siguiente prueba inicia en 5 segundos.\n')



# Returns an array with the data read from the sensor.
# Its size depends on the value of its input argument.
def getDataPoints(isResting, readingTime):

    # Initialize all variables
    rawValue = attention = meditation = amountOfNoise = blink = None
    delta = theta = lowAlpha = highAlpha = lowBeta = highBeta = lowGamma = midGamma = None

    # Initialize the array that stores the sensor readings
    eegPower = "delta,theta,low_alpha,high_alpha,low_beta,high_beta,low_gamma,mid_gamma"
    dataHeader = f"time_now,{eegPower},raw_value,attention,meditation,blink,amount_of_noise"
    dataPointsArray = [dataHeader]

    # Reading Data loop
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
                # Generate time_now with hour, minutes and seconds
                now = datetime.datetime.now()
                time_now = now.strftime("%H:%M:%S")
                delta, theta = dataPoint.delta, dataPoint.theta 
                lowAlpha, highAlpha = dataPoint.lowAlpha, dataPoint.highAlpha
                lowBeta, highBeta = dataPoint.lowBeta, dataPoint.highBeta
                lowGamma, midGamma = dataPoint.lowGamma, dataPoint.midGamma
                
                # Stores a row of data values
                dataRow = f"{time_now},{delta},{theta},{lowAlpha},{highAlpha},"\
                    f"{lowBeta},{highBeta},{lowGamma},{midGamma},"\
                    f"{rawValue},{attention},{meditation},{blink},{amountOfNoise}"
                
                # Adds sensor data as a new row
                # print(dataRow)                    # Debugging
                dataPointsArray.append(dataRow)

                # Calls printTestInfo() function
                printTestInfo(len(dataPointsArray), isResting, readingTime)
    
    # Returns the array with all the readings
    return dataPointsArray



# Inputs the DataPoints array and outputs the CSV file.
def writeDataPoints(isResting, readingTime):
            
    # Executes getDataPoints() function and stores the return result in data
    data = getDataPoints(isResting, readingTime)

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

        # Loop that runs the different test defined at testQueueArray.
        for test in testsQueueArray:
            print(f"\n{test[0]} Duración: {round(test[2]/60, 1)} minutos.")
            writeDataPoints(test[1], test[2])

        # Write the user info before finishing the connection with the MindWave.
        userData = writeData([])
        userData.writePersonalData()
        
    # Error message when device is not connected or couldn't be found.
    else:
        print(
            "Exiting because the program could not connect "\
            "to the MindWave Mobile device."
            )
