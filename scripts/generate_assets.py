"""Generate original diagram-style animations; these are not model outputs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import random

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
INK = '#30332e'
PAPER = '#faf7ee'
RUST = '#a94e3c'
SAGE = '#b9c7a5'
PINK = '#e3b4a6'
GOLD = '#e5cc91'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

def font(size, serif=False):
    return ImageFont.truetype(SERIF if serif else FONT, size)

def canvas():
    image = Image.new('RGB', (640, 300), PAPER)
    draw = ImageDraw.Draw(image)
    for x in range(20, 640, 24):
        for y in range(18, 300, 24):
            draw.ellipse((x, y, x+1, y+1), fill='#e3dfd3')
    return image, draw

def arrow(draw, start, end, fill=INK):
    draw.line([start, end], fill=fill, width=2)
    x, y = end
    a = math.atan2(y-start[1], x-start[0])
    points = [(x-9*math.cos(a-.5), y-9*math.sin(a-.5)), end,
              (x-9*math.cos(a+.5), y-9*math.sin(a+.5))]
    draw.line(points, fill=fill, width=2)

def mule(frame):
    image, draw = canvas()
    nodes = [(90,100),(210,56),(206,174),(335,125),(462,59),(475,192),(568,113),(332,235),(85,227)]
    edges = [(0,1),(0,2),(0,8),(1,2),(1,3),(2,3),(2,7),(3,4),(3,5),(3,7),(4,6),(5,6),(5,7),(7,8)]
    for a, b in edges:
        draw.line([nodes[a],nodes[b]], fill='#b9bcae', width=2)
    path = [0,2,3,5,6]
    for a,b in zip(path,path[1:]):
        draw.line([nodes[a],nodes[b]], fill=RUST,width=3)
    progress=(frame/48*4)%4
    index=int(progress)
    a,b=nodes[path[index]],nodes[path[index+1]]
    t=progress-index
    x,y=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t
    draw.ellipse((x-7,y-7,x+7,y+7), fill=RUST)
    for i,(x,y) in enumerate(nodes):
        highlight=i==3
        r=24 if highlight else 17
        draw.ellipse((x-r,y-r,x+r,y+r),fill=PINK if highlight else PAPER,outline=INK,width=2)
        draw.ellipse((x-4,y-8,x+4,y),outline=INK,width=2)
        draw.arc((x-10,y-1,x+10,y+13),180,360,fill=INK,width=2)
        if highlight:
            radius=32+int(5*math.sin(frame*math.pi/24))
            draw.arc((x-radius,y-radius,x+radius,y+radius),20,320,fill=RUST,width=2)
    draw.rounded_rectangle((365,253,566,282),radius=4,fill=PAPER,outline=INK,width=1)
    draw.text((377,260),'flag for review',font=font(15),fill=INK)
    draw.text((25,18),'connect the dots',font=font(15),fill=INK)
    arrow(draw,(385,246),(350,161),RUST)
    return image

def llm(frame):
    image,draw=canvas()
    draw.text((25,18),'one thought, one token',font=font(15),fill=INK)
    draw.rounded_rectangle((34,89,186,210),radius=8,fill='#e8ecdf',outline=INK,width=2)
    draw.text((50,105),'hello,',font=font(23,True),fill=INK)
    draw.text((50,143),'world',font=font(23,True),fill=INK)
    for i in range(3): draw.line((49,181+i*8,130-i*13,181+i*8),fill='#97a08b',width=2)
    arrow(draw,(197,150),(243,150))
    draw.rounded_rectangle((260,99,376,195),radius=15,fill=SAGE,outline=INK,width=3)
    draw.line((318,98,318,76),fill=INK,width=2)
    draw.ellipse((312,64,324,76),fill=GOLD,outline=INK,width=2)
    draw.rounded_rectangle((273,116,363,159),radius=9,fill=PAPER,outline=INK,width=2)
    if frame in (21,22,23):
        draw.line((288,137,300,137),fill=INK,width=3);draw.line((337,137,349,137),fill=INK,width=3)
    else:
        draw.ellipse((290,129,300,142),fill=INK);draw.ellipse((337,129,347,142),fill=INK)
    draw.arc((303,163,333,180),0,180,fill=INK,width=2)
    draw.rounded_rectangle((250,128,260,163),radius=3,fill=PAPER,outline=INK,width=2)
    draw.rounded_rectangle((376,128,386,163),radius=3,fill=PAPER,outline=INK,width=2)
    draw.text((260,218),'12 blocks',font=font(14),fill=INK)
    arrow(draw,(395,150),(437,150))
    tokens=['a','new','idea.']
    count=1+min(2,int(frame/13))
    for i,token in enumerate(tokens):
        y=84+i*53
        visible=i<count
        draw.rounded_rectangle((454,y,601,y+40),radius=6,fill=GOLD if visible else PAPER,outline=INK if visible else '#c9c8bc',width=2)
        if visible: draw.text((473,y+9),token,font=font(20),fill=INK)
        elif i==count: draw.text((474,y+10),'...',font=font(18),fill='#b0b3a5')
    draw.text((216,270),'predict → learn → repeat',font=font(14),fill=INK)
    return image

random.seed(12)
noise = [random.random() for _ in range(28*28)]
digit = Image.new('L',(112,112),0)
dd=ImageDraw.Draw(digit)
dd.line([(24,27),(87,25),(64,56),(49,96)],fill=255,width=10)
dd.line([(40,60),(78,57)],fill=255,width=6)
digit=digit.resize((28,28),Image.Resampling.LANCZOS)
target=list(digit.getdata())

def diffusion(frame):
    image,draw=canvas()
    draw.text((25,18),'finding shape in the noise',font=font(15),fill=INK)
    t=min(1,frame/36)
    for col,mix in enumerate([0,t*.55,t]):
        x=45+col*205
        draw.rounded_rectangle((x-8,74,x+120,202),radius=9,fill=PAPER,outline=INK,width=2)
        for i,(n,value) in enumerate(zip(noise,target)):
            v=int((n*(1-mix)+value/255*mix)*205)
            c=(246-v,242-v,229-v)
            px=x+(i%28)*4;py=82+(i//28)*4
            draw.rectangle((px,py,px+3,py+3),fill=c)
        draw.text((x+8,219),['noise','denoise','a digit'][col],font=font(17),fill=INK)
        if col<2: arrow(draw,(x+132,139),(x+178,139))
    draw.line((162,271,476,271),fill='#c9c8bc',width=3)
    draw.line((162,271,162+int(314*t),271),fill=RUST,width=3)
    draw.ellipse((157+int(314*t),266,167+int(314*t),276),fill=RUST)
    return image

for name,draw_frame,poster in [('mule',mule,12),('llm',llm,40),('diffusion',diffusion,40)]:
    frames=[draw_frame(frame) for frame in range(48)]
    frames[poster].save(ASSETS/f'{name}-still.png',optimize=True)
    palette=frames[poster].quantize(colors=96)
    indexed=[image.quantize(palette=palette,dither=Image.Dither.NONE) for image in frames]
    indexed[0].save(ASSETS/f'{name}.gif',save_all=True,append_images=indexed[1:],duration=85,loop=0,optimize=True,disposal=2)
    print(name,(ASSETS/f'{name}.gif').stat().st_size)

social=Image.new('RGB',(1200,630),'#f5f1e8')
d=ImageDraw.Draw(social)
d.text((67,51),'PRIYANSHI GOYAL',font=font(18),fill=RUST)
d.text((64,92),'A little curiosity',font=font(65,True),fill=INK)
d.text((64,169),'goes a long way.',font=font(65,True),fill=INK)
d.text((69,267),'AI RESEARCH / GENERATIVE MODELS / COMPUTER VISION',font=font(16),fill=INK)
for i,(name,color,label) in enumerate([('mule',PINK,'GRAPH ML'),('llm',SAGE,'LANGUAGE'),('diffusion',GOLD,'DIFFUSION')]):
    x=69+i*357
    d.rounded_rectangle((x,333,x+324,544),radius=22,fill=color,outline=INK,width=3)
    thumb=Image.open(ASSETS/f'{name}-still.png').resize((290,136),Image.Resampling.LANCZOS)
    social.paste(thumb,(x+17,352))
    d.text((x+20,507),label,font=font(17),fill=INK)
    for wx in [x+53,x+270]:d.ellipse((wx-17,528,wx+17,562),fill=PAPER,outline=INK,width=3)
    if i<2:d.line((x+325,528,x+356,528),fill=INK,width=4)
d.line((50,566,1150,566),fill=INK,width=2)
d.text((72,589),'COME ABOARD THE PROJECT EXPRESS →',font=font(14),fill=INK)
social.save(ASSETS/'social-preview.png',optimize=True)
