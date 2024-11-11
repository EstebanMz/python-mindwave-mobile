# read_mwm.py
# @author: Esteban Martínez

# TO-DO LIST
# - Store collected data in a CSV file every time the file is run.
# - Add digital filters and plots.
# - Add a periodic visual or sound alarm and set an amount of time the MindWave will run.

# This module reads data from the Mindwave Mobile EEG headset and prints it to the console.
# It connects to the headset, reads data points, and displays the values for:
# - Meditation
# - Attention
# - Blink (Not working)
# - EEG Power Bands (Delta, Theta, Low Alpha, High Alpha, Low Beta, High Beta, Low Gamma, Mid Gamma)
# - Poor Signal Level

import time
import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint, PoorSignalLevelDataPoint, AttentionDataPoint, MeditationDataPoint, BlinkDataPoint, EEGPowersDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap

# Main execution block.

# Initializes the MindwaveDataPointReader, starts the connection,
# and continuously reads and prints data points.
if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    
    if (mindwaveDataPointReader.isConnected()):
        # Initialize all variables
        attention = meditation = blink = delta = theta = lowAlpha = highAlpha = lowBeta = highBeta = lowGamma = midGamma = amountOfNoise = None
        # Print Header
        print("Attention;Meditation;Delta;Theta;LowAlpha;HighAlpha;LowBeta;HighBeta;LowGamma;MidGamma;AmountOfNoise")
        
        # Endless read cycle
        while(True):
            # DataPoint is the class that reads the next data point from the headset.
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (not dataPoint.__class__ is RawDataPoint):
                
                # Checks if the dataPoint object belongs to one of the specified data point classes.
                # If the dataPoint is an instance of one of these classes, the code then proceeds to extract the specific data value from that data point object.
                if isinstance(dataPoint, (PoorSignalLevelDataPoint, AttentionDataPoint, MeditationDataPoint, BlinkDataPoint, EEGPowersDataPoint)):
                    
                    if isinstance(dataPoint, PoorSignalLevelDataPoint):
                        amountOfNoise = dataPoint.amountOfNoise
                    
                    elif isinstance(dataPoint, AttentionDataPoint):
                        attention = dataPoint.attentionValue
                    
                    elif isinstance(dataPoint, MeditationDataPoint):
                        meditation = dataPoint.meditationValue
                    
                    elif isinstance(dataPoint, BlinkDataPoint):
                        blink = dataPoint.blinkValue
                    
                    elif isinstance(dataPoint, EEGPowersDataPoint):
                        delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, midGamma = dataPoint.delta, dataPoint.theta, dataPoint.lowAlpha, dataPoint.highAlpha, dataPoint.lowBeta, dataPoint.highBeta, dataPoint.lowGamma, dataPoint.midGamma
                        # Prints on console all data collected in a cycle.
                        print(f"{attention};{meditation};{delta};{theta};{lowAlpha};{highAlpha};{lowBeta};{highBeta};{lowGamma};{midGamma};{amountOfNoise}")
    # Error message when device is not connected.
    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the MindWave Mobile device.""").replace("\n", " ")))
        
