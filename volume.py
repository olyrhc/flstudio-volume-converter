# flstudio-volume-converter v1.0
# by Robin Calvin (olyrhc)

class __FLdB:
	volume_table = {
	1.0: (5.6,0.0036), 0.98: (5.0,0.0036), 0.943: (4.0,0.0035), 0.907: (3.0,0.0035), 0.87: (2.0,0.0035),
	0.835: (1.0,0.0035), 0.8: (0.0,0.0035),0.765: (-1.0,0.0035), 0.732: (-2.0,0.0032), 0.6962: (-3.0,0.0032),
	0.664: (-4.0,0.00316), 0.632: (-5.0,0.00325), 0.6: (-6.0,0.00319), 0.568: (-7.0,0.0031), 0.536: (-8.0,0.003),
	0.506: (-9.0,0.00295), 0.476: (-10.0,0.0029), 0.447: (-11.0,0.00289), 0.418: (-12.0,0.0027), 0.391: (-13.0,0.00263),
	0.365: (-14.0,0.00253), 0.34: (-15.0,0.0024), 0.316: (-16.0,0.0023), 0.2937: (-17.0,0.0022), 0.272: (-18.0,0.0021),
	0.2501: (-19.0,0.0019), 0.232: (-20.0,0.0019), 0.212: (-21.0,0.0017), 0.195: (-22.0,0.0017), 0.178: (-23.0,0.0015),
	0.163: (-24.0,0.00145), 0.149: (-25.0,0.00135), 0.135: (-26.0,0.00115), 0.123: (-27.0,0.00115), 0.112: (-28.0,0.00105),
	0.101: (-29.0,0.00095), 0.092: (-30.0,0.00091), 0.083: (-31.0,0.0008), 0.075: (-32.0,0.000775), 0.0675: (-33.0,0.000658),
	0.0606: (-34.0,0.0006), 0.0544: (-35.0,0.00053), 0.0489: (-36.0,0.0005), 0.0439: (-37.0,0.00045), 0.0395: (-38.0,0.0004),
	0.0355: (-39.0,0.00038), 0.03175: (-40.0,0.00034), 0.0286: (-41.0,0.00031), 0.0254: (-42.0,0.000265), 0.0228: (-43.0,0.00025),
	0.0203: (-44.0,0.00021), 0.0182: (-45.0,0.00018), 0.0164: (-46.0,0.00018), 0.01457: (-47.0,0.000156), 0.013: (-48.0,0.00014), 
	0.0116: (-49.0,0.000125), 0.0104: (-50.0,0.00011), 0.00925: (-51.0,0.0001), 0.00825: (-52.0,0.000088), 0.00735: (-53.0,0.000076),
	0.00655: (-54.0,0.000066), 0.00585: (-55.0,0.00006), 0.00522: (-56.0,0.0000545), 0.00468: (-57.0,0.000051), 0.0042: (-58.0,0.000046),
	0.0037: (-59.0,0.000037), 0.0033: (-60.0,0.000035), 0.00295: (-61.0,0.000034), 0.00265: (-62.0,0.00003), 0.0023: (-63.0,0.000022),
	0.00205: (-64.0,0.000018), 0.0019: (-65.0,0.000021), 0.00165: (-66.0,0.000019), 0.00145: (-67.0,0.00001), 0.0013: (-68.0,0.00001), 
	0.0012: (-69.0,0.000015), 
	}
	end_table = {
	0.001: -70.5, 0.00095: -71.0, 0.0009: -71.6, 0.0008: -72.3, 0.00075: -73.0, 0.0007: -73.7, 0.00065: -74.5, 0.00055: -75.5,
	0.0005: -76.5, 0.00045: -77.6, 0.0004: -79.0, 0.0003: -80.6, 0.00025: -82.5, 0.0002: -85.0, 0.00015: -88.5, 0.00009: -94.5,
	0.0: -100.0,
	}

global db_to_fl
global fl_to_db

def db_to_fl(db):
	if type(db) == float or type(db) == int:
		if db > 5.6: db = 5.6
		if db >= -69.9:
			voldata = [item for item in __FLdB.volume_table.items() if item[1][0] >= db][-1]
			vol = voldata[0] ; voldb = voldata[1][0] ; dist = voldata[1][1]
			return vol - round(voldb-db,1) * 10 * dist
		elif db <= -70.0:
			closest = min(__FLdB.end_table.values(), key = lambda value: abs(value-db))
			end_table = {v: k for k, v in __FLdB.end_table.items()}
			return end_table[closest]
	else:
		raise TypeError("argument 'db' must be of type float or int.")


def fl_to_db(volume):
	if type(volume) == float:
		if volume > 1.0: volume = 1.0
		if volume >= 0.00102:
			vol = [key for key in __FLdB.volume_table.keys() if key >= volume][-1]
			dist = __FLdB.volume_table[vol][1]
			decimals = {vol: 0.0, vol-1*dist: 0.1, vol-2*dist: 0.2, vol-3*dist: 0.3, vol-4*dist: 0.4,
						vol-5*dist: 0.5, vol-6*dist: 0.6, vol-7*dist: 0.7, vol-8*dist: 0.8, vol-9*dist: 0.9, }
			closest = min(decimals.keys(), key = lambda key: abs(key-volume))
			db = __FLdB.volume_table[vol][0]
			return round(db-decimals[closest],1)
		elif volume < 0.00102:
			closest = min(__FLdB.end_table.keys(), key = lambda key: abs(key-volume))
			return __FLdB.end_table[closest]
	else:
		raise TypeError("argument 'volume' must be of type float.")


def add_db(volume,db):
	if type(volume) == float:
		if type(db) == float or type(db) == int:
			return db_to_fl(fl_to_db(volume) + db)
		else:
			raise TypeError("argument 'db' must be of type float or int.")
	else:
		raise TypeError("argument 'volume' must be of type float.")
