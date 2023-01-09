import json

base = 16

keys = [
    'PATCH%COMP',
    'PATCH%PHASER(1)',
    'PATCH%FLANGER(1)',
    'PATCH%TREMOLO(1)',
    'PATCH%OVERTONE(1)',
    'PATCH%MIXER',
    'PATCH%NS',
    'PATCH%PEQ',
    ]

def patchcom_to_name(patchcom):
    """Convert PATCH%COM list of hex to ASCII."""
    return bytearray.fromhex(''.join(patchcom)).decode()

def report_stats(datadict):
    """"""
    print()
    print('# {}'.format(datadict['name']))
    print('| Index | Min value | Max value | Number of unique values | Comments |')
    print('| ----- | --------- | --------- | ----------------------- | -------- |') 
    for idx in range(len(datadict)-1):
        print('|{}|{}|{}|{}| |'.format(idx, min(datadict[idx]), max(datadict[idx]), len(set(datadict[idx]))))

alldicts = [
    {'name': 'PATCH%SLICER(1)', 
        0: [], 1: [], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8: [], 9: [], 
        10: [], 11: [], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18: [], 19: [], 
        20: [], 21: [], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28: [], 29: [], 
        30: [], 31: [], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38: [], 39: [], 
        40: [], 41: [], 42:[], 43:[], 44:[], 45:[], 46:[], 47:[], 48: [], 49: [], 
        50: [], 51: [], 52:[], 53:[], 54:[], 55:[], 56:[], 57:[], 58: [], 59: [], 
        60: [], 61: [], 62:[], 63:[], 64:[], 65:[], 66:[], 67:[], 68: [], 69: [], 
        70: [], 71: [], 72:[], 73:[], 74:[], 75:[], 76:[], 77:[], 78: [], 79: [], 
        80: [], 81: [], 82:[], 83:[], 84:[], 85:[], 86:[], 87:[], 88: [], 89: [], 
        90: [], 91: [], 92:[], 93:[], 94:[], 95:[], 96:[], 97:[], 98: [], 99: [], 
        100: [], 101: [], 102:[], 103:[], 104:[], 105:[], 106:[], 107:[], 108: [], 109: [], 
        110: [], 111: [], 112:[], 113:[], 114:[], 115:[], 116:[], 117:[], 118: [], 119: [], 
        120: [], 121: [], 122:[], 123:[], },
    {'name': 'PATCH%COMP', 0: [], 1: [], 2:[], 3:[], 4:[], 5:[], 6:[], },
    {'name': 'PATCH%PHASER(1)', 0: [], 1: [], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8: [], 9: [], },
    {'name': 'PATCH%FLANGER(1)', 0: [], 1: [], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8: [], 9: [], 10:[], },
    {'name': 'PATCH%TREMOLO(1)', 0: [], 1: [], 2:[], 3:[], 4:[], 5:[], },
    {'name': 'PATCH%OVERTONE(1)', 0: [], 1: [], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], },
    {'name': 'PATCH%MIXER', 0: [], 1: [], 2:[], 3:[], 4:[], },
    {'name': 'PATCH%NS', 0: [], 1: [], 2:[], },
    {'name': 'PATCH%PEQ', 0: [], 1: [], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8: [], 9: [], 10:[], 11:[], },
    ]

if __name__ == "__main__":
    paths = [
        r"Preset Patches.tsl",
        r"Classic SL-20 Collection.tsl",
        r"Expansion Pack 1.tsl",
        r"Expansion Pack 2.tsl",
        r"Expansion Pack 3.tsl",
        r"Expansion Pack 4.tsl",
        r"Expansion Pack 5.tsl",
        r"Expansion Pack 6.tsl",
        ]
    
    print('|Name'
        '|COMP 0|1|2|3|4|5|6|'
        'PHASER(1) 0|1|2|3|4|5|6|7|8|9|'
        'FLANGER(1) 0|1|2|3|4|5|6|7|8|9|10|'
        'TREMOLO(1) 0|1|2|3|4|5|'
        'OVERTONE(1) 0|1|2|3|4|5|6|7|8|'
        'MIXER 0|1|2|3|4|'
        'NS 0|1|2|'
        'PEQ 0|1|2|3|4|5|6|7|8|9|10|11|'
    )
    
    print('-'.join(['|']*65))
    
    for path in paths:
        with open(path, 'r') as f:
            contents = json.load(f)
            patterns = contents['data'][0]
            
            for pattern in patterns:
            
                paramSet = pattern['paramSet']
            
                name = patchcom_to_name(paramSet['PATCH%COM'])
                        
                values_str = ''
                for key in keys:  
                    values_raw = paramSet[key]
                    values_str += '|'.join([str(int(values_raw[idx], base=16)) for idx in range(len(values_raw))]) + '|'
                
                print('| {} | {} '.format(name, values_str))
      
                for datadict in alldicts:
                    for idx in range(len(datadict)-1): 
                        datadict[idx].append(int(paramSet[datadict['name']][idx], base=16))
               
    
    for datadict in alldicts:
        report_stats(datadict)
 