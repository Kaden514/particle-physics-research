import awkward as ak
import uproot
import ROOT
from array import array
import argparse
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq
from matplotlib.backends.backend_pdf import PdfPages

LIMIT = 100

def plot1D(data,histo):
    flatdata = ak.flatten(data,axis=None)
    n_events = len(flatdata)
    weight = ak.ones_like(flatdata)
    if n_events > 0:
        histo.FillN(n_events, array('d',flatdata), array('d',weight),1)

def hist_fft(hist):
    bin_counts = np.array([hist.GetBinContent(i) for i in range(1,hist.GetNbinsX() + 1)])
    d = hist.GetBinWidth(1)

    fft_vals = rfft(bin_counts)
    mag = np.abs(fft_vals)[1:]
    fft_freqs = rfftfreq(len(bin_counts), d=d)[1:]
    df = fft_freqs[1] - fft_freqs[0]
    edges = np.append(fft_freqs - df / 2, fft_freqs[-1] + df / 2)
    return edges, mag

def main():
    parser = argparse.ArgumentParser(description="Choose if you want to execute the particularly time-consuming parts of code. Don't add any flags if you don't need the optional parts.")
    parser.add_argument('-test',action='store_true',help='Shortened test analysis')
    parser.add_argument('-us106',action='store_true',help='runs with 106 us veto deadtime')
    parser.add_argument('-us200',action='store_true',help='runs with 200 us veto deadtime')
    parser.add_argument('-us8',action='store_true',help='runs with 8 us veto deadtime')
    args = parser.parse_args()

    ROOT.gStyle.SetOptStat(0)

    file2501 = ['original file directory taken out for proprietary purposes']
    file2446 = ['original file directory taken out for proprietary purposes']
    file2548 = ['original file directory taken out for proprietary purposes']
    file2590 = ['original file directory taken out for proprietary purposes']

    file2563 = ['original file directory taken out for proprietary purposes']
    file2578 = ['original file directory taken out for proprietary purposes']
    file2581 = ['original file directory taken out for proprietary purposes']
    file2584 = ['original file directory taken out for proprietary purposes']

    file2391 = ['original file directory taken out for proprietary purposes']
    file2392 = ['original file directory taken out for proprietary purposes']
    file2394 = ['original file directory taken out for proprietary purposes']

    file2395 = ['original file directory taken out for proprietary purposes']
    file2396 = ['original file directory taken out for proprietary purpose']
    file2398 = ['original file directory taken out for proprietary purposes']
    file2400 = ['original file directory taken out for proprietary purposes']

    nbins = 5000
    binwidth = 20e-9

    if args.us106:
        filelist = [file2563,file2578,file2581,file2584]
        mintime = 106e-6
        minbin = 100e-6
        maxbin = 200e-6
    if args.us200:
        filelist = [file2391,file2392,file2394]
        mintime = 200e-6
        minbin = 150e-6
        maxbin = 250e-6
    if args.us8:
        filelist = [file2395,file2396,file2398,file2400]
        mintime = 8e-6
        minbin = 0
        maxbin = 100e-6
    var = ['tClockCycles','tTrigger','tPrevPanelVeto']

    maxtime = mintime + nbins * binwidth

    output = ROOT.TFile('mindeadtime.root','RECREATE')
    deadtime = ROOT.TH1D('deadtime','Time Difference Between Current Trigger and Previous Trigger',100,100e-6,200e-6)
    dead8ns = ROOT.TH1D('dead8ns','Minimum Dead-time Edge (8 ns bins)',12500,135e-6,235e-6)
    dead20ns = ROOT.TH1D('dead20ns','Minimum Dead-time Edge (20 ns bins)',5000,135-6,235-6)
    deadveto = ROOT.TH1D('deadveto','Time Difference Between Current Trigger and Previous Veto',100,minbin,maxbin)
    veto20ns = ROOT.TH1D('veto20ns','Minimum Veto Dead-time Edge (20 ns bins)',nbins,mintime,maxtime)

    timehisto = [deadtime,dead8ns,dead20ns,deadveto,veto20ns]
    histograms = timehisto

    for hist in timehisto:
        hist.GetXaxis().SetTitle("Time (s)")
        hist.GetYaxis().SetTitle("Counts")
    
    if args.test:
        print('TESTING',LIMIT)

    for file in filelist:
        counter = 0

        for data in uproot.iterate(file,var,library='ak',step_size=1000):
            if args.test:
                counter += 1
                print(counter)
            if counter > LIMIT:
                break

            t_diff = []
            for t in range(1,len(data['tClockCycles'])):
                t_diff.append(data['tClockCycles'][t] * 20e-9 - data['tClockCycles'][t-1] * 20e-9)
            v_diff = ((data['tClockCycles'] - data['tPrevPanelVeto']) * (20e-9))

            plot1D(t_diff,deadtime)
            plot1D(t_diff,dead20ns)
            plot1D(v_diff,deadveto)
            plot1D(v_diff,veto20ns)

        print('file complete')

    print('all files done')
    print(veto20ns.GetBinWidth(2))    

    for h,label,pdff,pdfp in [(veto20ns,'Veto Dead-time FFT 20 ns bins','20_ns_plot_v_f.pdf','20_ns_plot_v_p.pdf'),
                              (dead20ns,'Dead-time FFT 20 ns bins','20_ns_plot_d_f.pdf','20_ns_plot_d_p.pdf')]:
        f,m = hist_fft(h)
        period = 1/f
        plt.stairs(m,f/1e6)
        plt.title(label)
        plt.xlabel('Frequency conjugate to Δt [MHz]')
        plt.ylabel('|FFT|')
        plt.show()
        plt.savefig(pdff,dpi=600, bbox_inches='tight')
        plt.close()

        plt.stairs(m,period*1e6)
        plt.xscale('log')
        plt.title(label)
        plt.xlabel('Period [μs]')
        plt.ylabel('|FFT|')
        plt.show()
        plt.savefig(pdfp,dpi=600, bbox_inches='tight')
        plt.close()

    for hist in histograms:
        hist.Write()
    output.Close()
if __name__ == "__main__":
    main()