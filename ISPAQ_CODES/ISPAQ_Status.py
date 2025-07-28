"""
DESCRIPTION:    Modificirana skripta za prikupljanje i provjeru podataka statusa rada iz .csv file-ova (simpleMetrics.csv i PSDMetrics.csv) 
                izracunatih putem ispaq rutine od podataka sa seizmografskih postaja: 'DF01','DF06','OTOC','STON','VSVC','ZBLJ','MRCN','STRC'.
                
                Za normalno pokretanje rutine ispaq potrebno je imati tekstualne preference_files, posebno za svaku postaju. U tekstu 
                preference_file-ova pozivaju se path-ovi od: dataselect_url (dataset -> mseed files), station_url (station .xml file) 
                i resp_dir (path to .resp files). Za ono sto nama treba, .xml file-ovi nisu potrebni.

                Za izracun osnovnog (metrics that do not require metadata) simpleMetrics.csv trebaju nam samo .mseed podaci, dok za 
                izracun PSDMetrics.csv su potrebni .resp file-ovi i .mseed podaci. .xml podaci se koriste za izradu .resp file-ova.

                Ovaj python kod javlja probleme o statusu rada seizmografskih postaja na temelju podataka: simpleMetrics.csv i PSDMetrics.csv.
                Izlazni .txt file se salje na mail kao evidencija o pogreskama u radu seizmografskih postaja.
"""


import pandas as pd
import sys

def simpleMetric_check(error_output,target,metricName,value):
        
    if metricName=='percent_availability' and value<99:
        err = target[3:13] + ': Missing data! Percent availability = ' + str(value)
        error_output.append(err)
        
    elif metricName=='num_spikes' and value>1000:
        err = target[3:13] + ': Too many spikes - check data and metrics!'
        error_output.append(err)
        
    elif metricName=='glitches' and value>1000:
        err = target[3:13] + ': Too many glitches - check data and metrics!'
        error_output.append(err)
        
    elif metricName=='num_gaps' and value>500:
        err = target[3:13] + ': Too many gaps - check data and metrics!'
        error_output.append(err)
        
    elif metricName=='num_overlaps' and value>1000:
        err = target[3:13] + ': Too many overlaps - check data and metrics!'
        error_output.append(err)
        
    elif (metricName=='sample_unique' and value<150) or (metricName=='sample_mean' and abs(value)>1e7) or\
    (metricName=='sample_median' and abs(value)>1e6) or (metricName=='sample_rms' and abs(value)>1e8):
        err = target[3:13] + ': Sample problems - check data and metrics!'
        error_output.append(err)

    return error_output

def simpleRateMetric_check(error_output,target,metricName,value):
    
    if metricName=='sample_rate_channel' and value!=0:
        err = target[3:13] + ': Sample rate problems - check data and metrics!'
        error_output.append(err)

    return error_output

def PSDMetric_check(error_output,target,metricName,value):
    
    if (metricName=='dead_channel_lin' and value<3) or (metricName=='dead_channel_gsn' and value!=0) or\
    (metricName=='pct_below_nlnm' and value>50) or (metricName=='pct_above_nhnm' and value>50):
        err = target[3:13] + ': Channel problems - check PSD and metrics!'
        error_output.append(err)

    return error_output

startdate = sys.argv[1]
error_output = []
stations = ['DF01','DF06','OTOC','STON','VSVC','ZBLJ','MRCN','STRC']

for sta in stations:
    try:
        infile = '/home/check_data/csv/'+sta+'/customStats_myStations_'+startdate+'_simpleMetrics.csv'
        stats = pd.read_csv(infile)
        stats_dict = stats.to_dict('index')

        for k, stinfo in stats_dict.items():
            target = stinfo['target']
            metricName = stinfo['metricName']
            value = stinfo['value']
            error_output = simpleMetric_check(error_output,target,metricName,value)
                    
        infile = '/home/check_data/csv/'+sta+'/customStats_myStations_'+startdate+'_PSDMetrics.csv'
        stats = pd.read_csv(infile)
        stats_dict = stats.to_dict('index')

        for k, stinfo in stats_dict.items():
            target = stinfo['target']
            metricName = stinfo['metricName']
            value = stinfo['value']
            error_output = PSDMetric_check(error_output,target,metricName,value)

    except Exception as e:
        err = 'No metrics file for '+sta+' - Check data!'
        error_output.append(err)
        continue
        
error_output = sorted(error_output)
fout = open('/home/check_data/status/Error_status_'+startdate+'.txt', 'w')
for k in error_output:
    fout.write(k + '\n')
fout.close()
