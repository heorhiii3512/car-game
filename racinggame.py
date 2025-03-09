from pygame import*

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

mode="main"

buttonb="button.png"
buttonb2="button2.png"

menu_arrow1="button arrow.png"
menu_arrow1_m_one="button arrow2.png"

menu_arrow2="button arrow1.png"
menu_arrow2_m_one="button arrow12.png"

standart_x,standart_y=(sw/2)-100,(sh/2)-100
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

class Image():
    def __init__(self,filename,w,h,x,y):
        self.image=transform.scale(image.load(filename),(w,h))
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        self.rect=self.image.get_rect(topleft=(x,y))

    def show(self):
        screen.blit(self.image,self.rect)
        self.rect.y+=5
        if self.rect.y>=sh:
            self.rect.y=-600

road=Image("road.png",250,600,(sw/2)-125,0)    
road1=Image("road.png",250,600,(sw/2)-125,-600)
road2=Image("road.png",250,600,(sw/2)-125,-1200)

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

play_button=BUTTON("PLAY",buttonb,buttonb2,140,80,330,100,"click.ogg")
leave_button=BUTTON("QUIT",buttonb,buttonb2,140,80,330,500,"click.ogg")

left_button=BUTTON("",menu_arrow1,menu_arrow1_m_one,100,100,50,(sh/2-50),"click.ogg")
right_button=BUTTON("",menu_arrow2,menu_arrow2_m_one,100,100,sw-150,(sh/2-50),"click.ogg")

back_button=BUTTON("BACK",buttonb,buttonb2,140,80,40,500,"click.ogg")
gamemode1_button=BUTTON("","trlight.png","trlight2.png",150,150,330,250,"click.ogg")

class Car():
    def __init__(self,main_image,upper_view,t_left,t_right,w,h,x,y,speed):
        self.image=transform.scale(image.load(main_image),(w,h))
        self.w=w
        self.h=h
        self.main=main_image
        self.upper=upper_view
        self.left=t_left
        self.right=t_right
        self.x=x
        self.y=y
        self.speed=speed
        self.rect=self.image.get_rect()

    def show(self):
        self.image=transform.scale(image.load(self.main),(self.w,self.h))
        screen.blit(self.image,(standart_x,standart_y))

    def drive(self,speed):
        self.image=transform.scale(image.load(self.upper),(self.w,self.h))
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>0:
            self.image=transform.scale(image.load(self.left),(self.w,self.h))
            self.rect.x-=speed
        if keys[K_RIGHT] and self.rect.x<sw-self.w:
            self.image=transform.scale(image.load(self.right),(self.w,self.h))
            self.rect.x+=speed
        screen.blit(self.image,self.rect)
   
car_Acura=Car("acura nsx.png","acura upper view.png","acura left.png","acura right.png",200,120,standart_x,standart_y,3)

def text(text,size,x,y):
    font2=font.Font(None,size)
    t=font2.render(text,True,(0,0,0))
    screen.blit(t,(x,y))

def for_main():
    play_button.rect.x,play_button.rect.y=330,400
    play_button.draw()
    leave_button.draw()

def for_menu():
    car_Acura.show()
    play_button.draw()
    back_button.draw()
    text(str(money),50,750,20)
    left_button.draw()
    right_button.draw()
    play_button.rect.x,play_button.rect.y=620,500

def for_choose():
    back_button.draw()
    gamemode1_button.draw()

def for_game():
    road1.show()
    road.show()
    car_Acura.drive(20)

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
            if right_button.rect.collidepoint(x,y) and mode!="main" and mode!="game" and mode!="choose":
                right_button.clicksound()
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
    
    clock.tick(45)