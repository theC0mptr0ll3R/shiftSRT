#!/usr/bin/env python
# shiftSRT.py
# Oki Mikito - Media to People, Incorporated, 2023
# Usage example (1): shiftSRT.py -target 00:05:42,240 -shift 00:00:02,100 someSRTfile.srt
# ^^^ ... takes in "someSRTfile.srt", stretch or modify the SRT timings to match the specified end target ("00:05:42.240")
# ver. 1.0 : Dec 09, 2023

import codecs, sys, srt, datetime

f = ''
fList = []
fdic = {}
idnum = 1
original_endTC = ''
target_endTC = ''
arg = sys.argv
targetRatio = 1.0
shiftTC = '00:00:00,000'

newFileName = arg[-1].replace('.SRT', '.srt') # ...foolproof, just in case
newFileName = newFileName.replace('.srt', '_shiftSRTd.srt')

if not '-target' in arg:
    print('   Usage example (1): shiftSRT -target 00:05:42.240 someSRTfile.srt\n   Exiting...')
    sys.exit(0)
else:   # ... convert the target TC to timedelta
    target_endTC = arg[arg.index('-target') + 1]
    target_endTC = srt.srt_timestamp_to_timedelta(target_endTC)
    if '-shift' in arg: # ... to see how much timestamp shifting is required
        shiftTC = arg[arg.index('-shift') + 1]
    shiftTC = srt.srt_timestamp_to_timedelta(shiftTC)

with codecs.open(arg[-1], 'r', encoding='utf_8_sig') as fbuf:
    f = fbuf.read()

fList = f.split('\r\n') # ... just to extract the timestamp data... kinda ugly ;-)

for L in fList: # ... building a dictionary set, linking w/ ID and timecode
    if ' --> ' in L:
        L = L.split(' --> ')
        fdic['<TC_' + str(idnum) + '>'] = L[0]
        idnum += 1
        fdic['<TC_' + str(idnum) + '>'] = L[1]
        idnum += 1

for t in fdic.values(): # ... replacing timecode instance w/ ID for later processing
    f = f.replace(t, list(fdic.keys())[list(fdic.values()).index(t)])

# ... find out the original SRT timestamp to see how much shrinking/stretching it may require:
original_endTC = list(fdic.values())[-1]
original_endTC = srt.srt_timestamp_to_timedelta(original_endTC)
targetRatio = (target_endTC - shiftTC) / original_endTC
print('ratio:', round(targetRatio * 100, 2), '%')

for i in fdic.keys():
    td = srt.srt_timestamp_to_timedelta(fdic[i])
    td = (td + shiftTC) * targetRatio
    f = f.replace(i, srt.timedelta_to_srt_timestamp(td))

with codecs.open(newFileName, 'w', encoding='utf_8_sig') as tf:
    tf.write(f)

