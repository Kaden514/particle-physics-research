import awkward as ak
import uproot
import ROOT
from array import array

ROOT.gStyle.SetOptStat(0) # to hide the histogram stats box

file = 'file directory taken out from original version for proprietary reasons'
var = ["timeFit_module_calibrated", 'time', "chan", "layer", "event_time_fromTDC", "area", "ipulse", "energy", "type", "height", "duration"]

output = ROOT.TFile('timestream.root','RECREATE') # output file
thrugoing = ROOT.TH2D('thrugoing', 'thrugoing', 100, -50, 50, 100, 0, 10)
background = ROOT.TH2D('background', 'background', 100, -50, 50, 100, 0, 10)
muon = ROOT.TH2D('muon', 'muon', 100, -50, 50, 100, 0, 100000)
area1 = ROOT.TH1D('frontleft', 'ch16 area (18e3 < ch18 area < 30e3)', 100, 0, 200000)
area2 = ROOT.TH1D('backleft', 'ch18 area (18e3 < ch18 area < 30e3)', 100, 0, 200000)
area3 = ROOT.TH1D('frontright', 'ch16 area (30e3 < ch18 area)', 100, 0, 200000)
area4 = ROOT.TH1D('backright', 'ch18 area (30e3 < ch18 area)', 100, 0, 200000)
area5 = ROOT.TH1D('front40', 'ch16 area (40e3 < ch18 area)', 100, 0, 200000)
area_height1 = ROOT.TH2D('area_h1', 'ch16 Height vs. Duration', 100, 0, 1500, 100, 0, 1500)
area_height2 = ROOT.TH2D('area_h2', 'ch18 Height vs. Duration', 100, 0, 1500, 100, 0, 1500)
bothareas = ROOT.TH2D('bothareas', 'ch16 Area vs. ch18 Area', 100, 0, 100000, 100, 0, 100000)

#i = 0
# 1348, just muon triggers
# look at how many bars are being hit and size of pulses
# /eos/experiment/formosa/commissioning/data/offline/v38/1300/0004
# figure out in each layer which bar has max pulse
# then look at pulses in every other bar
# how many bars are hit, then size of pulses
# first lets look at activity of side panels when there's a muon
# top left is row==0 and column==0
# side panels are indexed by type==2

for data in uproot.iterate(file, var, library='ak', step_size='10 mB'):
    #i += 1
    #if i > 500:
    #    break
    
    data["event_time_fromTDC"] = ak.broadcast_arrays(data["event_time_fromTDC"], data["timeFit_module_calibrated"])[0]

    timecut = (data['time'] < 600) & (data['time'] > 400) # masking for the desired events
    layer0 = ((data['layer']==0) & (data['type']==0))
    layer1 = ((data['layer']==1) & (data['type']==0))
    layer2 = ((data['layer']==2) & (data['type']==0))
    layer3 = ((data['layer']==3) & (data['type']==0))

    mask1 = ak.any(((layer0) & (timecut)),axis=-1) & ak.any(((layer1) & (timecut)),axis=-1) & ak.any(((layer2) & (timecut)),axis=-1) & ak.any(((layer3) & (timecut)),axis=-1)
    mask2 = ak.any(((layer0) & (timecut) 
                    & (data['area']>95e3)
                    ),axis=-1) & ak.any(((layer1) & (timecut) 
                    & (data['area']>95e3)
                    ),axis=-1) & ak.any(((layer2) & (timecut) 
                    & (data['area']>95e3)
                    ),axis=-1) & ak.any(((layer3) & (timecut) 
                    & (data['area']>95e3)
                    ),axis=-1)
    maskback = mask1 & ak.all((data["chan"] != 16), axis=-1) & ak.all((data["chan"] != 18), axis=-1)
    maskmuon = mask2 & ak.any(((data["chan"] == 16) & (timecut) & (data['area']>30e3)), axis=-1) & ak.any(((data["chan"] == 18) & (timecut) & (data['area']>18e3)), axis=-1)
    maskmuon_area = mask2 & ak.any(((data['chan'] == 16) & (timecut)), axis = -1) & ak.any(((data['chan'] == 18) & (timecut)), axis = -1)
    maskmuon_arear = mask2 & ak.any(((data['chan'] == 16) & (timecut)), axis = -1) & ak.any(((data['chan'] == 18) & (timecut) & (data['area']>30e3)), axis = -1)
    maskmuon_areal = mask2 & ak.any(((data['chan'] == 16) & (timecut)), axis = -1) & ak.any(((data['chan'] == 18) & (timecut) & (data['area']>18e3) & (data['area']<30e3)), axis=-1)
    maskmuon_area40 = mask2 & ak.any(((data['chan'] == 16) & (timecut)), axis = -1) & ak.any(((data['chan'] == 18) & (timecut) & (data['area']>40e3)), axis = -1)

    mask_muonh1 = maskmuon_area & (data['chan'] == 16) & (data['ipulse'] == 0)
    mask_muonh2 = maskmuon_area & (data['chan'] == 18) & (data['ipulse'] == 0)
    muonh1 = data[mask_muonh1]
    muonh2 = data[mask_muonh2]

    mask_area1l = maskmuon_areal & (data['chan'] == 16) & (data['ipulse'] == 0)# pick out the individual end panels' pulses to plot area
    mask_area2l = maskmuon_areal & (data['chan'] == 18) & (data['ipulse'] == 0)
    mask_area1r = maskmuon_arear & (data['chan'] == 16) & (data['ipulse'] == 0)
    mask_area2r = maskmuon_arear & (data['chan'] == 18) & (data['ipulse'] == 0)
    mask_area40 = maskmuon_area40 & (data['chan'] == 16) & (data['ipulse'] == 0)
    #print(mask_area1)
    #print(mask_area2)
    area_data1l = data[mask_area1l] # applying the area masks
    area_data2l = data[mask_area2l]
    area_data1r = data[mask_area1r]
    area_data2r = data[mask_area2r]
    area_data40 = data[mask_area40]

    #print(area_data1)
    #print(area_data2)

    mask_thru1 = mask1 & (data['layer'] == 0) # masking for the pulses in the respective layers for time difference
    mask_thru2 = mask1 & (data['layer'] == 3) 
    mask_back1 = maskback & (data['layer'] == 0) 
    mask_back2 = maskback & (data['layer'] == 3) 
    mask_muon1 = maskmuon & (data['layer'] == 0) 
    mask_muon2 = maskmuon & (data['layer'] == 3) 
    #print('t1',mask_thru1)
    #print('t2',mask_thru2)
    #print('b1',mask_back1)
    #print('b2',mask_back2)
    #print('m1',mask_muon1)
    #print('m2',mask_muon2)    
    thru1 = data[mask_thru1] # these are the pulses in layers 0 and 3
    thru2 = data[mask_thru2]
    back1 = data[mask_back1]
    back2 = data[mask_back2]
    muon1 = data[mask_muon1]
    muon2 = data[mask_muon2]
    #print('diff1', diff1)
    #print(len(diff1))
    #print(muon1)
    #print(muon2)
    max_thru1 = ak.where(thru1['area']==ak.max(thru1['area'], axis=-1),True,False) # masking for the max area pulses
    max_thru2 = ak.where(thru2['area'] == ak.max(thru2['area'], axis=-1), True, False)
    max_back1 = ak.where(back1['area'] == ak.max(back1['area'], axis=-1), True, False)
    max_back2 = ak.where(back2['area'] == ak.max(back2['area'], axis=-1), True, False)
    max_muon1 = ak.where(muon1['area'] == ak.max(muon1['area'], axis=-1), True, False)
    max_muon2 = ak.where(muon2['area'] == ak.max(muon2['area'], axis=-1), True, False)

    #print(diff2)
    #print(mask_diff2)
    #print(data1['layer'])

    thru1 = thru1[max_thru1] # applying the max area pulse masks
    thru2 = thru2[max_thru2]
    back1 = back1[max_back1]
    back2 = back2[max_back2]
    muon1 = muon1[max_muon1]
    muon2 = muon2[max_muon2]

    #print(thru1['area'])
    #print('max', ak.max(thru1['area']))
    #print(thru2['area'])
    #print(ak.max(diff2['area']))
    #print(back2)

    t_thru = thru2['timeFit_module_calibrated'] - thru1['timeFit_module_calibrated'] # getting the time differences for plotting
    t_back = back2['timeFit_module_calibrated'] - back1['timeFit_module_calibrated']
    t_muon = muon2['timeFit_module_calibrated'] - muon1['timeFit_module_calibrated']

    t_energy = data[mask1]
    b_energy = data[maskback]
    m_energy = data[maskmuon]
    
    #print(t_thru)
    #print('muon area: ', m_energy['area'])
    #print(t_back)
    #print(t_muon)
    #print(diff1['timeFit_module_calibrated'])
    #print(diff2['timeFit_module_calibrated'])
    #print('time', t_muon)
    #print('energy', m_energy['energy'])

    #print(ak.drop_none(t_thru))
    #print(diff1['area'])

    flat_time = ak.flatten(t_thru, axis=None)
    flat_back = ak.flatten(t_back, axis=None)
    flat_muon = ak.flatten(t_muon, axis=None)
    flat_area1l = ak.flatten(area_data1l['area'], axis=None)
    flat_area2l = ak.flatten(area_data2l['area'], axis=None)
    flat_area1r = ak.flatten(area_data1r['area'], axis=None)
    flat_area2r = ak.flatten(area_data2r['area'], axis=None)
    flat_area40 = ak.flatten(area_data40['area'], axis=None)
    flat_t_energy = ak.flatten(ak.max(t_energy['energy'], axis=-1),axis=None)
    flat_b_energy = ak.flatten(ak.max(b_energy['energy'], axis=-1),axis=None)
    flat_m_energy = ak.flatten(ak.max(m_energy['energy'], axis=-1),axis=None)
    flat_m_height1 = ak.flatten(muonh1['height'], axis=None)
    flat_m_height2 = ak.flatten(muonh2['height'],axis=None)
    flat_m_area1 = ak.flatten(muonh1["duration"], axis=None)
    flat_m_area2 = ak.flatten(muonh2['duration'],axis=None)

    n_events1 = len(flat_time)
    n_events2 = len(flat_back)
    n_events3 = len(flat_muon)
    n_events4 = len(flat_area1l)
    n_events5 = len(flat_area2l)
    n_events6 = len(flat_area1r)
    n_events7 = len(flat_area2r)
    n_events8 = len(flat_area40)
    n_events9 = len(flat_m_height1)
    n_events10 = len(flat_m_height2)
    n_events11 = len(flat_m_area1)
    n_events12 = len(flat_m_area2)

    weight1 = ak.ones_like(flat_time)
    weight2 = ak.ones_like(flat_back)
    weight3 = ak.ones_like(flat_muon)
    weight4 = ak.ones_like(flat_area1l)
    weight5 = ak.ones_like(flat_area2l)
    weight6 = ak.ones_like(flat_area1r)
    weight7 = ak.ones_like(flat_area2r)
    weight8 = ak.ones_like(flat_area40)
    weight9 = ak.ones_like(flat_m_height1)
    weight10 = ak.ones_like(flat_m_height2)
    weight11 = ak.ones_like(flat_m_area1)
    weight12 = ak.ones_like(flat_m_area2)

    if n_events1 > 0:
        thrugoing.FillN(n_events1, array('d', flat_time), array('d', flat_t_energy), array('d', weight1),1)
    if n_events2 > 0:
        background.FillN(n_events2, array('d', flat_back), array('d', flat_b_energy), array('d', weight2),1)
    if n_events3 > 0:
        muon.FillN(n_events3, array('d', flat_muon), array('d', flat_m_energy), array('d', weight3),1)
    if n_events4 > 0:
        area1.FillN(n_events4, array('d', flat_area1l), array('d', weight4),1)
    if n_events5 > 0:
        area2.FillN(n_events5, array('d', flat_area2l), array('d', weight5),1)
    if n_events6 > 0:
        area3.FillN(n_events6, array('d', flat_area1r), array('d', weight6),1)
    if n_events7 > 0:
        area4.FillN(n_events7, array('d', flat_area2r), array('d', weight7),1)
    if n_events8 > 0:
        area5.FillN(n_events8, array('d', flat_area40), array('d', weight8),1)
    if n_events9 > 0:
        area_height1.FillN(n_events9, array('d', flat_m_area1), array('d', flat_m_height1), array('d', weight9),1)
    if n_events10 > 0:
        area_height2.FillN(n_events10, array('d', flat_m_area2), array('d', flat_m_height2), array('d', weight10),1)
    if n_events11 > 0:
        bothareas.FillN(n_events11, array('d', flat_m_area2), array('d', flat_m_area1), array('d', weight11),1)

    #print(i)
    #print(thru1)

thrugoing.Write()
background.Write()
muon.Write()
area1.Write()
area2.Write()
area3.Write()
area4.Write()
area5.Write()
area_height1.Write()
area_height2.Write()
bothareas.Write()
#print("done")

output.Close()