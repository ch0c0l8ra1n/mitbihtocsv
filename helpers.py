import wfdb

def plotBeat( recId, point, width=75):
    sampfrom = point-width
    sampto = point+width
    r,s,a = getRecSampAnn(str(recId) , sampfrom=sampfrom,sampto=sampto)
    plotRec(recId,sampfrom,sampto) 

def getVoltages( recId,point,symbol,width=75):
    sampfrom = point-width
    sampto = point+width
    try:
        r = wfdb.rdrecord("data/"+str(recId),sampfrom=sampfrom,sampto=sampto) 
    except ValueError:
        return None
    signal = r.p_signal
    channelCount = len(signal[0])
    signals = [ [symbol] ]*channelCount 
    for item in signal:
        for i in range(channelCount):
            signals[i].append(item[i])
    return signals 

def signalListToString(sig):
    stringBuffer  = ""
    for item in sig[1:]:
        stringBuffer += str(item)+","
    stringBuffer+=sig[0]
    return stringBuffer

def plotRec(recId,sampfrom=0,sampto=None):
    r,s,a = getRecSampAnn(str(recId) , sampfrom=sampfrom,sampto=sampto)
    wfdb.plot_wfdb(r,a)

def getRecSampAnn(index,out="data",sampfrom=0,sampto=None):
    path="{}/{}".format(out,index)
    rec  = wfdb.rdrecord(path,sampfrom=sampfrom,sampto=sampto)
    ann  = wfdb.rdann(path,"atr",sampfrom=sampfrom,sampto=sampto,shift_samps=True)
    samp = wfdb.rdsamp(path,sampfrom=sampfrom,sampto=sampto)
    
    return rec,samp,ann




