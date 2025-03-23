from pygame import*
from random import*

font.init()
mixer.init()

mixer.music.load("theme.ogg")
mixer.music.play(-1)
volume=1
mixer.music.set_volume(0)
clock = time.Clock()

sw=800
sh=600

money=0
distance=0.01

mode="main"

buttonb="button.png"
buttonb2="button2.png"

menu_arrow1="button arrow.png"
menu_arrow1_m_one="button arrow2.png"

menu_arrow2="button arrow1.png"
menu_arrow2_m_one="button arrow12.png"

standart_x,standart_y=(sw/2)-100,(sh/2)-80
screen=display.set_mode((sw,sh))
display.set_caption("CARS")

def screen_mode():
    global background
    if mode=="main":
        back="background_main.png"
    elif mode=="menu":
        back="background_menu.png"
    elif mode=="choose":
        back="background_choose_option.png"
    elif mode=="game":
        back="background_game.png"
    background = transform.scale(image.load(back), (sw, sh))

class Running_obj(sprite.Sprite):
    def __init__(self,filename,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(filename),(w,h))
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        self.rect=self.image.get_rect(topleft=(x,y))
        self.kmph=5
        self.previous_y=None
    def go_up(self,obj):
        if Rect.colliderect(self.rect,obj.rect):
            print("loose")
        var=[275,405]
        if self.rect.bottom < 0:
            self.rect.y = randint(650,1000)
            self.rect.x = choice(var)

        print(obj.speed)
        if obj.speed>1:
            self.rect.y+=9.8+obj.speed/100
        if obj.speed>=50 and self.rect.y>sh+randint(100,200):
            self.rect.x=choice(var)
            self.rect.y=randint(200,400)*(-1)
        keys=key.get_pressed()
        if not keys[K_UP]:
            self.rect.y-=randint(1,2)
        if obj.speed>10 and keys[K_UP]:
            self.rect.y+=3
            
    def lets_go(self):
        screen.blit(self.image,self.rect)
        keys=key.get_pressed()
        self.rect.y+=3
        if keys[K_DOWN]:
            if self.kmph>=5:
                self.kmph-=2

        if keys[K_UP]:
            self.rect.y+=self.kmph
            if self.kmph<40:
                self.kmph+=1
        if not keys[K_UP] and self.kmph>5:
            self.rect.y+=self.kmph
            self.kmph-=self.kmph/50

        if self.rect.bottom>=sh+900:
            self.rect.y=-900

road1=Running_obj("road.png",350,900,(sw/2)-175,-1800) 
road=Running_obj("road.png",350,900,(sw/2)-175,0) 
road2=Running_obj("road.png",350,900,(sw/2)-175,-900) 

skins_npc=["npc car1.png","npc car2.png","npc car3.png","npc car4.png","npc car5.png","npc car6.png"]
npc=sprite.Group()
for i in range(randint(2,4)):
    npc_car=Running_obj(choice(skins_npc),120,200,randint(300,500),randint(600,900))
    npc.add(npc_car)

npc2=sprite.Group()
for i in range(randint(2,5)):
    npc_car=Running_obj(choice(skins_npc),120,200,randint(300,500),randint(10,200))
    npc.add(npc_car)

class BUTTON():
    def __init__(self,text,filename,filename2,w,h,x,y,click_sound=None):
        self.text=text
        self.image=transform.scale(image.load(filename),(w,h))
        self.image2=transform.scale(image.load(filename2),(w,h))
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mouse_on=False
        if click_sound:
            self.sound=mixer.Sound(click_sound)

    def draw(self):
        if self.mouse_on:
            current=self.image2
        else:
            current=self.image
        screen.blit(current,(self.rect.topleft))

        font1=font.Font(None,37)
        t=font1.render(self.text,True,(0,0,0))
        t_rect=t.get_rect(center=self.rect.center)
        screen.blit(t,t_rect)

    def check_mouse(self,mouse_pos):
        self.mouse_on=self.rect.collidepoint(mouse_pos)

    def clicksound(self):
        self.sound.play()

    def change(self,list_of_cars):
        for i in list_of_cars:
            i.x-=standart_x

    def change2(self,list_of_cars):
        for i in list_of_cars:
            i.x+=standart_x

play_button=BUTTON("PLAY",buttonb,buttonb2,140,80,330,100,"click.ogg")
leave_button=BUTTON("QUIT",buttonb,buttonb2,140,80,330,500,"click.ogg")
money_icon=BUTTON(str(money),"money icon.png","money icon.png",140,50,700,50)
left_button=BUTTON("",menu_arrow1,menu_arrow1_m_one,100,100,50,(sh/2-50),"click.ogg")
right_button=BUTTON("",menu_arrow2,menu_arrow2_m_one,100,100,sw-150,(sh/2-50),"click.ogg")

back_button=BUTTON("BACK",buttonb,buttonb2,140,80,40,500,"click.ogg")
gamemode1_button=BUTTON("","trlight.png","trlight2.png",150,150,330,250,"click.ogg")

class Car():
    def __init__(self,main_image,upper_view,t_left,t_right,w,h,x,y,w2,h2,g_x,g_y):
        self.image=transform.scale(image.load(main_image),(w,h))
        self.w=w
        self.h=h
        self.w2=w2
        self.h2=h2
        self.main=main_image
        self.upper=upper_view
        self.left=t_left
        self.right=t_right
        self.x=x
        self.y=y
        self.g_x=g_x
        self.g_y=g_y
        self.rect=self.image.get_rect()
        self.rect.x=g_x
        self.rect.y=g_y
        self.speed=0

    def show(self):
        self.image=transform.scale(image.load(self.main),(self.w,self.h))
        screen.blit(self.image,(self.x,self.y))

    def drive(self,speed):
        self.image=transform.scale(image.load(self.upper),(self.w2,self.h2))
        keys=key.get_pressed()
        if keys[K_DOWN] and self.speed>0:
            self.speed-=(self.speed/10)
        if keys[K_UP] and self.speed<130:
            self.speed+=1
        else:
            if self.speed>10:
                self.speed-=0.8
        if keys[K_LEFT] and self.rect.x>0:
            self.image=transform.scale(image.load(self.left),(self.w,self.h))
            self.rect.x-=speed
        if keys[K_RIGHT] and self.rect.x<sw-self.w:
            self.image=transform.scale(image.load(self.right),(self.w,self.h))
            self.rect.x+=speed
        screen.blit(self.image,self.rect)

car_Acura=Car("acura nsx.png","acura upper view.png","acura left.png","acura right.png",200,150,standart_x,standart_y,220,220,standart_x-10,sh/2+50)
car_Corvette=Car("corvette c8.png","corvette upper view.png","corvette left.png","corvette right.png",200,150,standart_x*2,standart_y,120,180,standart_x+40,sh/2+50)
car_Ferrari=Car("laferari.png","ferrari upper view.png","ferrari left.png","ferrari right.png",210,90,standart_x*3,standart_y+30,150,200,standart_x+10,sh/2+50)

list_of_cars=[car_Acura,car_Corvette,car_Ferrari]

def text(text,size,x,y):
    font2=font.Font(None,size)
    t=font2.render(text,True,(0,0,0))
    screen.blit(t,(x,y))

def for_main():
    play_button.rect.x,play_button.rect.y=330,400
    play_button.draw()
    leave_button.draw()

def for_menu():
    for i in list_of_cars:
        i.show()
    play_button.draw()
    back_button.draw()
    money_icon.draw()
    left_button.draw()
    right_button.draw()
    play_button.rect.x,play_button.rect.y=620,500

def for_choose():
    back_button.draw()
    gamemode1_button.draw()

def for_game():
    for i in list_of_cars:
        if i.x==standart_x:
            main_car=i
    speed_icon=BUTTON(str(int(main_car.speed)),"speed icon.png","speed icon.png",140,50,0,50)
    distance_icon=BUTTON("km "+str(distance),"speed icon.png","speed icon.png",140,50,0,110)
    speed_icon.draw()
    distance_icon.draw()
    road1.lets_go()
    road.lets_go()
    road2.lets_go()
    main_car.drive(20)
    npc.update()
    npc.draw(screen)
    npc2.update()
    npc2.draw(screen)
    for npc_car in npc:
        npc_car.go_up(main_car)
    for npc_car in npc2:
        npc_car.go_up(main_car)

run=True
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        if e.type == MOUSEMOTION:
            play_button.check_mouse(e.pos)
            leave_button.check_mouse(e.pos)
            back_button.check_mouse(e.pos)
            left_button.check_mouse(e.pos)
            right_button.check_mouse(e.pos)
            gamemode1_button.check_mouse(e.pos)

        if e.type==MOUSEBUTTONDOWN:
            x,y=e.pos
            if leave_button.rect.collidepoint(x,y) and mode=="main":
                quit()
            if play_button.rect.collidepoint(x,y) and mode!="choose" and mode!="game":
                play_button.clicksound()
                mode="menu"
                if play_button.rect.x!=330:
                    mode="choose"
            if back_button.rect.collidepoint(x,y) and mode!="main" and mode!="game":
                back_button.clicksound()
                if mode!="choose":
                    mode="main"
                if mode=="choose":
                    mode="menu"
            if left_button.rect.collidepoint(x,y) and mode!="main" and mode!="game" and mode!="choose":
                leave_button.clicksound()
                left_button.change2(list_of_cars)
            if right_button.rect.collidepoint(x,y) and mode!="main" and mode!="game" and mode!="choose":
                right_button.clicksound()
                right_button.change(list_of_cars)
            if gamemode1_button.rect.collidepoint(x,y) and mode!="main" and mode!="menu" and mode!="game":
                gamemode1_button.clicksound()
                mode="game"
                
    screen_mode()

    screen.blit(background,(0,0))

    if mode=="main":
        for_main()
    if mode=="menu":
        for_menu()
    if mode=="choose":
        for_choose()
    if mode=="game":
        for_game()

    display.update()
    
    clock.tick(60)