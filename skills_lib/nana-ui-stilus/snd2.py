import numpy as np, subprocess
from scipy.io import wavfile
SR=44100; D=12.0; N=int(SR*D); s=np.zeros(N)
P="/home/claude/sfxnew/anyag/sfx/"
def load(f,maxd=None):
    r=subprocess.run(["ffmpeg","-v","error","-i",P+f,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    a=np.frombuffer(r,np.float32).astype(float)
    if maxd: a=a[:int(maxd*SR)]; a[-int(0.05*SR):]*=np.linspace(1,0,int(0.05*SR))
    return a/ (np.max(np.abs(a))+1e-9)
def add(x,at,g):
    i=int(at*SR); e=min(N,i+len(x)); s[i:e]+=x[:e-i]*g
POP=load("pop_2357-preview.mp3"); TICK=load("pop_3005-preview.mp3"); TYPE=load("typing_1393-preview.mp3",0.8)
NOTE=load("notification_2575-preview.mp3"); SPARK=load("sparkle_871-preview.mp3"); WH=load("whoosh_1491-preview.mp3"); CLICK=load("click_2568-preview.mp3"); BUB=load("bubble_1317-preview.mp3")
add(BUB,0.1,0.35); add(BUB,0.9,0.3)
for t in [1.8,3.0,4.8]: add(POP,t,0.55)
for t in [2.7,4.5,6.0]: add(WH,t-0.1,0.25)
add(TYPE,3.5,0.35); add(CLICK,5.6,0.6)
add(SPARK,6.3,0.5); add(NOTE,7.4,0.45)
add(WH,8.5,0.45); add(BUB,8.9,0.35); add(BUB,9.6,0.3); add(POP,10.3,0.55); add(TYPE,10.7,0.35)
sr,m=wavfile.read("/home/claude/mb/mix_music.wav"); m=m.astype(float)/32768; m=np.pad(m,(0,max(0,N-len(m))))[:N]
tt=np.arange(N)/SR; m*=np.clip((D-tt)/1.5,0,1)
mix=m/np.max(np.abs(m))*0.4+s*0.9
wavfile.write("mix2.wav",SR,(mix/np.max(np.abs(mix))*0.95*32767).astype(np.int16))
