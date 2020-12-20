from __future__ import division
import scipy.io.wavfile
import scipy.signal
from pylab import *
from numpy import *
from scipy import *
from os import listdir
from os.path import isfile, join, splitext
##################################################################################################################
def loadFiles(path):
    print ("Start reading files:\n")
    files = [ f for f in listdir(path) if isfile(join(path,f)) and splitext(f)[1] == ".wav" ]
    samples = []
    maleCount = 0
    femaleCount = 0
    for f in files:
        p = path + '/' + f
        print ("Actually reading file: ", f, "\n")
        rate, data = scipy.io.wavfile.read(p)
        sig=[mean(d) for d in data]
        samples.append({'name': f, 'nameGender': f[-5:-4], 'signal': sig, 'sampleRate': rate})
        if f[-5:-4] == "M":
            maleCount += 1
        else:
            femaleCount += 1
    counters = {"maleCount": maleCount, "femaleCount": femaleCount}
    return samples, counters
##################################################################################################################
def clearsignal(fft_signal):
    m = max(fft_signal[1:])
    for i in range(1, len(fft_signal)):
        if fft_signal[i] < m / 2:                #here you can change something!!!
            fft_signal[i] = 0
##################################################################################################################
def print_wave(signal):
    var = []
    for i in range(len(signal)):
        var.append(i)
    var = np.array(var)
    fig = plt.figure(figsize=(15, 6), dpi=80)
    ax = fig.add_subplot(111)
    ax.plot(var, signal, linestyle='-')
    plt.show()
##################################################################################################################
def cepstrum(signal, n, w):
    window_time = 250                            #here you can change something!!!
    window_width = int(window_time*w/1000)
    num_of_wind = int(n/window_width)
    f = []
    for i in range(num_of_wind):
        poz = i*window_width
        signal_tmp = signal[poz:poz+window_width]
        signal_tmp *= blackman(len(signal_tmp))
        signal1 = fft(signal_tmp)
        signal1 = abs(signal1)

        clearsignal(signal1)

        for i in range(0, len(signal1)):
            if signal1[i] > 0:
                signal1[i] = log(signal1[i])
        signal2 = ifft(signal1)
        signal2 = abs(signal2)
        poz = 1
        r1 = int(math.floor(w/80))
        r2 = int(math.floor(w/255))
        m = max(signal2[r2:r1])
        for i in range(r2, r1):
            if m == signal2[i]:
                poz = i
                break
        f.append(w/poz)
    result = np.median(sorted(f))
    return result
##################################################################################################################
def recognizeGender(s):
    signal = s['signal']
    sig_len = len(s['signal'])
    rate = s['sampleRate']
    f = cepstrum(signal, sig_len, rate)
    # 165->87.9% dobrze
    # 167->87.9% dobrze
    # 170->89% dobrze
    if f<167:                                       #here you can change something!!!
        return 'M'
    else:
        return 'K'
##################################################################################################################
def launchAlgorithm(samples, counters):
    recognizedMale = 0
    recognizedFemale = 0
    wellRecognized = 0
    print ("Starting algorytm:\n")
    for s in samples:
        gender = recognizeGender(s)
        if gender == s['nameGender']:
            wellRecognized += 1
            if gender == "M":
                recognizedMale += 1
            elif gender == "K":
                recognizedFemale += 1
            print (s['name'], " Well recognized\n")
        else:
            print (s['name'], " Wrong recognized\n")
    samplesCount = counters['maleCount'] + counters['femaleCount']
    print ("Results:\n")
    print ("Well recognized number of Male: ", recognizedMale, "/", counters['maleCount'], '\n')
    print ("Well recognized number of Female: ", recognizedFemale, "/", counters['femaleCount'], '\n')
    print ("Final result: ", wellRecognized, "/", samplesCount, " (", wellRecognized/samplesCount*100, "%)", '\n')
##################################################################################################################
if __name__ == '__main__':
    samples, counters = loadFiles("train")
    launchAlgorithm(samples, counters)




