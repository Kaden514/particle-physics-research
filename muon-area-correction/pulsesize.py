# IMPORTANT:
# The pulse per channel vs channel histograms, the per channel heatmaps, and the max pulse per layer heatmap take a while for the code to process
# so if you want to plot the per channel stuff, add --chan to the run command line, and if you want the per layer heatmap, add --heatmap
# otherwise, just run it as is to save time

import awkward as ak
import uproot
import ROOT
from array import array
from ROOT import TLegend
import argparse


def main():
    parser = argparse.ArgumentParser(description="Choose if you want to execute the particularly time-consuming parts of code. Don't add any flags if you don't need the optional parts.")
    parser.add_argument("--chan",action="store_true", help="Plot the per channel histograms and heatmaps")
    parser.add_argument("--heatmap",action="store_true",help="Plot the max pulse per layer heatmap")
    args = parser.parse_args()

    # change file directory as needed
    file = 'file directory taken out from original version for proprietary reasons'
    var = ["timeFit_module_calibrated", 'time', "chan", "layer", "event_time_fromTDC", "area", "ipulse", "energy", "type", "height", "duration", "row", "column"]

    ROOT.gStyle.SetOptStat(0)

    output = ROOT.TFile('pulsesize.root','RECREATE') # output file
    side1 = ROOT.TH1D('side1','side panel 24 area', 100, 0, 1000)
    side1.GetXaxis().SetTitle("Area")
    side2 = ROOT.TH1D('side2','side panel 25 area', 100, 0, 1000)
    side2.GetXaxis().SetTitle("Area")
    front = ROOT.TH1D('front','front panel area', 100, 25000, 80000)
    front.GetXaxis().SetTitle("Area")
    back = ROOT.TH1D('back','back panel area', 100, 15000, 80000)
    back.GetXaxis().SetTitle("Area")
    column0 = ROOT.TH1D('column0','column 0 area', 200, 90000, 200000)
    column0.GetXaxis().SetTitle("Area")
    column1 = ROOT.TH1D('column1','column 1 area', 200, 90000, 200000)
    column1.GetXaxis().SetTitle("Area")
    muon = ROOT.TH1D('muon','bars being hit', 20, 0, 20)
    muon.GetXaxis().SetTitle("nbars")
    column0chan = ROOT.TH2D('column0chan','Column0 Area vs. Channel', 26, 0, 26, 100, 90000, 200000)
    column0chan.GetXaxis().SetTitle("chan")
    column0chan.GetYaxis().SetTitle("Area")
    column1chan = ROOT.TH2D('column1chan','Column1 Area vs. Channel',26,0,26,100,90000,200000)
    column1chan.GetXaxis().SetTitle("chan")
    column1chan.GetYaxis().SetTitle("Area")
    channelarea = ROOT.TH2D('channelarea','Max Pulse per Channel vs. Channel',30,0,30,100,0,200000)
    channelarea.GetXaxis().SetTitle("chan")
    channelarea.GetYaxis().SetTitle("Area")
    channelpulse = ROOT.TH2D('channelpulse','First Pulse per Channel vs. Channel',30,0,30,100,0,200000)
    channelpulse.GetXaxis().SetTitle('chan')
    channelpulse.GetYaxis().SetTitle('Area')

    chan0 = ROOT.TH1D('chan0','chan0 Max Area',200,90000,160000)
    chan0.GetXaxis().SetTitle("Area")
    chan1 = ROOT.TH1D('chan1','chan1 Max Area',200,90000,160000)
    chan1.GetXaxis().SetTitle("Area")
    chan2 = ROOT.TH1D('chan2','chan2 Max Area',200,90000,160000)
    chan2.GetXaxis().SetTitle("Area")
    chan3 = ROOT.TH1D('chan3','chan3 Max Area',200,90000,160000)
    chan4 = ROOT.TH1D('chan4','chan4 Max Area',200,90000,160000)
    chan5 = ROOT.TH1D('chan5','chan5 Max Area',200,90000,160000)
    chan6 = ROOT.TH1D('chan6','chan6 Max Area',200,90000,160000)
    chan7 = ROOT.TH1D('chan7','chan7 Max Area',200,90000,160000)
    chan8 = ROOT.TH1D('chan8','chan8 Max Area',200,90000,160000)
    chan9 = ROOT.TH1D('chan9','chan9 Max Area',200,90000,160000)
    chan10 = ROOT.TH1D('chan10','chan10 Max Area',200,90000,160000)
    chan11 = ROOT.TH1D('chan11','chan11 Max Area',200,90000,160000)
    chan12 = ROOT.TH1D('chan12','chan12 Max Area',200,90000,160000)
    chan14 = ROOT.TH1D('chan14','chan14 Max Area',200,90000,160000)
    chan20 = ROOT.TH1D('chan20','chan20 Max Area',200,90000,160000)
    chan22 = ROOT.TH1D('chan22','chan22 Max Area',200,90000,160000)
    chan3.GetXaxis().SetTitle("Area")
    chan4.GetXaxis().SetTitle("Area")
    chan5.GetXaxis().SetTitle("Area")
    chan6.GetXaxis().SetTitle("Area")
    chan7.GetXaxis().SetTitle("Area")
    chan8.GetXaxis().SetTitle("Area")
    chan9.GetXaxis().SetTitle("Area")
    chan10.GetXaxis().SetTitle("Area")
    chan11.GetXaxis().SetTitle("Area")
    chan12.GetXaxis().SetTitle("Area")
    chan14.GetXaxis().SetTitle("Area")
    chan20.GetXaxis().SetTitle("Area")
    chan22.GetXaxis().SetTitle("Area")

    chanp0 = ROOT.TH1D('chanp0','chan0 First Pulse Area',500,90000,160000)
    chanp0.GetXaxis().SetTitle("Area")
    chanp1 = ROOT.TH1D('chanp1','chan1 First Pulse Area',500,90000,160000)
    chanp1.GetXaxis().SetTitle("Area")
    chanp2 = ROOT.TH1D('chanp2','chan2 First Pulse Area',500,90000,160000)
    chanp2.GetXaxis().SetTitle("Area")
    chanp3 = ROOT.TH1D('chanp3','chan3 First Pulse Area',500,90000,160000)
    chanp3.GetXaxis().SetTitle("Area")
    chanp4 = ROOT.TH1D('chanp4','chan4 First Pulse Area',500,90000,160000)
    chanp4.GetXaxis().SetTitle("Area")
    chanp5 = ROOT.TH1D('chanp5','chan5 First Pulse Area',500,90000,160000)
    chanp5.GetXaxis().SetTitle("Area")
    chanp6 = ROOT.TH1D('chanp6','chan6 First Pulse Area',500,90000,160000)
    chanp6.GetXaxis().SetTitle("Area")
    chanp7 = ROOT.TH1D('chanp7','chan7 First Pulse Area',500,90000,160000)
    chanp7.GetXaxis().SetTitle("Area")
    chanp8 = ROOT.TH1D('chanp8','chan8 First Pulse Area',500,90000,160000)
    chanp8.GetXaxis().SetTitle("Area")
    chanp9 = ROOT.TH1D('chanp9','chan9 First Pulse Area',500,90000,160000)
    chanp9.GetXaxis().SetTitle("Area")
    chanp10 = ROOT.TH1D('chanp10','chan10 First Pulse Area',500,90000,160000)
    chanp10.GetXaxis().SetTitle("Area")
    chanp11 = ROOT.TH1D('chanp11','chan11 First Pulse Area',500,90000,160000)
    chanp11.GetXaxis().SetTitle("Area")
    chanp12 = ROOT.TH1D('chanp12','chan12 First Pulse Area',500,90000,160000)
    chanp12.GetXaxis().SetTitle("Area")
    chanp14 = ROOT.TH1D('chanp14','chan14 First Pulse Area',500,90000,160000)
    chanp14.GetXaxis().SetTitle("Area")
    chanp20 = ROOT.TH1D('chanp20','chan20 First Pulse Area',500,90000,160000)
    chanp20.GetXaxis().SetTitle("Area")
    chanp22 = ROOT.TH1D('chanp22','chan22 First Pulse Area',500,90000,160000)
    chanp22.GetXaxis().SetTitle("Area")

    chanpc0 = ROOT.TH1D('chanpc0','chan0 First Pulse Corrected Area',500,90000,160000)
    chanpc0.GetXaxis().SetTitle("Area")
    chanpc1 = ROOT.TH1D('chanpc1','chan1 First Pulse Corrected Area',500,90000,160000)
    chanpc1.GetXaxis().SetTitle("Area")
    chanpc2 = ROOT.TH1D('chanpc2','chan2 First Pulse Corrected Area',500,90000,160000)
    chanpc2.GetXaxis().SetTitle("Area")
    chanpc3 = ROOT.TH1D('chanpc3','chan3 First Pulse Corrected Area',500,90000,160000)
    chanpc3.GetXaxis().SetTitle("Area")
    chanpc4 = ROOT.TH1D('chanpc4','chan4 First Pulse Corrected Area',500,90000,160000)
    chanpc4.GetXaxis().SetTitle("Area")
    chanpc5 = ROOT.TH1D('chanpc5','chan5 First Pulse Corrected Area',500,90000,160000)
    chanpc5.GetXaxis().SetTitle("Area")
    chanpc6 = ROOT.TH1D('chanpc6','chan6 First Pulse Corrected Area',500,90000,160000)
    chanpc6.GetXaxis().SetTitle("Area")
    chanpc7 = ROOT.TH1D('chanpc7','chan7 First Pulse Corrected Area',500,90000,160000)
    chanpc7.GetXaxis().SetTitle("Area")
    chanpc8 = ROOT.TH1D('chanpc8','chan8 First Pulse Corrected Area',500,90000,160000)
    chanpc8.GetXaxis().SetTitle("Area")
    chanpc9 = ROOT.TH1D('chanpc9','chan9 First Pulse Corrected Area',500,90000,160000)
    chanpc9.GetXaxis().SetTitle("Area")
    chanpc10 = ROOT.TH1D('chanpc10','chan10 First Pulse Corrected Area',500,90000,160000)
    chanpc10.GetXaxis().SetTitle("Area")
    chanpc11 = ROOT.TH1D('chanpc11','chan11 First Pulse Corrected Area',500,90000,160000)
    chanpc11.GetXaxis().SetTitle("Area")
    chanpc12 = ROOT.TH1D('chanpc12','chan12 First Pulse Corrected Area',500,90000,160000)
    chanpc12.GetXaxis().SetTitle("Area")
    chanpc14 = ROOT.TH1D('chanpc14','chan14 First Pulse Corrected Area',500,90000,160000)
    chanpc14.GetXaxis().SetTitle("Area")
    chanpc20 = ROOT.TH1D('chanpc20','chan20 First Pulse Corrected Area',500,90000,160000)
    chanpc20.GetXaxis().SetTitle("Area")
    chanpc22 = ROOT.TH1D('chanpc22','chan22 First Pulse Corrected Area',500,90000,160000)
    chanpc22.GetXaxis().SetTitle("Area")

    hd0 = ROOT.TH2D('hd0','chan0 Height vs. Duration',100,0,500,100,1100,1300)
    hd1 = ROOT.TH2D('hd1','chan1 Height vs. Duration',100,0,500,100,1100,1300)
    hd2 = ROOT.TH2D('hd2','chan2 Height vs. Duration',100,0,500,100,1100,1300)
    hd3 = ROOT.TH2D('hd3','chan3 Height vs. Duration',100,0,500,100,1100,1300)
    hd4 = ROOT.TH2D('hd4','chan4 Height vs. Duration',100,0,500,100,1100,1300)
    hd5 = ROOT.TH2D('hd5','chan5 Height vs. Duration',100,0,500,100,1100,1300)
    hd6 = ROOT.TH2D('hd6','chan6 Height vs. Duration',100,0,500,100,1100,1300)
    hd7 = ROOT.TH2D('hd7','chan7 Height vs. Duration',100,0,500,100,1100,1300)
    hd8 = ROOT.TH2D('hd8','chan8 Height vs. Duration',100,0,500,100,1100,1300)
    hd9 = ROOT.TH2D('hd9','chan9 Height vs. Duration',100,0,500,100,1100,1300)
    hd10 = ROOT.TH2D('hd10','chan10 Height vs. Duration',100,0,500,100,1100,1300)
    hd11 = ROOT.TH2D('hd11','chan11 Height vs. Duration',100,0,500,100,1100,1300)
    hd12 = ROOT.TH2D('hd12','chan12 Height vs. Duration',100,0,500,100,1100,1300)
    hd14 = ROOT.TH2D('hd14','chan14 Height vs. Duration',100,0,500,100,1100,1300)
    hd20 = ROOT.TH2D('hd20','chan20 Height vs. Duration',100,0,500,100,1100,1300)
    hd22 = ROOT.TH2D('hd22','chan22 Height vs. Duration',100,0,500,100,1100,1300)
    hd0.GetXaxis().SetTitle("Duration")
    hd0.GetYaxis().SetTitle("Height")
    hd1.GetXaxis().SetTitle("Duration")
    hd1.GetYaxis().SetTitle("Height")
    hd2.GetXaxis().SetTitle("Duration")
    hd2.GetYaxis().SetTitle("Height")
    hd3.GetXaxis().SetTitle("Duration")
    hd3.GetYaxis().SetTitle("Height")
    hd4.GetXaxis().SetTitle("Duration")
    hd4.GetYaxis().SetTitle("Height")
    hd5.GetXaxis().SetTitle("Duration")
    hd5.GetYaxis().SetTitle("Height")
    hd6.GetXaxis().SetTitle("Duration")
    hd6.GetYaxis().SetTitle("Height")
    hd7.GetXaxis().SetTitle("Duration")
    hd7.GetYaxis().SetTitle("Height")
    hd8.GetXaxis().SetTitle("Duration")
    hd8.GetYaxis().SetTitle("Height")
    hd9.GetXaxis().SetTitle("Duration")
    hd9.GetYaxis().SetTitle("Height")
    hd10.GetXaxis().SetTitle("Duration")
    hd10.GetYaxis().SetTitle("Height")
    hd11.GetXaxis().SetTitle("Duration")
    hd11.GetYaxis().SetTitle("Height")
    hd12.GetXaxis().SetTitle("Duration")
    hd12.GetYaxis().SetTitle("Height")
    hd14.GetXaxis().SetTitle("Duration")
    hd14.GetYaxis().SetTitle("Height")
    hd20.GetXaxis().SetTitle("Duration")
    hd20.GetYaxis().SetTitle("Height")
    hd22.GetXaxis().SetTitle("Duration")
    hd22.GetYaxis().SetTitle("Height")

    hdp0 = ROOT.TH2D('hdp0','chan0 Height vs. Duration',100,0,500,100,0,1300)
    hdp0.GetXaxis().SetTitle("Duration")
    hdp0.GetYaxis().SetTitle("Height")
    hdp1 = ROOT.TH2D('hdp1','chan1 Height vs. Duration',100,0,500,100,0,1300)
    hdp1.GetXaxis().SetTitle("Duration")
    hdp1.GetYaxis().SetTitle("Height")
    hdp2 = ROOT.TH2D('hdp2','chan2 Height vs. Duration',100,0,500,100,0,1300)
    hdp2.GetXaxis().SetTitle("Duration")
    hdp2.GetYaxis().SetTitle("Height")
    hdp3 = ROOT.TH2D('hdp3','chan3 Height vs. Duration',100,0,500,100,0,1300)
    hdp3.GetXaxis().SetTitle("Duration")
    hdp3.GetYaxis().SetTitle("Height")
    hdp4 = ROOT.TH2D('hdp4','chan4 Height vs. Duration',100,0,500,100,0,1300)
    hdp4.GetXaxis().SetTitle("Duration")
    hdp4.GetYaxis().SetTitle("Height")
    hdp5 = ROOT.TH2D('hdp5','chan5 Height vs. Duration',100,0,500,100,0,1300)
    hdp5.GetXaxis().SetTitle("Duration")
    hdp5.GetYaxis().SetTitle("Height")
    hdp6 = ROOT.TH2D('hdp6','chan6 Height vs. Duration',100,0,500,100,0,1300)
    hdp6.GetXaxis().SetTitle("Duration")
    hdp6.GetYaxis().SetTitle("Height")
    hdp7 = ROOT.TH2D('hdp7','chan7 Height vs. Duration',100,0,500,100,0,1300)
    hdp7.GetXaxis().SetTitle("Duration")
    hdp7.GetYaxis().SetTitle("Height")
    hdp8 = ROOT.TH2D('hdp8','chan8 Height vs. Duration',100,0,500,100,0,1300)
    hdp8.GetXaxis().SetTitle("Duration")
    hdp8.GetYaxis().SetTitle("Height")
    hdp9 = ROOT.TH2D('hdp9','chan9 Height vs. Duration',100,0,500,100,0,1300)
    hdp9.GetXaxis().SetTitle("Duration")
    hdp9.GetYaxis().SetTitle("Height")
    hdp10 = ROOT.TH2D('hdp10','chan10 Height vs. Duration',100,0,500,100,0,1300)
    hdp10.GetXaxis().SetTitle("Duration")
    hdp10.GetYaxis().SetTitle("Height")
    hdp11 = ROOT.TH2D('hdp11','chan11 Height vs. Duration',100,0,500,100,0,1300)
    hdp11.GetXaxis().SetTitle("Duration")
    hdp11.GetYaxis().SetTitle("Height")
    hdp12 = ROOT.TH2D('hdp12','chan12 Height vs. Duration',100,0,500,100,0,1300)
    hdp12.GetXaxis().SetTitle("Duration")
    hdp12.GetYaxis().SetTitle("Height")
    hdp14 = ROOT.TH2D('hdp14','chan14 Height vs. Duration',100,0,500,100,0,1300)
    hdp14.GetXaxis().SetTitle("Duration")
    hdp14.GetYaxis().SetTitle("Height")
    hdp20 = ROOT.TH2D('hdp20','chan20 Height vs. Duration',100,0,500,100,0,1300)
    hdp20.GetXaxis().SetTitle("Duration")
    hdp20.GetYaxis().SetTitle("Height")
    hdp22 = ROOT.TH2D('hdp22','chan22 Height vs. Duration',100,0,500,100,0,1300)
    hdp22.GetXaxis().SetTitle("Duration")
    hdp22.GetYaxis().SetTitle("Height")

    heatchan = ROOT.TH2D('heatchan','Heatmap of Max Area Pulse per Channel',15,-3,12,15,-2,13)
    heatlayer = ROOT.TH2D('heatlayer','Heatmap of Max Area Pulse per Layer',15,-3,12,15,-2,13)
    heatchanpulse = ROOT.TH2D('heatchanpulse','Heatmap of First Pulse Area per Channel',15,-3,12,15,-2,13)
    heatlayerpulse = ROOT.TH2D('heatlayerpulse','Heatmap of First Pulse Area per Layer',15,-3,12,15,-2,13)
    heatevent = ROOT.TH2D('heatevent','Heatmap of Max Area Pulse per Event',15,-3,12,15,-2,13)
    heateventcorrected = ROOT.TH2D('heateventcorrected','Heatmap of Corrected Max Area Pulse per Event',15,-3,12,15,-2,13)

    column0pulse = ROOT.TH1D('column0pulse','column 0 area', 200, 90000, 200000)
    column0pulse.GetXaxis().SetTitle("Area")
    column1pulse = ROOT.TH1D('column1pulse','column 1 area', 200, 90000, 200000)
    column1pulse.GetXaxis().SetTitle("Area")
    column0pulsechan = ROOT.TH2D('column0pulsechan','Column0 Area vs. Channel',26, 0, 26, 100, 90000, 200000)
    column0pulsechan.GetXaxis().SetTitle("chan")
    column0pulsechan.GetYaxis().SetTitle("Area")
    column1pulsechan = ROOT.TH2D('column1pulsechan','Column1 Area vs. Channel',26,0,26,100,90000,200000)
    column1pulsechan.GetXaxis().SetTitle("chan")
    column1pulsechan.GetYaxis().SetTitle("Area")

    area0 = 99917.8 
    max0 = area0/99917.8 
    max1 = area0/102217 
    max2 = area0/98543.7 
    max3 = area0/109589 
    max4 = area0/105813 
    max5 = area0/104315 
    max6 = area0/101233 
    max7 = area0/114857 
    max8 = area0/112700 
    max9 = area0/106996 
    max10 = area0/112370 
    max11 = area0/113376 
    max12 = area0/111275 
    max14 = area0/99976.9 
    max20 = area0/119701 
    max22 = area0/112206 

    params = {0: max0, 1: max1, 2: max2, 3: max3, 4: max4, 5: max5, 6: max6, 7: max7, 8: max8, 9: max9, 10: max10, 11: max11, 12: max12, 13: 1, 14: max14, 15: 1, 16: 1, 17: 1,
                18: 1, 19: 1, 20: max20, 21: 1, 22: max22, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1,  31: 1}

    i = 0
    LIMIT = 100
    print("TESTING ", LIMIT)
    for data in uproot.iterate(file, var, library='ak', step_size=1000):
        i += 1
        if i > LIMIT:
            break

        data["event_time_fromTDC"] = ak.broadcast_arrays(data["event_time_fromTDC"], data["timeFit_module_calibrated"])[0]
        
        timecut = (data['time'] < 600) & (data['time'] > 400) # masking for the desired layers
        layer0 = ((data['layer']==0) & (data['type']==0))
        layer1 = ((data['layer']==1) & (data['type']==0))
        layer2 = ((data['layer']==2) & (data['type']==0))
        layer3 = ((data['layer']==3) & (data['type']==0))
        
        chanflat = ak.flatten(data['chan']) # applying area ratio corrections
        area_corrections = ak.unflatten([params[int(ch)] for ch in chanflat], ak.num(data['chan']))
        data['corrected_area'] = data['area']*area_corrections

        mask1 = ak.any(((layer0) & (timecut) 
                        & (data['area']>95000)
                        ),axis=-1) & ak.any(((layer1) & (timecut) 
                        & (data['area']>95000)
                        ),axis=-1) & ak.any(((layer2) & (timecut) 
                        & (data['area']>95000)
                        ),axis=-1) & ak.any(((layer3) & (timecut) 
                        & (data['area']>95000)
                        ),axis=-1) # masking for muon restrictions
        maskmuon = mask1 & ak.any(((data["chan"] == 16) & (timecut) & (data['area']>30000)), axis=-1) & ak.any(((data["chan"] == 18) & (timecut) & (data['area']>18000)), axis=-1)
        
        maskside1 = (maskmuon) & (data['chan'] == 24) & (data['ipulse'] == 0) #masks for events in side panels only
        maskside2 = (maskmuon) & (data['chan'] == 25) & (data['ipulse'] == 0)
        maskfront = (maskmuon) & (data['chan'] == 16) & (data['ipulse'] == 0) # masks for events in front and back panels
        maskback = (maskmuon) & (data['chan'] == 18) & (data['ipulse'] == 0)
        maskbar = (maskmuon) & (data['type'] == 0) & (data['ipulse'] == 0) # masks for events in bars only and ipulse == 0
        maskcolumn = (maskmuon) & (data['type'] == 0) # mask for events in bars only, no ipulse mask to prepare for max area masking
        muonpulse = (maskmuon) & (data['ipulse'] == 0) # mask for ipulse == 0 in all channels

        sidedata1 = data[maskside1]
        sidedata2 = data[maskside2]
        frontdata = data[maskfront]
        backdata = data[maskback]
        muondata = data[maskbar]
        testmuon = data[maskcolumn]
        testthru = data[mask1]
        muonarea = data[maskmuon]
        pulsedata = data[muonpulse]

        max_muon = ak.where(testmuon['area']==ak.max(testmuon['area'],axis=-1),True,False)
        testmuon = testmuon[max_muon]

        maskcolumn0 = (testmuon['column'] == 0)
        maskcolumn1 = (testmuon['column'] == 1)
        columndata0 = testmuon[maskcolumn0]
        columndata1 = testmuon[maskcolumn1]

        maskcolumnpulse0 = (muondata['column'] == 0)
        maskcolumnpulse1 = (muondata['column'] == 1)
        columnpulsedata0 = muondata[maskcolumnpulse0]
        columnpulsedata1 = muondata[maskcolumnpulse1]

        # function to expedite all the chan plots
        def chanhist(j,hist,hist2d,pulse,pulse2d,pulsecor):
            chanmask = (testmuon['chan'] == j) 
            chanpulse = (muondata['chan'] == j)
            chandata = testmuon[chanmask]
            pulsedata = muondata[chanpulse]
            flat_chan = ak.flatten(chandata['area'],axis=None)
            flat_height = ak.flatten(chandata['height'],axis=None)
            flat_duration = ak.flatten(chandata['duration'],axis=None)
            flat_pulse = ak.flatten(pulsedata['area'],axis=None)
            flat_pulse_corrected = ak.flatten(pulsedata['corrected_area'],axis=None)
            flat_hpulse = ak.flatten(pulsedata['height'],axis=None)
            flat_dpulse = ak.flatten(pulsedata['duration'],axis=None)
            n_events9 = len(flat_chan)
            n_eventsd = len(flat_duration)
            n_eventsh = len(flat_height)
            n_events13 = len(flat_pulse)
            n_eventsph = len(flat_hpulse)
            n_eventscor = len(flat_pulse_corrected)
            weight9 = ak.ones_like(flat_chan)
            weightd = ak.ones_like(flat_duration)
            weighth = ak.ones_like(flat_height)
            weight13 = ak.ones_like(flat_pulse)
            weightph = ak.ones_like(flat_hpulse)
            weightcor = ak.ones_like(flat_pulse_corrected)
            if n_events9 > 0:
                hist.FillN(n_events9, array('d',flat_chan), array('d',weight9),1)
            if n_eventsh > 0:
                hist2d.FillN(n_eventsh, array('d',flat_duration), array('d',flat_height), array('d',weighth),1)
            if n_events13 > 0:
                pulse.FillN(n_events13, array('d',flat_pulse), array('d',weight13),1)
            if n_eventsph > 0:
                pulse2d.FillN(n_eventsph, array('d',flat_dpulse), array('d',flat_hpulse), array('d',weightph),1)
            if n_eventscor > 0:
                pulsecor.FillN(n_eventscor, array('d',flat_pulse_corrected), array('d',weightcor),1)

        chanhist(0,chan0,hd0,chanp0,hdp0,chanpc0)
        chanhist(1,chan1,hd1,chanp1,hdp1,chanpc1)
        chanhist(2,chan2,hd2,chanp2,hdp2,chanpc2)
        chanhist(3,chan3,hd3,chanp3,hdp3,chanpc3)
        chanhist(4,chan4,hd4,chanp4,hdp4,chanpc4)
        chanhist(5,chan5,hd5,chanp5,hdp5,chanpc5)
        chanhist(6,chan6,hd6,chanp6,hdp6,chanpc6)
        chanhist(7,chan7,hd7,chanp7,hdp7,chanpc7)
        chanhist(8,chan8,hd8,chanp8,hdp8,chanpc8)
        chanhist(9,chan9,hd9,chanp9,hdp9,chanpc9)
        chanhist(10,chan10,hd10,chanp10,hdp10,chanpc10)
        chanhist(11,chan11,hd11,chanp11,hdp11,chanpc11)
        chanhist(12,chan12,hd12,chanp12,hdp12,chanpc12)
        chanhist(14,chan14,hd14,chanp14,hdp14,chanpc14)
        chanhist(20,chan20,hd20,chanp20,hdp20,chanpc20)
        chanhist(22,chan22,hd22,chanp22,hdp22,chanpc22)
        
        # setting up max pulse per channel
        def maxchan():
            for j in range(30):
                temp_maxPerLayerMask0 = ((muonarea['area']==ak.max(muonarea['area'][(muonarea['chan']==j)], keepdims=True, axis=-1)))
                maxchannel = muonarea[temp_maxPerLayerMask0]
                temp_maxPerLayerMask0 = maxchannel['area'] > 95000
                maxchannel = maxchannel[temp_maxPerLayerMask0]
                pulsechanmask = (pulsedata['chan'] == j)
                pulsechan = pulsedata[pulsechanmask]

                max28 = (maxchannel['chan'] == 28)
                maxchannel['posx'] = (maxchannel['column'] + 2*(maxchannel['layer']+max28))
                maxchannel['posy'] = (1 - maxchannel['row'] + 2*(maxchannel['layer']+max28))
                pulse28 = (pulsechan['chan'] == 28)
                pulsechan['posx'] = (pulsechan['column'] + 2*(pulsechan['layer']+pulse28))
                pulsechan['posy'] = (1 - pulsechan['row'] + 2*(pulsechan['layer']+pulse28))

                flat_channelarea = ak.flatten(maxchannel['area'],axis=None)
                flat_channel = ak.flatten(maxchannel['chan'],axis=None)
                flat_pulsearea = ak.flatten(pulsechan['area'],axis=None)
                flat_pulsechan = ak.flatten(pulsechan['chan'],axis=None)
                flat_x = ak.flatten(maxchannel['posx'],axis=None)
                flat_y = ak.flatten(maxchannel['posy'],axis=None)
                flat_xp = ak.flatten(pulsechan['posx'],axis=None)
                flat_yp = ak.flatten(pulsechan['posy'],axis=None)
                n_events8 = len(flat_channelarea)
                n_events9 = len(flat_x)
                n_events13 = len(flat_pulsearea)
                n_events14 = len(flat_xp)
                weight8 = ak.ones_like(flat_channelarea)
                weight9 = ak.ones_like(flat_x)
                weight13 = ak.ones_like(flat_pulsearea)
                weight14 = ak.ones_like(flat_xp)
                if n_events8 > 0:
                    channelarea.FillN(n_events8, array('d',flat_channel), array('d',flat_channelarea), array('d',weight8),1)
                if n_events9 > 0:
                    heatchan.FillN(n_events9, array('d',flat_x), array('d',flat_y),array('d',weight9),1)
                if n_events13 > 0:
                    channelpulse.FillN(n_events13, array('d',flat_pulsechan), array('d',flat_pulsearea),array('d',weight13),1)
                if n_events14 > 0:
                    heatchanpulse.FillN(n_events14, array('d',flat_xp), array('d',flat_yp),array('d',weight14),1)
                    

            #print('chan chan done')
        if args.chan:
            maxchan()
                    
        # Heat map for max pulse per layer
        def layermap():
            for j in range(-1,6):
                temp_maxPerLayerMask1 = ((muonarea['area']==ak.max(muonarea['area'][(muonarea['layer']==j)], keepdims=True, axis=-1)))
                maxlayer = muonarea[temp_maxPerLayerMask1]
                layerpulsemask = (pulsedata['layer'] == j)
                layerpulse = pulsedata[layerpulsemask]
                max28 = (maxlayer['chan'] == 28)
                pulse28 = (layerpulse['chan'] == 28)

                maxlayer['posx'] = (maxlayer['column'] + 2*(maxlayer['layer']+max28))
                maxlayer['posy'] = (1 - maxlayer['row'] + 2*(maxlayer['layer']+max28))
                layerpulse['posx'] = (layerpulse['column'] + 2*(layerpulse['layer']+pulse28))
                layerpulse['posy'] = (1 - layerpulse['row'] + 2*(layerpulse['layer']+pulse28))
                flat_x = ak.flatten(maxlayer['posx'],axis=None)
                flat_y = ak.flatten(maxlayer['posy'],axis=None)
                flat_xp = ak.flatten(layerpulse['posx'],axis=None)
                flat_yp = ak.flatten(layerpulse['posy'],axis=None)
                n_events10 = len(flat_x)
                n_events15 = len(flat_xp)
                weight10 = ak.ones_like(flat_x)
                weight15 = ak.ones_like(flat_yp)
                if n_events10 > 0:
                    heatlayer.FillN(n_events10, array('d',flat_x), array('d',flat_y), array('d',weight10),1)
                if n_events15 > 0:
                    heatlayerpulse.FillN(n_events15,array('d',flat_xp),array('d',flat_yp),array('d',weight15),1)

            #print("layermap done")

        if args.heatmap:
            layermap()

        # heatmap for max area pulse per event
        max_event = ak.where(muonarea['area']==ak.max(muonarea['area'],axis=-1),True,False)
        max_event_corrected = ak.where(muonarea['corrected_area']==ak.max(muonarea['corrected_area'],axis=-1),True,False)
        max_data = muonarea[max_event]
        max_data_corrected = muonarea[max_event_corrected]
        max28 = (max_data['chan'] == 28)
        max28cor = (max_data_corrected['chan'] == 28)
        max_data['posx'] = (max_data['column'] + 2*(max_data['layer']+max28))
        max_data['posy'] = (1 - max_data['row'] + 2*(max_data['layer']+max28))
        max_data_corrected['posx'] = (max_data_corrected['column'] + 2*(max_data_corrected['layer']+max28cor))
        max_data_corrected['posy'] = (1 - max_data_corrected['row'] + 2*(max_data_corrected['layer']+max28cor))
        flat_x = ak.flatten(max_data['posx'],axis=None)
        flat_y = ak.flatten(max_data['posy'],axis=None)
        flat_xcor = ak.flatten(max_data_corrected['posx'],axis=None)
        flat_ycor = ak.flatten(max_data_corrected['posy'],axis=None)
        n_events16 = len(flat_x)
        n_events17 = len(flat_xcor)
        weight16 = ak.ones_like(flat_x)
        weight17 = ak.ones_like(flat_xcor)
        if n_events16 > 0:
            heatevent.FillN(n_events16, array('d',flat_x), array('d',flat_y), array('d',weight16),1)
        if n_events17 > 0:
            heateventcorrected.FillN(n_events17, array('d',flat_xcor), array('d',flat_ycor), array('d',weight17),1)
        
        # finding nbars
        nbars = ak.count(ak.run_lengths(muondata['chan']),axis=-1,mask_identity=True)
        # print(nbars)

        flat_side = ak.flatten(sidedata1['area'], axis=None)
        flat_side2 = ak.flatten(sidedata2['area'],axis=None)
        flat_muon = ak.flatten(nbars, axis=None)
        flat_column0 = ak.flatten(columndata0['area'],axis=None)
        flat_column1 = ak.flatten(columndata1['area'],axis=None)
        flat_front = ak.flatten(frontdata['area'],axis=None)
        flat_back = ak.flatten(backdata['area'],axis=None)
        flat_column0chan = ak.flatten(columndata0['chan'],axis=None)
        flat_column1chan = ak.flatten(columndata1['chan'],axis=None)
        flat_columnpulse0 = ak.flatten(columnpulsedata0['area'],axis=None)
        flat_columnpulse1 = ak.flatten(columnpulsedata1['area'],axis=None)
        flat_columnpulse0chan = ak.flatten(columnpulsedata0['chan'],axis=None)
        flat_columnpulse1chan = ak.flatten(columnpulsedata1['chan'],axis=None)

        n_events1 = len(flat_side)
        n_events2 = len(flat_muon)
        n_events3 = len(flat_side2)
        n_events4 = len(flat_column0)
        n_events5 = len(flat_column1)
        n_events6 = len(flat_front)
        n_events7 = len(flat_back)
        n_events11 = len(flat_columnpulse0)
        n_events12 = len(flat_columnpulse1)

        weight1 = ak.ones_like(flat_side)
        weight2 = ak.ones_like(flat_muon)
        weight3 = ak.ones_like(flat_side2)
        weight4 = ak.ones_like(flat_column0)
        weight5 = ak.ones_like(flat_column1)
        weight6 = ak.ones_like(flat_front)
        weight7 = ak.ones_like(flat_back)
        weight11 = ak.ones_like(flat_columnpulse0)
        weight12 = ak.ones_like(flat_columnpulse1)

        if n_events1 > 0:
            side1.FillN(n_events1, array('d',flat_side), array('d',weight1),1)
        if n_events2 > 0:
            muon.FillN(n_events2, array('d',flat_muon), array('d',weight2),1)
        if n_events3 > 0:
            side2.FillN(n_events3, array('d',flat_side2), array('d',weight3),1)
        if n_events4 > 0:
            column0.FillN(n_events4, array('d',flat_column0), array('d',weight4),1)
            column0chan.FillN(n_events4, array('d',flat_column0chan), array('d',flat_column0), array('d',weight4),1)
        if n_events5 > 0:
            column1.FillN(n_events5, array('d',flat_column1), array('d',weight5),1)
            column1chan.FillN(n_events5, array('d',flat_column1chan), array('d',flat_column1), array('d',weight5),1)
        if n_events6 > 0:
            front.FillN(n_events6, array('d',flat_front), array('d',weight6),1)
        if n_events7 > 0:
            back.FillN(n_events7, array('d',flat_back), array('d',weight7),1)
        if n_events11 > 0:
            column0pulse.FillN(n_events11, array('d',flat_columnpulse0),array('d',weight11),1)
            column0pulsechan.FillN(n_events11, array('d',flat_columnpulse0chan),array('d',flat_columnpulse0),array('d',weight11),1)
        if n_events12 > 0:
            column1pulse.FillN(n_events12, array('d',flat_columnpulse1),array('d',weight12),1)
            column1pulsechan.FillN(n_events12,array('d',flat_columnpulse1chan),array('d',flat_columnpulse1),array('d',weight12),1)

    def fitting(hist,histc):
        hist.Fit("gaus","Q")
        f = hist.GetFunction("gaus")
        mean = f.GetParameter(1)
        sigma = f.GetParameter(2)
        hist.Fit("gaus","R","",mean-sigma,mean+sigma)
        hist.SetLineColor(ROOT.kBlue)
        histc.SetLineColor(ROOT.kGreen)
        histc.Draw()
        hist.Draw("SAME")
        legend = TLegend(0.7, 0.75, 0.90, 0.87)
        legend.AddEntry(hist, hist.GetTitle(), "l")
        legend.AddEntry(histc, histc.GetTitle(), "l")
        legend.Draw()
        canvas.Print("chanpulse.pdf")
        g.write(f'\n{hist.GetTitle()}: {mean}')

    canvas = ROOT.TCanvas("canvas")
    canvas.Print("chanpulse.pdf[")
    g = open('gaussian_peak_values.txt', 'w')
    fitting(chanp0,chanpc0)
    fitting(chanp1,chanpc1)
    fitting(chanp2,chanpc2)
    fitting(chanp3,chanpc3)
    fitting(chanp4,chanpc4)
    fitting(chanp5,chanpc5)
    fitting(chanp6,chanpc6)
    fitting(chanp7,chanpc7)
    fitting(chanp8,chanpc8)
    fitting(chanp9,chanpc9)
    fitting(chanp10,chanpc10)
    fitting(chanp11,chanpc11)
    fitting(chanp12,chanpc12)
    fitting(chanp14,chanpc14)
    fitting(chanp20,chanpc20)
    fitting(chanp22,chanpc22)
    canvas.Print("chanpulse.pdf]")
    g.close()

    if not (args.chan or args.heatmap):
        print("Neither the pulse per channel vs channel histograms nor the max pulse per layer heatmaps were plotted.")
        parser.print_help()

    side1.Write()
    side2.Write()
    muon.Write()
    column0.Write()
    column1.Write()
    front.Write()
    back.Write()
    column0chan.Write()
    column1chan.Write()
    channelarea.Write()
    chan0.Write()
    chan1.Write()
    chan2.Write()
    chan3.Write()
    chan4.Write()
    chan5.Write()
    chan6.Write()
    chan7.Write()
    chan8.Write()
    chan9.Write()
    chan10.Write()
    chan11.Write()
    chan12.Write()
    chan14.Write()
    chan20.Write()
    chan22.Write()
    hd0.Write()
    hd1.Write()
    hd2.Write()
    hd3.Write()
    hd4.Write()
    hd5.Write()
    hd6.Write()
    hd7.Write()
    hd8.Write()
    hd9.Write()
    hd10.Write()
    hd11.Write()
    hd12.Write()
    hd14.Write()
    hd20.Write()
    hd22.Write()
    heatchan.Write()
    heatlayer.Write()
    column0pulse.Write()
    column1pulse.Write()
    column0pulsechan.Write()
    column1pulsechan.Write()
    chanp0.Write()
    chanp1.Write()
    chanp2.Write()
    chanp3.Write()
    chanp4.Write()
    chanp5.Write()
    chanp6.Write()
    chanp7.Write()
    chanp8.Write()
    chanp9.Write()
    chanp10.Write()
    chanp11.Write()
    chanp12.Write()
    chanp14.Write()
    chanp20.Write()
    chanp22.Write()
    chanpc0.Write()
    chanpc1.Write()
    chanpc2.Write()
    chanpc3.Write()
    chanpc4.Write()
    chanpc5.Write()
    chanpc6.Write()
    chanpc7.Write()
    chanpc8.Write()
    chanpc9.Write()
    chanpc10.Write()
    chanpc11.Write()
    chanpc12.Write()
    chanpc14.Write()
    chanpc20.Write()
    chanpc22.Write()
    hdp0.Write()
    hdp1.Write()
    hdp2.Write()
    hdp3.Write()
    hdp4.Write()
    hdp5.Write()
    hdp6.Write()
    hdp7.Write()
    hdp8.Write()
    hdp9.Write()
    hdp10.Write()
    hdp11.Write()
    hdp12.Write()
    hdp14.Write()
    hdp20.Write()
    hdp22.Write()
    heatlayerpulse.Write()
    heatchanpulse.Write()
    channelpulse.Write()
    heatevent.Write()
    heateventcorrected.Write()

    output.Close()
if __name__ == "__main__":
    main()
