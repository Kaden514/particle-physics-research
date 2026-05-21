# Usage: python threshold.py --flag1 --flag2... --flagn
# Optional flags are to save on time in the event that you don't need to do certain things
# Optional flags:
# --rl: filling efficiency text file for right to left veto method
# --lr: filling efficiency text file for left to right veto method
# --test: only run up to LIMIT loops of data, for quick testing purposes
# --d: filling efficiency text file for dynamic veto method
# --old: using run 2372 (should probably not be used with --rl --lr and --d since this is just for ipulse efficiency)

import awkward as ak
import uproot
import ROOT
from array import array
from ROOT import TLegend
from ROOT import gPad
import argparse
import numpy as np
import matplotlib.pyplot as plt

LIMIT = 101

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
    hist1.Draw()
    hist2.Draw("SAME")

    legend = TLegend(0.5, 0.8, 0.9, 0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    legend.AddEntry(hist1, hist1.GetTitle(), "l")
    legend.AddEntry(hist2, hist2.GetTitle(), "l")
    legend.Draw()

    canvas.Print(f'{file}')
    canvas.Print(f'{end}')
    canvas.Close()
    return canvas,legend

def main():
    parser = argparse.ArgumentParser(description="Choose if you want to execute the particularly time-consuming parts of code. Don't add any flags if you don't need the optional parts.")
    parser.add_argument("--rl",action="store_true",help="Static window from right to left")
    parser.add_argument("--lr",action='store_true',help='Static window from left to right')
    parser.add_argument("--test",action='store_true',help='Test run for 100 data chunks')
    parser.add_argument('--d',action='store_true',help='Dynamic window with right bound at mintime - 20 ns')
    parser.add_argument('--old',action='store_true',help='Using old run 2372')
    args = parser.parse_args()
    
    # choosing which run to use
    if args.old:
        file = 'file directory taken out from original version for proprietary reasons'
    if not args.old:
        file = 'file directory taken out from original version for proprietary reasons'

    var = ["timeFit_module_calibrated", 'time', "chan", "layer", "event_time_fromTDC", "area", "ipulse", "energy", "type", "height", "duration", "row", "column", "timeFit_module_finalCalibration",'nPE']

    output = ROOT.TFile('threshold.root','RECREATE') # output file
    timefit = ROOT.TH1D('timefit','time For Muonic Events', 256, 0, 1280)
    thresh200 = ROOT.TH1D('thresh200','Window width = 200 ns', 256, 0, 1280)
    thresh250 = ROOT.TH1D('thresh250','Window width = 250 ns', 256, 0, 1280)
    thresh300 = ROOT.TH1D('thresh300','Window width = 300 ns', 256, 0, 1280)
    thresh400 = ROOT.TH1D('thresh400','Window width = 400 ns', 256, 0, 1280)
    thresh500 = ROOT.TH1D('thresh500','Window width = 500 ns', 256, 0, 1280)
    thresh550 = ROOT.TH1D('thresh550','Window width = 550 ns', 256, 0, 1280)
    t1before = ROOT.TH1D('t1before','Time Difference Between Max Pulses in Layers 0-1 Before Cut', 200, -100, 100)
    t2before = ROOT.TH1D('t2before','Time Difference Between Max Pulses in Layers 1-2 Before Cut', 200, -100,100)
    t3before = ROOT.TH1D('t3before','Time Difference Between Max Pulses in Layers 2-3 Before Cut',200,-100,100)
    t1after = ROOT.TH1D('t1after','Time Difference Between Max Pulses in Layers 0-1 After Cut', 200, -100, 100)
    t2after = ROOT.TH1D('t2after','Time Difference Between Max Pulses in Layers 1-2 After Cut', 200, -100, 100)
    t3after = ROOT.TH1D('t3after','Time Difference Between Max Pulses in Layers 2-3 After Cut', 200, -100, 100)
    maxpulses = ROOT.TH1D('maxpulses','Max Pulse Per Layer',256,0,1280)
    threshmax200 = ROOT.TH1D('threshmax200','Max pulses for 200 ns window',256,0,1280)
    threshmax250 = ROOT.TH1D('threshmax250','Max pulses for 250 ns window',256,0,1280)
    threshmax300 = ROOT.TH1D('threshmax300','Max pulses for 300 ns window',256,0,1280)
    threshmax400 = ROOT.TH1D('threshmax400','Max pulses for 400 ns window',256,0,1280)
    threshmax500 = ROOT.TH1D('threshmax500','Max pulses for 500 ns window',256,0,1280)
    threshmax550 = ROOT.TH1D('threshmax550','Max pulses for 550 ns window',256,0,1280)
    nbarchunks = ROOT.TH2D('nbarchunks','Number of chan Hit vs. Time Chunk Per Event',8,0,1280,26,0,26)
    npe = ROOT.TH1D('npe','nPE',200,0,1000)
    npetime = ROOT.TH2D('npetime','nPE vs. time',256,0,1280,200,0,1000)
    npechan = ROOT.TH2D('npechan','nPE vs. chan',26,0,26,200,0,1000)
    timefitipulse = ROOT.TH1D('timefitipulse','time for Muonic Events, ipulse == 0',256,0,1280)
    ipulsemax = ROOT.TH1D('ipulsemax','Max Pulse Per Layer, ipulse == 0',256,0,1280)

    # histogram lists
    timehisto = [timefit,thresh200,thresh250,thresh300,thresh400,thresh500,thresh550,maxpulses,threshmax200,threshmax250,threshmax300,threshmax400,threshmax500,threshmax550,timefitipulse,ipulsemax]
    time_diff = [t1before,t2before,t3before,t1after,t2after,t3after]
    timechunk = [nbarchunks]
    npehist = [npe]
    npe2d = [npetime]
    npe2dchan = [npechan]
    # chanhist = [chanbefore]

    for hist in timehisto:
        hist.GetXaxis().SetTitle("Time (ns)")
    for hist in time_diff:
        hist.GetXaxis().SetTitle("Time Difference (ns)")
    for hist in timechunk:
        hist.GetXaxis().SetTitle("Time Chunk (ns)")
        hist.GetYaxis().SetTitle("Number of Chan")
    for hist in npe2d:
        hist.GetXaxis().SetTitle('Time (ns)')
        hist.GetYaxis().SetTitle('nPE')
    for hist in npe2dchan:
        hist.GetXaxis().SetTitle('chan')
        hist.GetYaxis().SetTitle('nPE')

    histograms = timehisto + time_diff + timechunk + npehist + npe2d + npe2dchan

    totalEntries = 0
    ipulseEvents = 0
    event200 = 0
    event250 = 0
    event300 = 0
    event400 = 0
    event500 = 0
    event550 = 0

    h = open("threshold_value.txt",'w')

    threshlimit = 600
    eventsrl = np.zeros(threshlimit)
    eventslr = np.zeros(threshlimit)
    eventsd = np.zeros(threshlimit)

    # time = "time"
    time = "timeFit_module_finalCalibration"

    if args.test:
        print("TESTING ", LIMIT)
    i = 0

    for data in uproot.iterate(file, var, library='ak', step_size=1000):
        if args.test:
            i += 1
            print(i)
        if i > LIMIT:
            break
        
        data["event_time_fromTDC"] = ak.broadcast_arrays(data["event_time_fromTDC"], data["timeFit_module_calibrated"])[0]
        
        timecut = (data[time] > 450) & (data[time] < 650) # masking for the desired layers
        layer0 = ((data['layer']==0) & (data['type']==0)) #& timecut
        layer1 = ((data['layer']==1) & (data['type']==0)) #& timecut
        layer2 = ((data['layer']==2) & (data['type']==0)) #& timecut
        layer3 = ((data['layer']==3) & (data['type']==0)) #& timecut
        ipulsecut = (data['ipulse'] == 0)
       
        if args.old:
            layer0 = ((data['layer']==0) & (data['type']==0)) & timecut
            layer1 = ((data['layer']==1) & (data['type']==0)) & timecut
            layer2 = ((data['layer']==2) & (data['type']==0)) & timecut
            layer3 = ((data['layer']==3) & (data['type']==0)) & timecut

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
        maskbar = maskmuon & (data["type"] == 0)
        
        ipulsedata = data[ipulsecut]
        ipulsetimecut = (ipulsedata[time] > 450) & (ipulsedata[time] < 650)
        ipulselayer0 = ((ipulsedata['layer']==0) & (ipulsedata['type']==0)) 
        ipulselayer1 = ((ipulsedata['layer']==1) & (ipulsedata['type']==0)) 
        ipulselayer2 = ((ipulsedata['layer']==2) & (ipulsedata['type']==0)) 
        ipulselayer3 = ((ipulsedata['layer']==3) & (ipulsedata['type']==0)) 
        
        if args.old:
            ipulselayer0 = ((ipulsedata['layer']==0) & (ipulsedata['type']==0)) & ipulsetimecut
            ipulselayer1 = ((ipulsedata['layer']==1) & (ipulsedata['type']==0)) & ipulsetimecut
            ipulselayer2 = ((ipulsedata['layer']==2) & (ipulsedata['type']==0)) & ipulsetimecut
            ipulselayer3 = ((ipulsedata['layer']==3) & (ipulsedata['type']==0)) & ipulsetimecut

        ipulsemask1 = ak.any(((ipulselayer0) 
                        & (ipulsedata['area']>95000*1.25)
                        ),axis=-1) & ak.any(((ipulselayer1) 
                        & (ipulsedata['area']>95000*1.25)
                        ),axis=-1) & ak.any(((ipulselayer2)
                        & (ipulsedata['area']>95000*1.25)
                        ),axis=-1) & ak.any(((ipulselayer3)
                        & (ipulsedata['area']>95000*1.25)
                        ),axis=-1) # masking for muon restrictions
        ipulsemaskmuon = ipulsemask1 & ak.any(((ipulsedata["chan"] == 16) & (ipulsedata['area']>30000*1.25)), axis=-1) & ak.any(((ipulsedata["chan"] == 18) & (ipulsedata['area']>18000*1.25)), axis=-1)
        ipulsemaskbar = ipulsemaskmuon & (ipulsedata["type"] == 0)

        data = data[maskbar]
        ipulsedata = ipulsedata[ipulsemaskbar]

        muondata = data

        # max pulse in each layer
        maskmuon0 = data['layer']==0 
        maskmuon1 = data['layer']==1
        maskmuon2 = data['layer']==2
        maskmuon3 = data['layer']==3
        muon0 = data[maskmuon0]
        muon1 = data[maskmuon1]
        muon2 = data[maskmuon2]
        muon3 = data[maskmuon3]
        max_muon0 = ak.where(muon0['area'] == ak.max(muon0['area'],axis=-1),True,False)
        max_muon1 = ak.where(muon1['area'] == ak.max(muon1['area'],axis=-1),True,False)
        max_muon2 = ak.where(muon2['area'] == ak.max(muon2['area'],axis=-1),True,False)
        max_muon3 = ak.where(muon3['area'] == ak.max(muon3['area'],axis=-1),True,False)
        max_muondata0 = muon0[max_muon0]
        max_muondata1 = muon1[max_muon1]
        max_muondata2 = muon2[max_muon2]
        max_muondata3 = muon3[max_muon3]

        # max pulse in each ipulse == 0 layer
        imaskmuon0 = ipulsedata['layer']==0 
        imaskmuon1 = ipulsedata['layer']==1
        imaskmuon2 = ipulsedata['layer']==2
        imaskmuon3 = ipulsedata['layer']==3
        imuon0 = ipulsedata[imaskmuon0]
        imuon1 = ipulsedata[imaskmuon1]
        imuon2 = ipulsedata[imaskmuon2]
        imuon3 = ipulsedata[imaskmuon3]
        imax_muon0 = ak.where(imuon0['area'] == ak.max(imuon0['area'],axis=-1),True,False)
        imax_muon1 = ak.where(imuon1['area'] == ak.max(imuon1['area'],axis=-1),True,False)
        imax_muon2 = ak.where(imuon2['area'] == ak.max(imuon2['area'],axis=-1),True,False)
        imax_muon3 = ak.where(imuon3['area'] == ak.max(imuon3['area'],axis=-1),True,False)
        imax_muondata0 = imuon0[imax_muon0]
        imax_muondata1 = imuon1[imax_muon1]
        imax_muondata2 = imuon2[imax_muon2]
        imax_muondata3 = imuon3[imax_muon3]

        # plotting time of max pulse of each layer
        maxes = ak.concatenate([max_muondata0[time],max_muondata1[time],max_muondata2[time],max_muondata3[time]],axis=-1)
        plot1D(maxes,maxpulses)

        # plotting time of max pulse of each layer for ipulse == 0
        imaxes = ak.concatenate([imax_muondata0[time],imax_muondata1[time],imax_muondata2[time],imax_muondata3[time]],axis=-1)
        plot1D(imaxes,ipulsemax)

        # initializing array for which channels get hits in certain time chunks
        chunks = np.linspace(0,1280,9)

        # function to plot the chan vs time chunks
        def timeChunks():
            for j in range(len(chunks)-1):
                mask = (data[time] > chunks[j]) & (data[time] < chunks[j+1])
                chanchunk = data[mask]
                nbars = ak.count(ak.run_lengths(chanchunk['chan']),axis=-1,mask_identity=True)
                timechunk = ak.broadcast_arrays(chunks[j], nbars)[0]
                plot2D(timechunk,nbars,nbarchunks)

        # function to count up valid events
        def nonempty_events(muontime):
            return ak.sum(ak.any(muontime > 0,axis=-1))
        
        # veto functions do the threshold masking without counting up the events, threshold function count them up
        # these functions aren't really used anyway
        def vetorl(width,offset):
            mask = ak.any((data[time] < offset) & (data[time] > (offset-width)),axis=-1)
            threshdata = data[~mask]
            # events[width] += nonempty_events(threshdata['timeFit_module_finalCalibration'])
            return threshdata
        
        def thresholdrl(width,offset):
            mask = ak.any((data[time] < (offset)) & (data[time] > (offset-width)),axis=-1)
            threshdata = data[~mask]
            eventsrl[width] += nonempty_events(threshdata[time])
            return threshdata
        
        def vetolr(width,offset):
            mask = ak.any((data[time] < (width+offset)) & (data[time] > offset),axis=-1)
            threshdata = data[~mask]
            # events[width] += nonempty_events(threshdata['timeFit_module_finalCalibration'])
            return threshdata
        
        def thresholdlr(width,offset):
            mask = ak.any((data[time] < (width+offset)) & (data[time] > offset),axis=-1)
            threshdata = data[~mask]
            eventslr[width] += nonempty_events(threshdata[time])
            return threshdata
        
        # efficiencies right to left
        if args.rl:
            totalEntriesrl = 0
            dt = 450 - data[time]  # t0 broadcast as before

            # For each event, the closest pulse to the LEFT of t0
            closest_pre = ak.min(ak.where(dt >= 0, dt, np.inf), axis=-1, initial=np.inf)

            valid_events = ak.any(data[time] > 0, axis=-1)
            closest_pre_valid = ak.to_numpy(closest_pre[valid_events])

            thresholds = np.arange(threshlimit)

            # Event survives if no pulse landed within [t0-T, t0], i.e. closest_pre > T
            survives = closest_pre_valid[:, np.newaxis] > thresholds
            eventsrl += survives.sum(axis=0)
            totalEntriesrl += nonempty_events(muondata[time])

        # efficiencies left to right        
        if args.lr:
            totalEntrieslr = 0
            dt = data[time] - 100  # t0 should be broadcast like mintime was

            # For each event, the closest pulse to the RIGHT of t0
            closest_post = ak.min(ak.where(dt >= 0, dt, np.inf), axis=-1, initial=np.inf)

            valid_events = ak.any(data[time] > 0, axis=-1)
            closest_post_valid = ak.to_numpy(closest_post[valid_events])

            thresholds = np.arange(threshlimit)

            # Event survives if no pulse landed within [t0, t0+T], i.e. closest_post > T
            survives = closest_post_valid[:, np.newaxis] > thresholds
            eventslr += survives.sum(axis=0)
            totalEntrieslr += nonempty_events(muondata[time])

        # efficiencies for dynamic veto method
        if args.d:
            # t1 = max_muondata1[time] - max_muondata0[time]
            # t2 = max_muondata2[time] - max_muondata1[time]
            # t3 = max_muondata3[time] - max_muondata2[time]
            # timemask1 = ak.all(abs(t1) <= 25,axis=-1)
            # timemask2 = ak.all(abs(t2) <= 25,axis=-1)
            # timemask3 = ak.all(abs(t3) <= 25,axis=-1)
            # totaltimemask = timemask1 & timemask2 & timemask3
            dynamicdata = data

            # maskmuon0 = dynamicdata['layer']==0 
            # maskmuon1 = dynamicdata['layer']==1
            # maskmuon2 = dynamicdata['layer']==2
            # maskmuon3 = dynamicdata['layer']==3
            # muon0 = dynamicdata[maskmuon0]
            # muon1 = dynamicdata[maskmuon1]
            # muon2 = dynamicdata[maskmuon2]
            # muon3 = dynamicdata[maskmuon3]

            # max_muon0 = ak.where(muon0['area'] == ak.max(muon0['area'],axis=-1),True,False)
            # max_muon1 = ak.where(muon1['area'] == ak.max(muon1['area'],axis=-1),True,False)
            # max_muon2 = ak.where(muon2['area'] == ak.max(muon2['area'],axis=-1),True,False)
            # max_muon3 = ak.where(muon3['area'] == ak.max(muon3['area'],axis=-1),True,False)
            # max_muondata0 = muon0[max_muon0]
            # max_muondata1 = muon1[max_muon1]
            # max_muondata2 = muon2[max_muon2]
            # max_muondata3 = muon3[max_muon3]

            # times = ak.concatenate([max_muondata0[time],max_muondata1[time],max_muondata2[time],max_muondata3[time]],axis=-1)
            mintime_before = ak.min(maxes,axis=-1) - 20

            totalEntriesd = 0
            dt = mintime_before - dynamicdata[time]  # mintime already broadcast
            pretrigger_dt = ak.where((dt > 0), dt, np.inf)  # only care about pulses BEFORE mintime

            # For each event, the closest pretrigger pulse distance
            closest_pre = ak.min(pretrigger_dt, axis=-1, initial=np.inf)  # shape: (n_events,)

            # An event is VETOED at threshold T if closest_pre <= T
            # An event SURVIVES if closest_pre > T (or no pretrigger pulse exists -> inf > T always)
            valid_events = ak.any(dynamicdata[time] > 0, axis=-1)
            closest_pre_valid = ak.to_numpy(closest_pre[valid_events])

            thresholds = np.arange(threshlimit)  # shape: (600,)

            # Broadcasting: (n_events, 1) > (600,) -> (n_events, 600) boolean, then sum over events
            survives = closest_pre_valid[:, np.newaxis] > thresholds  # shape: (n_events, 600)
            eventsd += survives.sum(axis=0)
            totalEntriesd += nonempty_events(dynamicdata[time])

        timeChunks()

        # counting up muon events and ipulse events to get efficiency
        ipulseEvents += nonempty_events(ipulsedata[time])
        totalEntries += nonempty_events(muondata[time])
        
        mask450 = (data[time] > 0) & (data[time] < 450)
        data450 = data[mask450]
        
        plot1D(muondata[time],timefit)
        # plot1D(veto(200)[time],thresh200)
        # plot1D(veto(250)[time],thresh250)
        # plot1D(veto(300)[time],thresh300)
        # plot1D(veto(400)[time],thresh400)
        # plot1D(veto(500)[time],thresh500)
        # plot1D(veto(550)[time],thresh550)
        
        plot1D(ipulsedata[time],timefitipulse)

        plot1D(muondata['nPE'],npe)
        plot2D(muondata[time],muondata['nPE'],npetime)
        plot2D(data450['chan'],data450['nPE'],npechan)

    totalEntriesrl = eventsrl[0]
    totalEntrieslr = eventslr[0]
    totalEntriesd = eventsd[0]
        
    for j in range(threshlimit):
        h.write(f"\n{j}")
        
    if args.rl:
        efficiencyrl = eventsrl/totalEntriesrl

        g = open("threshold_efficiency_rl.txt",'w')

        for j in range(threshlimit):
            g.write(f"\n{efficiencyrl[j]}")

        g.close()
    if args.lr:
        efficiencylr = eventslr/totalEntrieslr
        derivative = np.gradient(efficiencylr)

        o = open("threshold_efficiency_lr.txt",'w')
        k = open("threshold_derivative.txt",'w')

        for j in range(threshlimit):
            o.write(f"\n{efficiencylr[j]}")
            k.write(f"\n{derivative[j]}")

        o.close()
        k.close()
    if args.d:
        efficiencyd = eventsd/totalEntriesd

        q = open("threshold_efficiency_d.txt",'w')

        for j in range(threshlimit):
            q.write(f"\n{efficiencyd[j]}")

        q.close()

    canvas = ROOT.TCanvas("canvas")
    canvas.Print("threshold.pdf[")
    timefit.Draw()
    canvas.Print("threshold.pdf")

    def thresholdRatio(hist,left,right):
        hist.Draw()
        ymin = gPad.GetUymin()
        ymax = gPad.GetUymax()
        l = ROOT.TLine(left,ymin,left,ymax)
        l.SetLineColor(ROOT.kRed)
        l.SetLineStyle(9)
        l.Draw("same")
        l = ROOT.TLine(right,ymin,right,ymax)
        l.SetLineColor(ROOT.kRed)
        l.SetLineStyle(9)
        l.Draw("same")
        gPad.Update()
        canvas.Print("threshold.pdf")

    h.close()

    canvas.Print("threshold.pdf]")
    canvas.Close()

    comparison("ipulsecanvas","ipulse_comparison.pdf",timefit,timefitipulse)
    comparison("imax","ipulsemax_comparison.pdf",maxpulses,ipulsemax)
    
    if args.old:
        m = open('ipulse_efficiency_old.txt','w')
    if not args.old:
        m = open('ipulse_efficiency.txt','w')
    ipulseeff = ipulseEvents/totalEntries
    print("ipulse efficiency: ",ipulseeff)
    m.write(f"\n{ipulseeff}")
    m.close()

    for hist in histograms:
        hist.Write()

    output.Close()

if __name__ == "__main__":
    main()