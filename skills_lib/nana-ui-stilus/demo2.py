import math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS,DUR=1080,1920,30,12.0
IF="/home/claude/fontpkg/node_modules/@expo-google-fonts/inter/"
def F(p,s): return ImageFont.truetype(p,int(s))
SER="PlayfairDisplay.ttf"; HAND="PatrickHand-Regular.ttf"
I5=IF+"500Medium/Inter_500Medium.ttf"; I6=IF+"600SemiBold/Inter_600SemiBold.ttf"; I7=IF+"700Bold/Inter_700Bold.ttf"
INK=(38,36,40); SOFT=(110,104,100); ACC=(196,110,70); GREEN=(52,160,90); CX=500
def clamp(x): return max(0.0,min(1.0,x))
def eo(x): x=clamp(x); return 1-(1-x)**3
def ob(x): x=clamp(x); c=1.5; return 1+(c+1)*(x-1)**3+c*(x-1)**2
src="/home/claude/ad/stock/laptop_29997.mp4"
rd=subprocess.Popen(["ffmpeg","-v","error","-ss","1","-i",src,"-t",str(DUR+0.5),"-vf","scale=-2:2100,crop=1080:1920,fps=30,gblur=sigma=14,eq=saturation=0.55:brightness=0.10","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
CREAM=np.array([248,242,233],np.float32)
yy,xx=np.mgrid[0:H,0:W]; vig=np.clip(1-0.18*(((xx-W/2)/(W*0.8))**2+((yy-H/2)/(H*0.75))**2),0.82,1)[...,None]
rng=np.random.default_rng(2)
def card(l,box,r=26,fill=(255,255,255),a=250):
    x0,y0,x1,y1=box; s=Image.new("RGBA",l.size,(0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle([x0+4,y0+12,x1+4,y1+12],radius=r,fill=(90,70,50,60))
    l.alpha_composite(s.filter(ImageFilter.GaussianBlur(16))); ImageDraw.Draw(l).rounded_rectangle(box,radius=r,fill=fill+(a,))
def pop(img,t,a,fn,cy):
    p=clamp((t-a)/0.45)
    if p<=0: return
    lay=Image.new("RGBA",img.size,(0,0,0,0)); fn(lay)
    off=int((1-eo(p))*36)
    if p<1:
        al=lay.split()[3].point(lambda v:int(v*eo(p))); lay.putalpha(al)
    img.alpha_composite(lay,(0,off))
def serif(img,t,a,txt,y,size=80,col=INK):
    d=ImageDraw.Draw(img); f=F(SER,size); x=CX-d.textlength(txt,font=f)/2
    for i,w in enumerate(txt.split(" ")):
        p=clamp((t-a-i*0.12)/0.4); ww=d.textlength(w+" ",font=f)
        if p>0:
            l=Image.new("RGBA",img.size,(0,0,0,0)); ImageDraw.Draw(l).text((x,y+(1-eo(p))*14),w,font=f,fill=col+(int(255*eo(p)),)); img.alpha_composite(l)
        x+=ww
def hand(img,t,a,txt,y,size=54,col=ACC,dur=1.0):
    f=F(HAND,size); tw=ImageDraw.Draw(img).textlength(txt,font=f); p=clamp((t-a)/dur)
    if p<=0: return
    l=Image.new("RGBA",(int(tw)+20,size+30),(0,0,0,0)); ImageDraw.Draw(l).text((10,8),txt,font=f,fill=col)
    l=l.crop((0,0,max(1,int(l.width*p)),l.height)); img.alpha_composite(l,(int(CX-tw/2-10),int(y-8)))
def arrow(img,t,a,y0,y1):
    p=clamp((t-a)/0.4)
    if p<=0: return
    d=ImageDraw.Draw(img); ye=y0+(y1-y0)*eo(p)
    d.line([CX,y0,CX,ye],fill=ACC,width=6)
    if p>0.6: d.polygon([(CX-16,ye-18),(CX+16,ye-18),(CX,ye+4)],fill=ACC)
def num(d,x,y,n):
    d.ellipse([x,y,x+54,y+54],fill=ACC); d.text((x+27,y+27),str(n),font=F(I7,28),fill=(255,255,255),anchor="mm")
def step(img,t,a,n,title,sub,y,chip=None,chip_t=0,btn=False):
    def fn(l):
        card(l,[130,y,870,y+150]); d=ImageDraw.Draw(l); num(d,160,y+48,n)
        d.text((240,y+34),title,font=F(I7,34),fill=INK); d.text((240,y+86),sub,font=F(I5,26),fill=SOFT)
        if chip:
            k=int(len(chip)*clamp((t-chip_t)/0.8))
            if k>0:
                tw=d.textlength(chip,font=F(I6,24)); d.rounded_rectangle([840-tw-36,y+90,840,y+130],radius=20,fill=(246,236,226)); d.text((840-18,y+110),chip[:k],font=F(I6,24),fill=ACC,anchor="rm")
        if btn:
            pp=clamp((t-a-0.8)/0.3); s=1-0.08*math.sin(math.pi*pp)
            bw,bh=230*s,52*s; cx,cy=730,y+75; d.rounded_rectangle([cx-bw/2,cy-bh/2,cx+bw/2,cy+bh/2],radius=12,fill=(178,40,46)); d.text((cx,cy),"BERECHNEN",font=F(I7,22),fill=(255,255,255),anchor="mm")
    pop(img,t,a,fn,y+75)
def result(img,t,a,y):
    def fn(l):
        card(l,[230,y,770,y+225],r=30,fill=(255,255,255),a=252); d=ImageDraw.Draw(l); d.rounded_rectangle([230,y,770,y+225],radius=30,outline=ACC,width=4)
        d.text((CX,y+30),"HAVI NETTÓ",font=F(I7,24),fill=ACC,anchor="ma")
        v=int(1672*eo((t-a-0.2)/1.3)); d.text((CX,y+58),f"{v:,}".replace(","," ")+" €",font=F(SER,96),fill=INK,anchor="ma")
        d.text((CX,y+185),"2 000 € bruttóból",font=F(I5,22),fill=SOFT,anchor="ma")
    pop(img,t,a,fn,y+100)
def comment(img,t,a,y,word):
    def fn(l):
        card(l,[130,y,870,y+86],r=43); d=ImageDraw.Draw(l); d.ellipse([150,y+17,202,y+69],fill=(220,196,176))
        k=int(len(word)*clamp((t-a-0.4)/0.6)); d.text((222,y+25),word[:k],font=F(I7,30),fill=INK); d.text((840,y+27),"Post",font=F(I6,28),fill=(56,120,240),anchor="ra")
    pop(img,t,a,fn,y+43)
def frame(t,bg):
    z=1+0.04*t/DUR; b=bg.resize((int(W*z),int(H*z)),Image.BILINEAR); ox=(b.width-W)//2; oy=(b.height-H)//2; b=b.crop((ox,oy,ox+W,oy+H))
    a=np.asarray(b).astype(np.float32)*0.30+CREAM*0.70; a=a*vig+rng.normal(0,4,(H,W,1))
    img=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert("RGBA")
    if t<8.8:
        fade=1-clamp((t-8.4)/0.4)
        lay=Image.new("RGBA",img.size,(0,0,0,0))
        serif(lay,t,0.1,"Mennyi marad",380); serif(lay,t,0.35,"a bruttóból?",470); hand(lay,t,0.9,"(Ausztriában, 3 lépésben kiszámolod)",575)
        step(lay,t,1.8,1,"Nyisd meg","AK Brutto-Netto-Rechner",690)
        arrow(lay,t,2.7,845,900)
        step(lay,t,3.0,2,"Írd be","havi bruttó + tartomány",910,chip="2 000 € · Stmk",chip_t=3.5)
        arrow(lay,t,4.5,1065,1120)
        step(lay,t,4.8,3,"Számold ki",'"Jetzt berechnen"',1130,btn=True)
        arrow(lay,t,6.0,1285,1330)
        result(lay,t,6.3,1340)
        if fade<1: al=lay.split()[3].point(lambda v:int(v*fade)); lay.putalpha(al)
        img.alpha_composite(lay)
    else:
        serif(img,t,8.9,"Mentsd el,",520); serif(img,t,9.15,"hogy meglegyen…",612)
        hand(img,t,9.6,"(és küldd el annak, akinek jól jön)",720,size=48)
        comment(img,t,10.3,880,"NETTÓ")
    return img.convert("RGB")
only=[float(x) for x in sys.argv[1:]]
wr=None if only else subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1080x1920","-r","30","-i","-","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","silent2.mp4"],stdin=subprocess.PIPE)
for n in range(int(DUR*FPS)):
    buf=rd.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    t=n/FPS
    if only and not any(abs(t-o)<0.017 for o in only): continue
    im=frame(t,Image.frombytes("RGB",(W,H),buf))
    if only: im.save(f"e_{t:05.2f}.jpg",quality=85)
    else: wr.stdin.write(im.tobytes())
if wr: wr.stdin.close(); wr.wait()
