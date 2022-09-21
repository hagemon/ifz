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

### Configure
Edit `config.yaml`, like:

```yaml
targets:
  iPhone 14:
    - hagemon.TimeTo
    - hagemon.Nested
  iPhone 14 Pro:
    - hagemon.TimeTo
    - hagemon.Nested
```

We support multiple devices and apps running simultaneously, **note that
you should compile apps on corresponding simulator first.** 

### Fuzzing

Implement fuzzing method by derive `Fuzzing` class, or just using `RandomFuzzing`:

 ```python
 class RandomFuzzing(Fuzzing):
 @action_decorator
 def action(self, app: App):
     executable = app.executable_widgets
     index = random.randint(0, len(executable))
     w = executable[index]
     tap(w.center.x, w.center.y, app.udid)
 ```
`action_decorator` helps you to refresh GUI layout status after taking an action, or you can drop it and handle yourself. 

### Run

Alter and run `main.py` to fit your requirements.

## Components

### main.py

The entrance of this tool, responsible for booting device and apps under test, and performing random events on execucable widgets.

### config.yaml

Specify the device and bundles (apps) for the tool, only installed simulators can be used for now.

Available devices would be listed if wrong or empty devices are specified.

### executor.py

A wrapper for executing `idb` commands to perform core functions such as listing available devices and apps, booting devices, launching apps, fetching UI layouts and simulating touch events.

Executor is utilized in a singleton manner. Just `from executor import executor` to use these APIs.

### device.py

A wrapper of device, persists basic information about device and functions for booting, launching app, fetch GUI status.

### app.py

A wrapper of app, consists of widgets hierarchy on the current screen.

### parser.py

A wrapper for parsing raw text from `idb` commands to a structural manner, including devices list, widget layout and so on.
Rather than using `idb ui decrible-all` command shown in official document, we discovered an option `--nested` in [source
code](https://github.com/facebook/idb/blob/3cc2e69f281ada4ad209b31fbd350ba7d782e8f5/idb/cli/commands/accessibility.py) 
of `idb` and get the nested format of GUI layouts.

Note that GUI elements provided by `idb` is not completed, this may due to its inconsistent to `Accessibility Inspector`
tool in recent versions, causing some group view or its content (e.g. TabView) missing.

For TabView, which only provide `group` widget without content, we adopted a workaround solution that analysing
`group` widget's information and apply `idb ui describe-point x y` to get detailed content.

We built view hierarchy in a tree formulation as following:

```
|TimeTo Application (non-executable)
     |---Add Item Button (executable)
     |---Cycle Heading (non-executable)
     |---None Group (non-executable)
          |------IN A WEEK Heading (non-executable)
          |------Clear Night Image (executable)
          |------Eh..🤔 StaticText (executable)
          |------arrow.forward Image (executable)
          |------Done StaticText (executable)
          |------Clear Night Image (executable)
          |------Eh..🤔 StaticText (executable)
          |------arrow.forward Image (executable)
          |------Done StaticText (executable)
     |---Tab Bar Group (non-executable)
          |------Cycle RadioButton (executable)
          |------Schedule RadioButton (executable)
          |------Settings RadioButton (executable)
```

More scenarios are discovering for building view hierarchy, issues are welcomed.

### Fuzzing.py

Implementation of fuzzing criteria, base on the abstract `Fuzzing` class.

## TBD

- Refine the completeness of view hierarchy.
- More actions supported.