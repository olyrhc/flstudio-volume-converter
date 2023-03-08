# flstudio-volume-converter
A Python module for FL Studios MIDI-scripting API that make volume conversions between float and dB

### Purpose

You can set the volume in the mixer in your scripts with FL Studio's MIDI-scripting API with **setTrackVolume()**. This command accepts a float value between 0 and 1 as input. So how do you set the volume to say -4.5 dB?  Well, you'd need to convert it from dB to float first. Something like float_value = pow(10.0, -4.5/20), right?  

**No**. The reason is that FL Studio uses a non-linear volume scale.

In my attempt to solve this, I made a map of the dB values and wrote some code that fetches the nearest values from a lookup-table. It's not perfect but it gets the job done with only a 0.1 dB margin of error for most of the volume range! That is, unless you try to convert ridiculously low dB-values below -70dB, where the error-rate will increase really fast. The reason for this is that the volume scale in FL Studio loses a lot of its resolution near the bottom end, i.e. it's not possible to set any exact values when the values approach near silence (who would need that anyway?). Nevertheless, I have mapped all the nearest values that **setTrackVolume()** can set all the way to the bottom, so in that regard, the conversions are as perfect as they can be made.

### Installation & Usage
