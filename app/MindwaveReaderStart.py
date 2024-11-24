# MindwaveReaderStart.py
# @author: Esteban Martinez
# @github: EstebanMz

# This module reads data from the Mindwave Mobile EEG headset and stores it
# as a CSV file inside "output_files" folder. The length of the output files
# depends on the argument of the function writeDataPoints(), which is called
# in the Main Execution block by reading testQueueArray, written at the start.
#
# Duration of tests is tied by the fact that the MindWave Mobile records a packet
# of data at a pace of once per second. That means if you set SHORT_TEST_LENGTH 
# to 120, any test with that input value will last 120 seconds, or 2 minutes.
# 
# The data saved from the sensor is:
# - Time of DataPoint reading
# - EEG Power Bands (Delta, Theta, Low Alpha, High Alpha, Low Beta, High Beta,
#   Low Gamma, Mid Gamma)
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
# - test[2]: Length of the test, determined by one of the selected values above.
testsQueueArray = [
    [f'Prueba corta para Imaginación motora del pie Derecho.', False, SHORT_TEST_LENGTH],
    [f'Prueba corta para Imaginación motora del pie Izquierdo.', False, SHORT_TEST_LENGTH],
    [f'Descanso corto.', True, SHORT_TEST_LENGTH],
    [f'Prueba larga para Imaginación motora del pie Derecho.', False, LONG_TEST_LENGTH],
    [f'Prueba larga para Imaginación motora del pie Izquierdo.', False, LONG_TEST_LENGTH],
    [f'Descanso largo.', True, LONG_TEST_LENGTH]
    # [f'Prueba reposo.', True, 60],                  # Debugging
    # [f'Prueba imaginación.', False, 30]             # Debugging
]



# Prints the following info when getDataPoints() is running:
# - A block of text every 5 seconds that tells the volunteer to think in the
#   correspondent imaginary movement. It takes in mind to not send this
#   visual signal when it's a resting test.
# - A notification when there are 15 seconds left for a running test.
def printTestInfo(arrayLength, isResting, readingTime):

    if arrayLength % 5 == 0 and isResting == False:
        print('\n'*10 + 'X'*50 + '\n' + 'X'*50 + '\n' + 'X'*50)
    elif (arrayLength - 1) % 5 == 0 and isResting == False:
        print('')
    elif (arrayLength + 1) % 15 == 0 and isResting == True:
        print('')

    if arrayLength == (readingTime - 15) and isResting == False:
        print('\n'*10 + 'X'*50 + '\n' + 'X'*50)
        print('Esta prueba finaliza en 15 segundos.\n')
    elif arrayLength == (readingTime - 15) and isResting == True:
        print('\n'*2 + 'X'*50 + '\n' + 'X'*50)
        print('Esta prueba finaliza en 15 segundos.\n')



# Returns an array with the data read from the sensor. Its size depends on 
# the value of the readingTime argument.
# The other argument, isResting, defines the type of test running and will have 
# a different behavior while printing text to the console.
def getDataPoints(isResting, readingTime):

    # Initializes the variables of all DataPoint instances.
    rawValue = attention = meditation = amountOfNoise = blink = None
    delta = theta = lowAlpha = highAlpha = lowBeta = highBeta = lowGamma = midGamma = None

    # Creates the array that will store the sensor readings.
    eegPower = "delta,theta,low_alpha,high_alpha,low_beta,high_beta,low_gamma,mid_gamma"
    dataHeader = f"date_time,{eegPower},raw_value,attention,meditation,blink,amount_of_noise"
    dataPointsArray = [dataHeader]

    # DataPoint reading loop.
    while(len(dataPointsArray) <= readingTime):

        # DataPoint is the class that reads the next data point from the headset.
        dataPoint = mindwaveDataPointReader.readNextDataPoint()

        # Checks if the read data point belongs to one of the specified 
        # instances in the DataPoint class. If it's true, the function continues
        # to extract and store its value for that DataPoint instance.
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

            # In this last instance, all the DataPoints are arranged 
            # to be stored in dataPointsArray.
            elif isinstance(dataPoint, EEGPowersDataPoint):

                # Creates dateTime variable with the current date and time.
                now = datetime.datetime.now()
                dateTime = now.strftime("%Y-%m-%d %H:%M:%S")

                # Defines the variables for the data points corresponding to
                # the group of EEG Powers.
                delta, theta = dataPoint.delta, dataPoint.theta
                lowAlpha, highAlpha = dataPoint.lowAlpha, dataPoint.highAlpha
                lowBeta, highBeta = dataPoint.lowBeta, dataPoint.highBeta
                lowGamma, midGamma = dataPoint.lowGamma, dataPoint.midGamma

                # Saves a row with all the data values read in the instances.
                dataRow = f"{dateTime},{delta},{theta},{lowAlpha},{highAlpha},"\
                    f"{lowBeta},{highBeta},{lowGamma},{midGamma},"\
                    f"{rawValue},{attention},{meditation},{blink},{amountOfNoise}"

                # Adds the data from the sensor as a new row to the array.
                # print(dataRow)                    # Debugging
                dataPointsArray.append(dataRow)

                # Calls printTestInfo() function.
                printTestInfo(len(dataPointsArray), isResting, readingTime)

    # Returns the data array containing all readings from a test.
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

    # Clears console at the start.
    os.system('clear')

    # Initializes DataPoint Reader and attempts to establish a connection 
    # with the MindWave device.
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()

    # If MindWave is connected, it will first read the testsQueueArray and
    # execute the tests defined in it using the writeDataPoints function.
    # After finishing all the queued tests, it will ask the user to enter 
    # their personal data (first name, last name, age and gender).
    if (mindwaveDataPointReader.isConnected()):

        # Loop that runs the different test defined at testQueueArray.
        for test in testsQueueArray:
            print('\n'*2 + '='*100 + '\n' + '='*100 + '\n')
            print(f"\t{test[0]} Duración: {round(test[2]/60)} minutos.")
            print('\n' + '='*100 + '\n' + '='*100 + '\n'*2)
            writeDataPoints(test[1], test[2])

        # Write the user info before finishing the connection with the MindWave.
        userData = writeData([])
        userData.writePersonalData()

    # Error message when device is not connected or couldn't be found.
    else:
        print(
            "\nError de conexión: No se pudo conectar con el dispositivo MindWave Mobile. "\
            "Reinicia la diadema y ejecuta de nuevo el código."
            )
