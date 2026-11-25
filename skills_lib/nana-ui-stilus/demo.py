import math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS,DUR=1080,1920,30,10.0
IF="/home/claude/fontpkg/node_modules/@expo-google-fonts/inter/"
def F(p,s): return ImageFont.truetype(p,int(s))
SER="PlayfairDisplay.ttf"; HAND="PatrickHand-Regular.ttf"
I5=IF+"500Medium/Inter_500Medium.ttf"; I6=IF+"600SemiBold/Inter_600SemiBold.ttf"; I7=IF+"700Bold/Inter_700Bold.ttf"; I4=IF+"400Regular/Inter_400Regular.ttf"
CREAM=(246,238,224); YEL=(244,214,120); INK=(28,28,32); CX=500
def clamp(x): return max(0.0,min(1.0,x))
def eo(x): x=clamp(x); return 1-(1-x)**3
def ob(x): x=clamp(x); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
# background frames
src="/home/claude/ad/stock/laptop_29997.mp4"
rd=subprocess.Popen(["ffmpeg","-v","error","-ss","1","-i",src,"-t",str(DUR+0.5),"-vf","scale=-2:2100,crop=1080:1920,fps=30,eq=saturation=0.75:contrast=1.04:brightness=-0.04,colorbalance=rs=0.06:gs=0.02:bs=-0.06","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
yy,xx=np.mgrid[0:H,0:W]; topg=(1-0.45*np.clip(1-(yy-250)/600,0,1)*(yy>250)-0.45*(yy<=250))[...,None]; vig=np.clip(1-0.55*(((xx-W/2)/(W*0.75))**2+((yy-H/2)/(H*0.7))**2),0.35,1)[...,None]
rng=np.random.default_rng(1)
def shadow_card(img,box,r,fill,alpha=245,sh=110,blur=18,outline=None):
    x0,y0,x1,y1=box
    s=Image.new("RGBA",img.size,(0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle([x0+6,y0+14,x1+6,y1+14],radius=r,fill=(0,0,0,sh))
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))
    l=Image.new("RGBA",img.size,(0,0,0,0)); ImageDraw.Draw(l).rounded_rectangle(box,radius=r,fill=fill+(alpha,),outline=outline,width=2 if outline else 0)
    img.alpha_composite(l)
def pop(img,t,a,draw_fn,cx,cy,scale_from=0.85):
    p=clamp((t-a)/0.45)
    if p<=0: return
    lay=Image.new("RGBA",img.size,(0,0,0,0)); draw_fn(lay)
    k=scale_from+(1-scale_from)*ob(p); dy=(1-eo(p))*40
    if k!=1:
        lay=lay.resize((int(W*k),int(H*k)),Image.BILINEAR); ox=int(cx-cx*k); oy=int(cy-cy*k+dy)
        tmp=Image.new("RGBA",img.size,(0,0,0,0)); tmp.alpha_composite(lay,(max(0,ox),max(0,oy)) if ox>=0 and oy>=0 else (0,0)); lay=tmp
    if p<1: a_=lay.split()[3].point(lambda v:int(v*eo(p))); lay.putalpha(a_)
    img.alpha_composite(lay)
def serif_line(img,t,a,txt,y,size=78):
    d=ImageDraw.Draw(img); f=F(SER,size); words=txt.split(" ")
    tot=d.textlength(txt,font=f); x=CX-tot/2
    for i,w in enumerate(words):
        p=clamp((t-a-i*0.12)/0.4)
        ww=d.textlength(w+" ",font=f)
        if p>0:
            l=Image.new("RGBA",img.size,(0,0,0,0)); dl=ImageDraw.Draw(l)
            dl.text((x+2,y+3+(1-eo(p))*14),w,font=f,fill=(0,0,0,int(120*p))); 
            l=l.filter(ImageFilter.GaussianBlur(3)); dl=ImageDraw.Draw(l)
            dl.text((x,y+(1-eo(p))*14),w,font=f,fill=CREAM+(int(255*eo(p)),))
            img.alpha_composite(l)
        x+=ww
def hand_line(img,t,a,txt,y,size=58,dur=1.0):
    f=F(HAND,size); d=ImageDraw.Draw(img); tw=d.textlength(txt,font=f)
    p=clamp((t-a)/dur)
    if p<=0: return
    l=Image.new("RGBA",(int(tw)+20,size+30),(0,0,0,0)); dl=ImageDraw.Draw(l)
    dl.text((12,10),txt,font=f,fill=(0,0,0,110)); l=l.filter(ImageFilter.GaussianBlur(2)); dl=ImageDraw.Draw(l); dl.text((10,8),txt,font=f,fill=YEL)
    cut=int(l.width*p); l=l.crop((0,0,max(1,cut),l.height))
    img.alpha_composite(l,(int(CX-tw/2-10),int(y-8)))
def icon(d,x,y,s=40):
    d.rounded_rectangle([x,y,x+s,y+s],radius=10,fill=(212,96,70))
    for k in range(6):
        ang=k*math.pi/3; d.line([x+s/2,y+s/2,x+s/2+math.cos(ang)*s*0.34,y+s/2+math.sin(ang)*s*0.34],fill=(255,240,230),width=3)
def prompt_bar(img,t,a,txt,y=1300):
    def dr(l):
        d=ImageDraw.Draw(l); box=[120,y,880,y+96]
        tmp=Image.new("RGBA",img.size,(0,0,0,0)); shadow_card(tmp,box,26,(252,250,247)); l.alpha_composite(tmp); d=ImageDraw.Draw(l)
        icon(d,140,y+28,42)
        d.text((198,y+22),"AK RECHNER",font=F(I7,17),fill=(150,150,150))
        n=int(len(txt)*clamp((t-a-0.5)/1.6)); s=txt[:n]+("|" if (t*2)%1<0.5 and n<len(txt) else "")
        d.text((198,y+46),s,font=F(I5,29),fill=INK)
        d.rounded_rectangle([812,y+26,856,y+70],radius=12,fill=(212,96,70)); d.polygon([(826,y+56),(834,y+38),(842,y+56)],fill=(255,255,255))
    pop(img,t,a,dr,500,y+48)
def mac_window(img,t,a,rows,ticks):
    def dr(l):
        box=[110,720,560,1060]; tmp=Image.new("RGBA",img.size,(0,0,0,0)); shadow_card(tmp,box,22,(250,249,246)); l.alpha_composite(tmp); d=ImageDraw.Draw(l)
        for i,c in enumerate([(237,106,94),(245,191,79),(97,197,84)]): d.ellipse([132+i*24,742,148+i*24,758],fill=c)
        d.text((220,740),"brutto-netto · 2026",font=F(I6,19),fill=(120,120,120))
        d.line([110,776,560,776],fill=(230,228,224),width=2)
        for i,(k,v) in enumerate(rows):
            yy=800+i*80; d.rounded_rectangle([132,yy,538,yy+62],radius=14,fill=(244,242,238))
            d.text((150,yy+18),k,font=F(I5,24),fill=(90,90,90)); d.text((470,yy+18),v,font=F(I7,24),fill=INK,anchor="ra")
            pt=clamp((t-ticks[i])/0.25)
            if pt>0:
                cx,cy=510,yy+31; r=13*ob(pt); d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(52,168,90))
                if pt>0.5: d.line([cx-6,cy,cx-1,cy+5,cx+7,cy-6],fill=(255,255,255),width=3)
    pop(img,t,a,dr,335,890)
def dark_badge(img,t,a):
    def dr(l):
        box=[620,740,900,930]; tmp=Image.new("RGBA",img.size,(0,0,0,0)); shadow_card(tmp,box,24,(24,24,28),alpha=235); l.alpha_composite(tmp); d=ImageDraw.Draw(l)
        d.text((760,772),"HAVI NETTÓ",font=F(I7,19),fill=(170,170,170),anchor="ma")
        v=int(1672*eo((t-a-0.2)/1.2)); s=f"{v:,}".replace(","," ")+" €"
        d.text((760,812),s,font=F("InstrumentSerif-Regular.ttf",78),fill=(246,238,224),anchor="ma")
        d.text((760,900),"2 000 € bruttóból",font=F(I5,18),fill=(140,140,140),anchor="ma")
    pop(img,t,a,dr,760,835)
def notif(img,t,a):
    def dr(l):
        box=[560,1090,900,1200]; tmp=Image.new("RGBA",img.size,(0,0,0,0)); shadow_card(tmp,box,22,(252,250,247)); l.alpha_composite(tmp); d=ImageDraw.Draw(l)
        icon(d,580,1118,46); d.text((642,1116),"Arbeiterkammer",font=F(I7,22),fill=INK); d.text((642,1148),"Eredmény kész  ✓",font=F(I5,20),fill=(52,168,90))
    pop(img,t,a,dr,730,1145)
def comment_bar(img,t,a,word):
    def dr(l):
        y=1250; box=[120,y,880,y+84]; tmp=Image.new("RGBA",img.size,(0,0,0,0)); shadow_card(tmp,box,42,(255,255,255)); l.alpha_composite(tmp); d=ImageDraw.Draw(l)
        d.ellipse([140,y+16,192,y+68],fill=(214,190,170)); n=int(len(word)*clamp((t-a-0.4)/0.6))
        d.text((212,y+24),word[:n],font=F(I7,30),fill=INK); d.text((850,y+26),"Post",font=F(I6,28),fill=(56,120,240),anchor="ra")
    pop(img,t,a,dr,500,1292)
def frame(t,bg):
    zoom=1+0.05*t/DUR; b=bg.resize((int(W*zoom),int(H*zoom)),Image.BILINEAR); ox=(b.width-W)//2; oy=(b.height-H)//2; b=b.crop((ox,oy,ox+W,oy+H))
    a=np.asarray(b).astype(np.float32)*vig*topg; a+=rng.normal(0,7,(H,W,1)); img=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert("RGBA")
    if t<7.4:
        serif_line(img,t,0.1,"Mennyi marad",400); serif_line(img,t,0.35,"a bruttóból?",500); hand_line(img,t,1.0,"(és ezt kevesen tudják…)",610)
        prompt_bar(img,t,1.8,"számold ki: 2000 € bruttó → nettó")
        mac_window(img,t,3.6,[("Bruttó","2 000 €"),("Tartomány","Steiermark"),("Ingázás","40 km")],[4.0,4.35,4.7])
        dark_badge(img,t,5.1); notif(img,t,6.3)
    else:
        serif_line(img,t,7.5,"Mentsd el,",430); serif_line(img,t,7.75,"hogy meglegyen…",530); hand_line(img,t,8.2,"(jól jön még)",640)
        comment_bar(img,t,8.4,"NETTÓ")
    return img.convert("RGB")
only=[float(x) for x in sys.argv[1:]]
wr=None if only else subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1080x1920","-r","30","-i","-","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","silent.mp4"],stdin=subprocess.PIPE)
for n in range(int(DUR*FPS)):
    buf=rd.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    t=n/FPS
    if only and not any(abs(t-o)<0.017 for o in only): continue
    im=frame(t,Image.frombytes("RGB",(W,H),buf))
    if only: im.save(f"d_{t:05.2f}.jpg",quality=85)
    else: wr.stdin.write(im.tobytes())
if wr: wr.stdin.close(); wr.wait()
