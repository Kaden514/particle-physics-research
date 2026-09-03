# Usage: python rateLumiComparison.py -flag1 -flag2
# Flags are for whether you want the efficiency vs. time plots done for pulse level or trigger level
# Flags:
# -pulse: pulse level
# -trigger: trigger level

import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Choose between pulse-level analysis or trigger-level analysis or both")
    parser.add_argument("-trigger",action='store_true',help='Trigger-level analysis')
    parser.add_argument('-pulse',action='store_true',help='Pulse-level analylsis')
    args = parser.parse_args()

    x = np.loadtxt("timeshift.txt",unpack = True)

    if args.trigger:
        t = np.loadtxt("efficiency.txt",unpack = True)
        plt.plot(x,t,'bo')
        plt.ylim(0.8,1)
        plt.title('Efficiency of Quiet-time vs. Nominal Trigger Time (Trigger Level)')
        plt.xlabel('Shift From Original Run Starts (s)')
        plt.ylabel("Efficiency")
        plt.show()
        plt.savefig("efficiency_plot.pdf",dpi=600)
        plt.close()

    if args.pulse:
        p = np.loadtxt("pulse_efficiency.txt",unpack = True)
        plt.plot(x,p,'bo')
        plt.ylim(0.9,1.05)
        plt.title('Efficiency of Quiet-time vs. Nominal Trigger Time (Pulse Level)')
        plt.xlabel('Shift From Original Run Starts (s)')
        plt.ylabel("Efficiency")
        plt.show()
        plt.savefig("efficiency_pulse_plot.pdf",dpi=600)
        plt.close()

if __name__ == '__main__':
    main()