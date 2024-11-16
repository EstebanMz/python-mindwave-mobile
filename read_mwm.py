# read_mwm.py
# @author: Esteban Martínez

# TO-DO LIST
# - Store collected data in a CSV file every time the file is run.
# - Add digital filters and plots.
# - Add a periodic visual or sound alarm and set an amount of time the MindWave will run.

# This module reads data from the Mindwave Mobile EEG headset and prints it 
# to the console. It connects to the headset, reads data points, 
# and displays the values for:
# - EEG Power Bands (Delta, Theta, Low Alpha, High Alpha, Low Beta, High Beta, Low Gamma, Mid Gamma)
# - Raw Data
# - Meditation
# - Attention
# - Amount of Noise (also known as Poor Signal Level)
# - Blink (Not working)

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
        rawValue = attention = meditation = amountOfNoise = blink = None
        delta = theta = lowAlpha = highAlpha = lowBeta = highBeta = lowGamma = midGamma = None
        data_header = "eeg_power;raw_value;attention;meditation;amount_of_noise"

        # Print Header
        # EEG_Power = Delta;Theta;LowAlpha;HighAlpha;LowBeta;HighBeta;LowGamma;MidGamma
        print(data_header)

        # Endless read cycle
        while(True):
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
                    
                    # Prints on console all data collected in a cycle.
                    print(
                        f"[{delta},{theta},{lowAlpha},{highAlpha},"\
                        f"{lowBeta},{highBeta},{lowGamma},{midGamma}];"\
                        f"{rawValue};{attention};{meditation};{amountOfNoise}"
                    )
    
    # Error message when device is not connected or couldn't be found.
    else:
        print((
            textwrap.dedent("""\
            Exiting because the program could not connect
            to the MindWave Mobile device.""").replace("\n", " ")
            ))
