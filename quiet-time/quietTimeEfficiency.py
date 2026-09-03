# Usage: python quietTimeEfficiency.py -flag1 -flag2...
# Flags depend on which type of analysis you want: pulse level or trigger level (you could do both too)
# Flags:
# -pulse: pulse level analysis
# -trigger: trigger level analysis
# -test: no time shift implemented, just the original run starts used

import awkward as ak
import uproot
import ROOT
from array import array
from ROOT import TLegend
from ROOT import gPad
import argparse
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import pandas as pd

LIMIT = 50

# function for plotting 1D histograms
def plot1D(data,histo):
    flatdata = ak.flatten(data,axis=None)
    n_events = len(flatdata)
    weight = ak.ones_like(flatdata)
    if n_events > 0:
        histo.FillN(n_events, array('d',flatdata), array('d',weight),1)

# function for plotting 2D histograms
def plot2D(x,y,histo):
    flatx = ak.flatten(x,axis=None)
    flaty = ak.flatten(y,axis=None)
    n_events = len(flatx)
    weight = ak.ones_like(flatx)
    if n_events > 0:
        histo.FillN(n_events, array('d',flatx), array('d',flaty), array('d',weight),1)

# function for comparing histograms directly
def comparison(c,file,hist1,hist2):
    canvas = ROOT.TCanvas(f'{c}')
    begin = file + '['
    end = file + ']'
    canvas.Print(f'{begin}')

    hist2.SetLineColor(ROOT.kGreen)
    hist1.SetStats(0)
    hist2.SetStats(0)

    max_val = max(hist1.GetMaximum(), hist2.GetMaximum())
    hist1.SetMaximum(max_val * 1.1)
    hist1.Draw()
    hist2.Draw("SAME")

    legend = TLegend(0.35, 0.8, 0.75, 0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    legend.AddEntry(hist1, hist1.GetTitle(), "l")
    legend.AddEntry(hist2, hist2.GetTitle(), "l")
    legend.Draw()

    canvas.Print(f'{file}')
    canvas.Print(f'{end}')
    canvas.Close()

def main():
    parser = argparse.ArgumentParser(description="Choose between pulse-level analysis or trigger-level analysis or both")
    parser.add_argument("-trigger",action='store_true',help='Trigger-level analysis')
    parser.add_argument('-pulse',action='store_true',help='Pulse-level analylsis')
    parser.add_argument('-test',action='store_true',help='Shortened test analysis')
    args = parser.parse_args()

    quietfile = {'original file directory taken out for proprietary purposes'}
    loudfile = {'original file directory taken out for proprietary purposes'}
    quietpulse = ['original file directory taken out for proprietary purposes']
    loudpulse = ['original file directory taken out for proprietary purposes']
    
    triggervar = ['clockCycles','trigger','rollovers','ticksSinceOrbital','time','startTime']
    pulsevar = ["timeFit_module_calibrated", 'time', "chan", "layer", "event_time_fromTDC", "area", "ipulse", "energy", "type", "height", "duration", "row", "column", "timeFit_module_finalCalibration",'nPE']

    true_quietstart = 1748514061
    true_loudstart = 1748516849
    true_loudend = 1748518200

    output = ROOT.TFile('quietTimeEfficiency.root','RECREATE') # output file

    quiettimeplot = ROOT.TH1D('quiettimeplot','quiet triggertime',2000,true_quietstart-10,true_loudend+10)
    loudtimeplot = ROOT.TH1D('loudtimeplot','nominal triggertime',2000,true_quietstart-10,true_loudend+10)
    quietrateplot = ROOT.TH1D('quietrateplot','quiet-time trigger-level instantaneous rate',2000,true_quietstart-10,true_loudend+10)
    loudrateplot = ROOT.TH1D('loudrateplot','nominal trigger-level instantaneous rate',2000,true_quietstart-10,true_loudend+10)
    quietratelumiplot = ROOT.TH1D('quietratelumi','quiet-time rate/luminosity',2000,true_quietstart-10,true_loudend+10)
    loudratelumiplot = ROOT.TH1D('loudratelumi','nominal rate/luminosity',2000,true_quietstart-10,true_loudend+10)
    quietlumi = ROOT.TH1D('quietlumi','quiet-time rate/luminosity',200,0,0.01)
    loudlumi = ROOT.TH1D('loudlumi','nominal rate/luminosity',200,0,0.01)
    efficiencyplot = ROOT.TH1D('efficiency','Efficiency of Quiet Trigger-time vs. Nominal',50,.9,1)

    quietpulsetimeplot = ROOT.TH1D('quietpulsetimeplot','quiet pulse time',2000,true_quietstart-10,true_loudend+10)
    loudpulsetimeplot = ROOT.TH1D('loudpulsetimeplot','nominal pulse time',2000,true_quietstart-10,true_loudend+10)
    quietpulserateplot = ROOT.TH1D('quietpulserateplot','quiet-time pulse-level rate',2000,true_quietstart-10,true_loudend+10)
    loudpulserateplot = ROOT.TH1D('loudpulserateplot','nominal pulse-level rate',2000,true_quietstart-10,true_loudend+10)
    quietpulselumiplot = ROOT.TH1D('quietpulselumiplot','quiet-time pulse-level rate/luminosity',2000,true_quietstart-10,true_loudend+10)
    loudpulselumiplot = ROOT.TH1D('loudpulselumiplot','nominal pulse-level rate/luminosity',2000,true_quietstart-10,true_loudend+10)
    quietpulselumi = ROOT.TH1D('quietpulselumi','quiet-time pulse-level rate/luminosity',100,0,.002)
    loudpulselumi = ROOT.TH1D('loudpulselumi','nominal pulse-level rate/luminosity',100,0,.002)
    pulseefficiencyplot = ROOT.TH1D('pulseefficiency','Efficiency of Quiet Pulse-time vs. Nominal',50,.9,1.1)

    quiet_binwidth = quiettimeplot.GetBinWidth(20)
    loud_binwidth = loudtimeplot.GetBinWidth(20)
    quiet_pulse_binwidth = quietpulsetimeplot.GetBinWidth(20)
    loud_pulse_binwidth = loudpulsetimeplot.GetBinWidth(20)

    # histogram lists
    timehist = [quiettimeplot,loudtimeplot,quietrateplot,loudrateplot,quietratelumiplot,loudratelumiplot,quietpulserateplot,loudpulserateplot,quietpulselumiplot,loudpulselumiplot,quietpulsetimeplot,loudpulsetimeplot]
    for hist in timehist:
        hist.GetXaxis().SetTitle("Epoch Time (s)")

    lumihist = [quietlumi, loudlumi,quietpulselumi,loudpulselumi]
    for hist in lumihist:
        hist.GetXaxis().SetTitle("rate/luminosity (pb)")
        hist.GetYaxis().SetTitle("Counts")
    
    effhist = [efficiencyplot,pulseefficiencyplot]
    for hist in effhist:
        hist.GetXaxis().SetTitle("Efficiency")

    histograms = timehist + lumihist + effhist

    lower_time = -50
    upper_time = 50
    f = open("timeshift.txt",'w')
    g = open("efficiency.txt",'w')
    p = open('pulse_efficiency.txt','w')
    canvastrigger = ROOT.TCanvas('lumicanvas')
    canvastrigger.Print('rate_lumi_comparison.pdf[')
    canvaspulse = ROOT.TCanvas('pulsecanvas')
    canvaspulse.Print('rate_lumi_pulse_comparison.pdf[')
    efficiency_list = []
    efficiency_pulse = []

    def fitting(c,file,hist1,hist2,eff,text):
        c.cd()

        hist1.Fit("gaus","Q")
        hist2.Fit("gaus","Q")
        hist1.SetStats(0)
        hist2.SetStats(0)

        d = hist1.GetFunction("gaus")
        e = hist2.GetFunction("gaus")

        mean1 = d.GetParameter(1)
        sigma1 = d.GetParameter(2)
        error1 = d.GetParError(1)
        mean2 = e.GetParameter(1)
        sigma2 = e.GetParameter(2)
        error2 = e.GetParError(1)

        print(f'{c} quiet:', error1)
        print(f'{c} loud:', error2)

        hist1.Fit("gaus","R","",mean1-(sigma1 * 1.5),mean1+(sigma1 * 1.5))
        hist2.Fit("gaus","R","",mean2-(sigma2 * 1.5),mean2+(sigma2*1.5))
        d = hist1.GetFunction('gaus')
        e = hist2.GetFunction('gaus')
        quietmean = d.GetParameter(1)
        loudmean = e.GetParameter(1)

        text.write(f"\n{quietmean/loudmean}")
        eff.append(quietmean/loudmean)

        hist1.SetLineColor(ROOT.kBlue)
        hist2.SetLineColor(ROOT.kGreen)
        hist1.SetTitle(f'Time shift: {dt}')
        max_val = max(hist1.GetMaximum(), hist2.GetMaximum())
        hist1.SetMaximum(max_val * 1.1)
        hist1.Draw()
        hist2.Draw("SAME")

        legend = TLegend(0.7, 0.75, 0.90, 0.87)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        if args.trigger:
            legend.AddEntry(hist1, 'quiet trigger-time', "l")
            legend.AddEntry(hist2, 'nominal trigger-time', "l")
        if args.pulse:
            legend.AddEntry(hist1, 'quiet pulse-time', "l")
            legend.AddEntry(hist2, 'nominal pulse-time', "l")
        legend.Draw()

        c.Print(f'{file}')
    
    if args.test:
        print('TESTING ',LIMIT)
        lower_time = 0
        upper_time = 0

    quiet_events = 0
    quiet_muon_events = 0
    loud_events = 0
    loud_muon_events = 0

    for t in range(lower_time,upper_time+1):

        dt = t*0.1
        quietstart = true_quietstart + dt
        loudstart = true_loudstart + dt
        loudend = true_loudend + dt

        f.write(f"\n{dt}")

        for hist in histograms:
            hist.Reset("ICESM")

        if args.trigger:
            for data in uproot.iterate(quietfile, triggervar, library='ak', step_size=1000):
                data['time'] = data['time'] + np.float64(quietstart)
                plot1D(data['time'],quiettimeplot)

            for data in uproot.iterate(loudfile,triggervar,library='ak',step_size=1000):
                data['time'] = data['time'] + np.float64(loudstart)
                plot1D(data['time'],loudtimeplot)

            for i in range(1,quiettimeplot.GetNbinsX() + 1):
                counts = quiettimeplot.GetBinContent(i)
                quietrateplot.SetBinContent(i, counts/quiet_binwidth)

            for i in range(1,loudtimeplot.GetNbinsX() + 1):
                counts = loudtimeplot.GetBinContent(i)
                loudrateplot.SetBinContent(i, counts/loud_binwidth)

        if args.pulse:
            for data in uproot.iterate(quietpulse,pulsevar,library='ak',step_size=1000):

                data["event_time_fromTDC"] = ak.broadcast_arrays(data["event_time_fromTDC"], data["timeFit_module_calibrated"])[0]
                data['time_shift'] = data['event_time_fromTDC'] + dt                
                layer0 = ((data['layer']==0) & (data['type']==0))
                layer1 = ((data['layer']==1) & (data['type']==0))
                layer2 = ((data['layer']==2) & (data['type']==0))
                layer3 = ((data['layer']==3) & (data['type']==0))

                mask1 = ak.any(((layer0) 
                        & (data['area']>95000*1.25)
                        ),axis=-1) & ak.any(((layer1) 
                        & (data['area']>95000*1.25)
                        ),axis=-1) & ak.any(((layer2)
                        & (data['area']>95000*1.25)
                        ),axis=-1) & ak.any(((layer3)
                        & (data['area']>95000*1.25)
                        ),axis=-1) # masking for muon restrictions
                maskmuon = mask1 & ak.any(((data["chan"] == 16) & (data['area']>30000*1.25)), axis=-1) & ak.any(((data["chan"] == 18) & (data['area']>18000*1.25)), axis=-1)
                muondata = data[maskmuon]

                plot1D(ak.firsts(muondata['time_shift'],axis=-1),quietpulsetimeplot)

            for data in uproot.iterate(loudpulse,pulsevar,library='ak',step_size=1000):

                data["event_time_fromTDC"] = ak.broadcast_arrays(data["event_time_fromTDC"], data["timeFit_module_calibrated"])[0]
                data['time_shift'] = data['event_time_fromTDC'] + dt
                layer0 = ((data['layer']==0) & (data['type']==0))
                layer1 = ((data['layer']==1) & (data['type']==0))
                layer2 = ((data['layer']==2) & (data['type']==0))
                layer3 = ((data['layer']==3) & (data['type']==0))

                mask1 = ak.any(((layer0) 
                        & (data['area']>95000*1.25)
                        ),axis=-1) & ak.any(((layer1) 
                        & (data['area']>95000*1.25)
                        ),axis=-1) & ak.any(((layer2)
                        & (data['area']>95000*1.25)
                        ),axis=-1) & ak.any(((layer3)
                        & (data['area']>95000*1.25)
                        ),axis=-1) # masking for muon restrictions
                maskmuon = mask1 & ak.any(((data["chan"] == 16) & (data['area']>30000*1.25)), axis=-1) & ak.any(((data["chan"] == 18) & (data['area']>18000*1.25)), axis=-1)
                muondata = data[maskmuon]
                plot1D(ak.firsts(muondata['time_shift'],axis=-1),loudpulsetimeplot)

            for i in range(1,quietpulsetimeplot.GetNbinsX() + 1):
                counts = quietpulsetimeplot.GetBinContent(i)
                quietpulserateplot.SetBinContent(i, counts/quiet_pulse_binwidth)
            
            for j in range(1,loudpulsetimeplot.GetNbinsX() + 1):
                counts = loudpulsetimeplot.GetBinContent(j)
                loudpulserateplot.SetBinContent(j, counts/loud_pulse_binwidth)
            
        quietrateplot.GetYaxis().SetTitle("Rate (Hz)")
        loudrateplot.GetYaxis().SetTitle("Rate (Hz)")
        quietpulserateplot.GetYaxis().SetTitle("Rate (Hz)")
        loudpulserateplot.GetYaxis().SetTitle("Rate (Hz)")

        df = pd.read_csv('Fill10673_ATLASLuminosity_TotInst.csv',header=None)
        df['datetime'] = pd.to_datetime(
            df.iloc[:,0],
            format = "%Y-%m-%d %H:%M:%S.%f",
            utc=False)
        df['epoch_seconds'] = (df['datetime'] - pd.Timestamp("1970-01-01")) / pd.Timedelta(seconds=1)

        nbins = 2000
        xlow = quietstart
        xhigh = loudend
        edges = np.linspace(xlow, xhigh, nbins+1)
        df['bin_idx'] = np.digitize(df['epoch_seconds'],edges)
        in_range = df.loc[(df['bin_idx'] >= 1) 
                    & (df['bin_idx'] <= nbins)]

        quiet_rate_lumi_list = np.array([])
        loud_rate_lumi_list = np.array([])
        quietpulse_rate_lumi_list = np.array([])
        loudpulse_rate_lumi_list = np.array([])
        
        for b in range(1,nbins+1):
            lumi = in_range.loc[in_range['bin_idx'] == b, 1]
            if len(lumi) > 0:
                avg_lumi = lumi.mean()

                if args.trigger:
                    quiet_rate_lumi = quietrateplot.GetBinContent(b)/avg_lumi
                    quietratelumiplot.SetBinContent(b, quiet_rate_lumi)
                    if quiet_rate_lumi != 0:
                        quiet_rate_lumi_list = np.append(quiet_rate_lumi_list,quiet_rate_lumi)

                    loud_rate_lumi = loudrateplot.GetBinContent(b)/avg_lumi
                    loudratelumiplot.SetBinContent(b, loud_rate_lumi)
                    if loud_rate_lumi != 0:
                        loud_rate_lumi_list = np.append(loud_rate_lumi_list,loud_rate_lumi)

                if args.pulse:
                    quietpulse_rate_lumi = quietpulserateplot.GetBinContent(b)/avg_lumi
                    quietpulselumiplot.SetBinContent(b,quietpulse_rate_lumi)
                    if quietpulse_rate_lumi != 0:
                        quietpulse_rate_lumi_list = np.append(quietpulse_rate_lumi_list,quietpulse_rate_lumi)

                    loudpulse_rate_lumi = loudpulserateplot.GetBinContent(b)/avg_lumi
                    loudpulselumiplot.SetBinContent(b,loudpulse_rate_lumi)
                    if loudpulse_rate_lumi != 0:
                        loudpulse_rate_lumi_list = np.append(loudpulse_rate_lumi_list,loudpulse_rate_lumi)

        quietratelumiplot.GetYaxis().SetTitle('Rate/Luminosity (pb)')
        loudratelumiplot.GetYaxis().SetTitle('Rate/Luminosity (pb)')
        quietpulselumiplot.GetYaxis().SetTitle("Rate/Luminosity (pb)")
        loudpulselumiplot.GetYaxis().SetTitle("Rate/Luminosity (pb)")

        quiet_rate_lumi_data = ak.from_numpy(quiet_rate_lumi_list)
        loud_rate_lumi_data = ak.from_numpy(loud_rate_lumi_list)
        quietpulse_rate_lumi_data = ak.from_numpy(quietpulse_rate_lumi_list)
        loudpulse_rate_lumi_data = ak.from_numpy(loudpulse_rate_lumi_list)
        
        plot1D(quiet_rate_lumi_data,quietlumi)
        plot1D(loud_rate_lumi_data,loudlumi)
        plot1D(quietpulse_rate_lumi_data,quietpulselumi)
        plot1D(loudpulse_rate_lumi_data,loudpulselumi)
        
        if args.trigger:
            fitting(canvastrigger,"rate_lumi_comparison.pdf",quietlumi,loudlumi,efficiency_list,g)
        if args.pulse:
            fitting(canvaspulse,"rate_lumi_pulse_comparison.pdf",quietpulselumi,loudpulselumi,efficiency_pulse,p)
    
    efficiency_data = ak.Array(efficiency_list)
    efficiency_pulse_data = ak.Array(efficiency_pulse)
    plot1D(efficiency_data,efficiencyplot)
    plot1D(efficiency_pulse_data,pulseefficiencyplot)

    canvastrigger.Print('rate_lumi_comparison.pdf]')
    canvaspulse.Print('rate_lumi_pulse_comparison.pdf]')

    for hist in histograms:
        hist.Write()
    f.close()
    g.close()
    p.close()
    output.Close()

if __name__ == "__main__":
    main()