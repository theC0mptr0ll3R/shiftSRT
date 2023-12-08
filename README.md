# shiftSRT
shiftSRT.py ... a Python3 tool to stretch/shrink SRT timestamps (to fit modified video).

I had to sync a bunch of SRT subtitle files to synchronize to time-stretched videos... and it took too much time to manually edit timestamps! So I came up with a coding solution, in hope to save hours after hours of my time.

Usage example: shiftSRT.py -target 00:07:54.056 someSRTfile.srt
^^^ Suppose the original timestamp ends at 00:05:29,600. By setting the timestamp target as "00:07:54,056", you will be shifting each timestamp's timing to 143.83 % of the original. In this example, it writes a new file named "someSRTfile_shiftSRTd.srt" with modified timestamp timings.

library required to pre-install: srt
