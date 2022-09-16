## Introduction

A Python wrapper of [idb](https://fbidb.io) for fuzzing testing on iOS apps in simulators.

This project is still very young, more supports are on the way.

## Pre-requirements

### Homebrew

```commandline
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

More info on [Homebrew Homepage](https://brew.sh).

### XCode Command Line Tools

If you install XCode from App Store or download from official developer website, this would have been installed,
or you can run

```commandline
xcode-select --install
```

### idb

idb is made up of 2 parts, each of which needs to be installed separately.

#### idb companion

```commandline
brew tap facebook/fb
brew install idb-companion
```

#### idb client

Use your own version of pip here.
```commandline
pip install fb-idb  
```

More info on [idb document](https://fbidb.io/docs/installation).

## Usage

1. Edit config.yaml.
1. Alter `main.py` or directly run it to perform 10 random tap for app under test.

A demo of `config.yaml`:

```yaml
device: iPhone 13
bundles:
  - hagemon.Sunset  # Bundle ID of app under test.
```

## Components

### config.yaml

Specify the device and bundles(apps) for the tool, only installed simulators in the following list can be used for now.

```python
class DeviceType(Enum):
    PHONE_11 = 'iPhone 11'
    PHONE_11_P = 'iPhone 11 Pro'
    PHONE_11_PM = 'iPhone 11 Pro Max'
    PHONE_12 = 'iPhone 12'
    PHONE_12_P = 'iPhone 12 Pro'
    PHONE_12_PM = 'iPhone 12 Pro Max'
    PHONE_12_MI = 'iPhone 12 mini'
    PHONE_13 = 'iPhone 13'
    PHONE_13_P = 'iPhone 13 Pro'
    PHONE_13_PM = 'iPhone 13 Pro Max'
    PHONE_13_MI = 'iPhone 13 mini'
    PHONE_14 = 'iPhone 14'
    PHONE_14_P = 'iPhone 14 Pro'
    PHONE_14_PM = 'iPhone 14 Pro Max'
    PHONE_SE = 'iPhone SE (2nd generation)'
    PHONE_8 = 'iPhone 8'
    PHONE_8_P = 'iPhone 8 Plus'
```

More devices and automatic installation will be supported recently.

### executor.py

A wrapper for executing `idb` commands to perform core functions such as listing avaliable devices and apps, booting devices, launching apps, fetching UI layouts and simulating touch events.

Executor is utilized in a singleton manner. Just `from executor import executor` to use thses APIs.

### main.py

The entrance of this tool, responsible for booting device and apps under test, and performing random events on  exeucable widgets.

### device.py

A wrapper of device, consists of enumerations of device types and status. The `Device` class persists basic information about device and functions for booting, launching app, fetch UI status and trigger random events.

Fetching UI and trigger events would call some functions of currently activated application, more details in `app.py`.

### app.py

A wrapper of app, consists of widgets on the current screen. Executable widgets are also marked for performing random events.

### parser.py

A wrapper for parsing raw text from `idb` commands to a structural manner, including devices list, widget layout and so on.