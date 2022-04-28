Install the dependencies

```pip install -r requirements.txt```

uses mediapipe hands solution to get the hand coordinates and uses python packages to move the pointer.

Installing autopy on the m1 mac was difficult.

It needs to be built from source:
https://github.com/autopilot-rs/autopy

modify the src/libs.rs file:
```8+ | #![feature(specialization, const_fn_transmute)]```

modify the makefile:
```5+ |      python3 setup.py build```

```17+ |     pip3 install . ```

Type the following commands in the terminal after navigating to the autopy directory from the github clone:
```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh```
```rustup default```
```make```
```make install```

