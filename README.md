# Instructions for MindWave:
### Read throughtly the whole documentation below:
**(Updated to November 2024, Esteban Martínez)**

**Device target:** Raspberry Pi 4B

---

Clone this repository
```
git clone https://github.com/EstebanMz/python-mindwave-mobile.git
```

Go to folder project
```
cd python-mindwave-mobile
```

Install the following libraries and modules
```
sudo apt-get install libbluetooth-dev python-dev-is-python3 libglib2.0-dev libboost-python-dev libboost-thread-dev libglib2.0-dev pkg-config
```
```
sudo apt install python3-gattlib
```

## Create a Python Virtual Environment

### *Mandatory to install Pybluez's Bluetooth package.*

Other packages will be installed inside the virtual environment as well.
```
python -m venv .venv
```

### Activate virtual environment

If correct, `(.venv)` should show up at the start of the command line.
***You may need to follow this step every time you open a terminal window if you use the alternative launch option.***
```
source .venv/bin/activate
```

### Install PyBluez inside the environment.

PyBluez is a Bluetooth package for Linux and compatible with Raspberry OS. More info [about PyBluez](https://github.com/pybluez/pybluez).
```
pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
```

### Install the following Python packages.

Include the original `python-mindwave-mobile` package and Pandas.
```
pip install git+https://github.com/robintibor/python-mindwave-mobile.git

```
```
pip install pandas
```

---

## Launch Command
### *Before run, turn off and on the MindWave Mobile 2 just before for pairing purposes.*
```
.venv/bin/python MindwaveReaderStart.py
```

Alternative option if you don't need to stay inside the virtual environment.
```
python app/MindwaveReaderStart.py
```

### Exit virtual environment
```
deactivate
```

---

Afterwards, you can use it within Python like this, with the headset set in pairing mode (http://support.neurosky.com/kb/mindwave-mobile/how-do-i-put-the-mindwave-mobile-into-discovery-mode):

```python
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
mindwaveDataPointReader = MindwaveDataPointReader()
# connect to the mindwave mobile headset...
mindwaveDataPointReader.start()
# read one data point, data point types are specified in  MindwaveDataPoints.py'
dataPoint = mindwaveDataPointReader.readNextDataPoint()
print(dataPoint)
```
