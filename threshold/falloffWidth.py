# code to make the efficiency plots

import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.loadtxt("threshold_value.txt",unpack=True)
    y = np.loadtxt("threshold_efficiency_rl.txt",unpack=True)
    i = np.loadtxt('ipulse_efficiency.txt',unpack=True)
    l = np.loadtxt("threshold_efficiency_lr.txt",unpack=True)
    d = np.loadtxt("threshold_efficiency_d.txt",unpack=True)
    o = np.loadtxt("ipulse_efficiency_old.txt",unpack=True)

    new = np.full(x.shape,i)
    old = np.full(x.shape,o)
    plt.plot(x,y,'ro',ms=1.5,label="Right to left veto window: upperbound = 450")
    plt.plot(x,l,'go',ms=1.5,label="Left to right veto window: lowerbound = 100")
    plt.plot(x,d,'bo',ms=1.5,label="Dynamic veto window: lowerbound = mintime - 20")
    plt.plot(x,new,color='steelblue',marker='o',markevery=26,ms=3,label="ipulse==0 efficiency")
    plt.plot(x,old,color='tomato',marker='s',markevery=37,ms=3,label='ipulse==0 efficiency (450 < t < 600) for muons in nominal trigger menu')
    plt.title("Efficiency vs. Width of Pretrigger Veto Threshold Window")
    plt.xlabel("Width of Pretrigger Veto Threshold Window (ns)")
    plt.ylabel("Efficiency")
    plt.legend(frameon=False,fontsize=6)
    plt.show()
    plt.savefig("E_vs_T.pdf",dpi=600)
    plt.close()

    y = np.loadtxt("threshold_derivative.txt",unpack=True)
    plt.plot(x,y,'ko',ms=1.5)
    for i in range(300,430):
        if y[i] < -0.003:
            left = i
            break
    plt.axvline(x=left,color='r',linestyle='--')
    for i in range(400,500):
        if abs(y[i]) < 0.0001:
            right = i
            break
    plt.axvline(x=right,color='r',linestyle='--')
    plt.title("Derivative of Efficiency vs Pretrigger Veto Threshold Window")
    plt.xlabel("Pretrigger Veto Threshold Window (ns)")
    plt.ylabel("Derivative")
    plt.savefig("D_vs_T.pdf",dpi=300)

    width = right-left
    print('Width: ', width)

if __name__ == "__main__":
    main()
