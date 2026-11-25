import sys, json, numpy as np
sys.path.insert(0,"/home/claude/mb")
from sfxlib import *
from scipy.io import wavfile
D=10.0; N=int(SR*D); s=np.zeros(N)
def add(x,at,g):
    i=int(at*SR); e=min(N,i+len(x)); s[i:e]+=x[:e-i]*g
for t in [0.1,0.35,1.0,7.5,7.75,8.2]: add(blub(),t,0.5)
for t in [1.8,3.6,5.1,6.3,8.4]: add(pop(),t,0.8)
for t in [4.0,4.35,4.7,6.3]: add(ping(),t,0.45)
r=np.random.default_rng(3)
for t in np.arange(2.3,3.9,0.075): add(tick(),t+r.uniform(-0.02,0.02),0.35)
for t in np.arange(8.8,9.4,0.09): add(tick(),t,0.35)
add(whoosh(),7.3,0.7)
sr,m=wavfile.read("/home/claude/mb/mix_music.wav"); m=m.astype(float)/32768; m=np.pad(m,(0,max(0,N-len(m))))[:N]
tt=np.arange(N)/SR; m*=np.clip((D-tt)/1.5,0,1)
mix=m/np.max(np.abs(m))*0.45+s/np.max(np.abs(s))*0.5
wavfile.write("mix.wav",SR,(mix/np.max(np.abs(mix))*0.95*32767).astype(np.int16))
