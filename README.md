# flstudio-volume-converter
A Python module for FL Studios MIDI-scripting API that make volume conversions between dB and float

### Purpose

You can set the volume in the mixer in your scripts with FL Studio's MIDI-scripting API with **mixer.setTrackVolume**. This method accepts a float value between 0 and 1 as input. So how can you set the volume to -4.5 dB for example? Well, you'd need to convert it from dB to float first. Something like `float_value = pow(10, -4.5 / 20)`, right?  

**No**. The reason is that FL Studio uses a non-linear volume scale.

In my attempt to solve this, I made a map of the dB values and wrote some code that fetches the nearest values from a lookup-table. It gets the job done with perfect accuracy (_when converting from dB to float_) unless you try to convert ridiculously low dB-values below -70dB, where the error-rate will increase really fast. The reason for this is that the volume scale in FL Studio loses a lot of its resolution near the bottom end, i.e. it's not possible to set any exact values when the values approach near silence (who would need that anyway?). Nevertheless, I have mapped all the nearest values that **mixer.setTrackVolume** can set, all the way to the bottom. In that regard, the conversions are as perfect as they can be made.

Please note that when converting the other way around (_from float to dB_), the accuracy will suffer a bit due to the fact that the conversion uses the nearest value it can find in the lookup-table. The result will be pretty close (_within 0.1 dB_) but not as perfect as when converting from dB to float. You can circumvent this by using **mixer.getTrackVolume** and give it the optional argument to return the result in dB instead.

### Installation & Usage

Copy the file volume.py to the same folder as your own script resides in. Open your script in a text-editor and import the flstudio-volume-converter module. The import-line can be added anywhere in your script as long as it's somewhere at the beginning. I recommend putting it together with the rest of FL Studio's MIDI scripting API imports.

To import flstudio-volume-converter, add this line to your script:  
`import volume`

It gives you access to 3 methods:

|Method|Argument|Result|Documentation|
|:---|:---|:---|:---|
|db_to_fl|decibel_value|float|Converts the given decibel_value to a float value between 0 and 1.|
|fl_to_db|float_value|decibel|Converts the given float_value to a decibel value between -100 and 5.6. Note that this will return the nearest dB value which means that the result will be within a 0.1 dB margin of error, i.e. it's not perfect. If you need perfect accuracy, use **mixer.getTrackVolume(track_number, 1)** to get the volume in dB from the desired track.|
|add_db|float, decibel|float|Takes a given float value and adds or subtracts the given amount of decibels from it. A positive decibel value will be added, a negative value will be subtracted. The result will be within a 0.1 dB margin of error.|

### Examples:
(_requires that the mixer module from FL Studios MIDI scripting API has been imported._)

---
### db_to_fl
`track = 1`  
`volume_in_float = volume.db_to_fl(-4.5)`  
`mixer.setTrackVolume(track, volume_in_float)`

**Result:** Track 1 in the mixer will be set to -4.5 dB.

---
### fl_to_db
`value_in_float = mixer.getTrackVolume(1)`  
`converted_to_db = volume.fl_to_db(value_in_float)`  
`print(converted_to_db)`

**Result:** The volume of track 1 will be printed as a dB value.

---
### add_db (adding)
`value_in_float = 0.8`  
`added_volume = 0.5`  
`new_value_in_float = volume.add_db(value_in_float, added_volume)`

**Result:** new_value_in_float will still be a float value but will have 0.5 dB added to it.

---
### add_db (subtracting)
`value_in_float = 0.8`  
`subtracted_volume = -0.5`  
`new_value_in_float = volume.add_db(value_in_float, subtracted_volume)`

**Result:** new_value_in_float will still be a float value but will have 0.5 dB subtracted from it.

---
