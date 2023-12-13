#!/usr/bin/env python
# shiftSRT.py
# Oki Mikito - Media to People, Incorporated, 2023
# Usage example (1): shiftSRT.py -target 00:05:42,240 -shift 00:00:02,100 someSRTfile.srt
# ^^^ ... takes in "someSRTfile.srt", stretch or modify the SRT timings to match the specified end target ("00:05:42.240")
# ver. 1.0 : Dec 09, 2023
# ver. 1.1 : Dec 13, 2023 - fix negative value shifting bug

import codecs, sys, re, srt

f = ''
original_endTC = ''
target_endTC = '00:00:00,000'
tFlag = 0
arg = sys.argv
targetRatio = 1.0
shiftTC = '00:00:00,000'
negativeShiftFlag = 0

newFileName = arg[-1].replace('.SRT', '.srt') # ...foolproof, just in case
newFileName = newFileName.replace('.srt', '_shifted.srt')

if len(arg) == 1:
    print('   Usage example (1): shiftSRT -target 00:05:42.240 someSRTfile.srt\n   Exiting...')
    sys.exit(0)
else:   # ... convert the target TC to timedelta
    if '-target' in arg:
        target_endTC = arg[arg.index('-target') + 1]
    else:
        tFlag = 1
    target_endTC = srt.srt_timestamp_to_timedelta(target_endTC)
    if '-shift' in arg: # ... to see how much timestamp shifting is required
        shiftTC = arg[arg.index('-shift') + 1]
        if '-' in shiftTC:
            negativeShiftFlag = 1
            shiftTC = re.sub('-', '', shiftTC)
        shiftTC = srt.srt_timestamp_to_timedelta(shiftTC)

with codecs.open(arg[-1], 'r', encoding='utf_8_sig') as fbuf:
    f = fbuf.read()

f = re.sub('(\r\n)+', '\r\n', f)

f = srt.make_legal_content(f)
sBuf = srt.parse(f)
sub = list(sBuf)

# ... find out the original SRT timestamp to see how much shrinking/stretching it may require:
original_endTC = sub[-1].end
if tFlag == 0:
    if negativeShiftFlag == 1:
        targetRatio = (target_endTC + shiftTC) / original_endTC
    else:
        targetRatio = (target_endTC - shiftTC) / original_endTC
else:
    target_endTC = original_endTC
    targetRatio = 1.0
print('ratio:', round(targetRatio * 100, 2), '%')

for i in range(len(sub)):
    if negativeShiftFlag == 1:
        sub[i].start = (sub[i].start * targetRatio) - shiftTC
        sub[i].end = (sub[i].end * targetRatio) - shiftTC
    else:
        sub[i].start = (sub[i].start * targetRatio) + shiftTC
        sub[i].end = (sub[i].end * targetRatio) + shiftTC

with codecs.open(newFileName, 'w', encoding='utf_8_sig') as tf:
    tf.write(srt.compose(sub))

