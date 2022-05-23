"""
Author: Feras Alshehri (falshehri@mail.csuchico.edu)
Brief: scan syslog file, and calculate average frame rate (FPS).
Developer note: This scanner was designed to parse and extract 
                all syslog messages created by the capture.c and
                opencv_capture.cpp, and may not work with any
                other format.
Date: 2/20/2022
"""

from cProfile import label
from turtle import color
from numpy import average
import collections
import pandas as pd
import matplotlib.pyplot as plt

processNames = ["ACV_FINAL"]

def main():

    for p in processNames:
        # parse frame numbers and timestamps from syslog file and store into a 
        frameAndTimestampDict = {}
        colorDetectedAndTimestampDict = {}
        with open('/var/log/syslog') as syslogFile:
            for line in syslogFile:
                if p in line:
                    # print(line)
                    if "got frame #" in line:
                        frameNumber = line.split("got frame #")[1].split(" @ ")[0]
                        timestamp = line.split("@ ")[-1][:-1]
                        frameAndTimestampDict[frameNumber] = timestamp
                    
                    elif "Color detected = " in line:
                        colorDetected = line.split("Color detected = ")[1].split(" @ ")[0]
                        timestamp = line.split("@ ")[-1][:-1]
                        colorDetectedAndTimestampDict[colorDetected] = timestamp
                    
                    else:
                        # undefined message.. ignore
                        continue
        
        # calculate average frame rate on parsed data from syslog
        allTimestampsInS = []
        for k,v in frameAndTimestampDict.items():
            allTimestampsInS.append(int(v.split(".")[0]))

        allTimestampsInSFreq = collections.Counter(allTimestampsInS)
        
        # print results to user
        print(f"Process {p}: ")
        if len(allTimestampsInS) < 1:
            print("\t No data found")
        else:
            print(f"\t sample size = {len(allTimestampsInS)} frames in total.")
            avg = average(list(allTimestampsInSFreq.values()))
            print(f"\t average frame rate = {avg} FPS.")

            # plot distribution
            s = 0
            freqDict = {}
            for _,v in allTimestampsInSFreq.items():
                freqDict[s] = v
                s=s+1

            df = pd.DataFrame.from_dict(freqDict, orient='index')
            df.columns=[f'FPS ({len(allTimestampsInS)} frames)']
            ax = df.plot()
            # df.plot()

            # overlay the average as a red horizontal line
            plt.axhline(y = avg, 
                        color = 'r', 
                        linestyle = '-', 
                        label=f"FPS_avg = {avg:.2f}")
            del df

            # normalize by removing outliers (first and last time seconds)
            print(f"\t>> dropping first and last second's frames count")
            print(f"\t\t>> first second's frames count was {freqDict[0]}")
            print(f"\t\t>> last second's frames count was {freqDict[s-1]}")
            droppedFramesCount = freqDict[0] + freqDict[s-1]
            del freqDict[0]
            del freqDict[s-1]

            df = pd.DataFrame.from_dict(freqDict, orient='index')
            df.columns=[f'Normalized FPS ({len(allTimestampsInS) - droppedFramesCount} frames)']
            df.plot(color = 'g', ax=ax)

            # overlay the average as a red horizontal line
            avg = average(list(freqDict.values()))
            plt.axhline(y = avg, 
                        color = 'orange', 
                        linestyle = '-', 
                        label=f"Normalized FPS_avg = {avg:.2f}")
            plt.legend(loc = 'lower right')
            plt.title(f"Distribution of {p} FPS ")
            plt.xlabel("time [s]")
            plt.ylabel("frame rate [FPS]")
            plt.savefig(f"distribution_plot_{p}_fps")
            plt.cla()

            print(f"\t average frame rate (after outliers removal) = {avg} FPS")

if __name__ == "__main__":
    main()