import pyautogui
resolution = pyautogui.size()
width = resolution[0]
height = resolution[1]
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import (Color, Ellipse, Rectangle,Line)


class change_size(Button):
    def __init__(self,painter,curent_color,change_bright,**kwargs):

        self.curent_color = curent_color
        self.painter = painter
        self.change_bright = change_bright

        self.bright = 1    #прозрачность по умолчанию

        super(change_size,self).__init__(**kwargs)

        #создание кружочка для показа текущего размера кисти
        with self.canvas:
            self.size_ellipse = Ellipse(pos=(width/1.025,(height/4.75)),size= (3,3))   #центральная позиция кружка меняется для того чтобы он был ровно посередине

    def on_touch_move(self,click):
        #меняем положение кружка текущего размера кисти
        with self.canvas:
            self.size_ellipse.size = (self.painter.size_line*2,self.painter.size_line*2)
            self.size_ellipse.pos = (width/1.025-self.painter.size_line/2,height/4.75-self.painter.size_line/2)


        if click.x > width/1.13 and click.x < width/1.05:
            if click.y > height/4.9 and click.y < height/4.1:

                self.painter.color_save(self.curent_color)    #сохраняем цвет чтоб прога не лагала

                self.painter.size_line = (click.x -width/1.14)/8     #вычесление нового размера кисти
                self.pos = (click.x-10,self.pos[1])
                self.painter.size[0] = width/ 1.155 - self.painter.size_line



    def touch(self,instance,state):
        mouse = pyautogui.position()
        self.mouse = pyautogui.position()
        if mouse[0] > width/1.13 and mouse[0] < width/1.05:
            if height - mouse[1] > height/4.9 and height - mouse[1] < height/4.1:
            #когда мышь нажата на кнопку цвет кисти сохраняется и временно изменяется на белый т.к с полупрозрачным цветом прога лагает
                if state == 'down':

                        self.painter.color_save(self.curent_color)

                        self.pos = (mouse.x-10,self.pos[1])

                #если произошло отжатие мыши то цвет кисти приобретает цвет загруженный раннее
                if state == 'normal':
                    self.painter.color_load()

            #сохраняем цвет еще раз на случай если пользователь очистит холст
                    self.painter.change_color(self.curent_color,self.change_bright.bright)


class change_bright(Button):
    def __init__(self,painter, curent_color,**kwargs):
        self.painter = painter
        self.curent_color = curent_color

        self.bright = 1
        super(change_bright,self).__init__(**kwargs)
        with self.canvas:
    	    
            self.bright_rect = Rectangle(pos=(width/1.02,height/6.5)
    	    	,size=(30,30))


    def on_touch_move(self,click):

            if click.x > width/1.13 and click.x < width/1.05:
                if  click.y > height/7 and  click.y < height/5:
                    self.painter.color_save(self.curent_color)
                    self.bright = (click.x-width/1.135)/125

                    self.change_rect_bright()

                    self.pos = (click.x-10,self.pos[1])

    			

    def touch(self,instance,state):
        mouse = pyautogui.position()
        if mouse[0] > width / 1.13 and mouse[0] < width / 1.05:
            if height - mouse[1] > height / 8 and height - mouse[1] < height / 4:
                #здесь все тоже самое что с ползунком от размера кисти
                if state == 'down':
                        self.painter.color_save(self.curent_color)
                        self.pos = (mouse.x-10,self.pos[1])

                if state == 'normal':

                    self.painter.color_load()

                    self.painter.color_save(self.curent_color,self.bright)
                    self.painter.change_color(self.curent_color,self.bright)


    def change_rect_bright(self):
        self.canvas.remove(self.bright_rect)
        with self.canvas:
            Color(1,1,1,self.bright)

            self.bright_rect = Rectangle(pos=(width/1.02,height/6.5),
                size=(30,30))
