from kivy.graphics import (Color, Ellipse,Triangle, Rectangle,Line)

from kivy.uix.widget import Widget
from kivy.uix.label import Label 
from kivy.uix.button import Button 


from painter_objects import MakeTriangle, MakeSquare, MakeEllipse, graphic_function
import copy

import pyautogui
import math
from shapely.geometry import LineString


width,height = pyautogui.size()

cell = 20  #размер клетки заднего фона в пикселях
amount_cell = 50

class painter(Widget):
	def __init__(self,App_window,**kwargs):
		super(painter,self).__init__(**kwargs)
        
		self.App_window = App_window

		self.size_line = 2
		self.filling = False	#заливка фигур по дефолту нет
		self.canvas_width = math.ceil( width/1.155)  # Ширина холста
		self.canvas_height = math.ceil(height/1.2)  # Высота холста
		self.size_hint = (None, None)  # Отключаем автоматическое изменение размеров
		self.size = (self.canvas_width, self.canvas_height) 
		self.pos = (0,height/4)


		self.count = 0
		self.drawing_accept = True
		self.new_line_needed = None
		self.background = []
		self.segments = []
		self.mode = 'pencil'	#первоначально устанавливается режим кисти

		self.all_objects = []   #для хранения текущих обьектов на экране
		self.colors = []    #для хранения использованных цветов
		self.deleted_objects = []    #для хранения удаленных с экрана обьектов отдельно
		self.colors_deleted_objects = []    #для хранения цветов удаленных обьектов

		self.functions =[]
		self.segments = []
		self.dots = []

		self.gui  = []
		self.generals_active = False

		self.list_count = 0

		self.strings = []

		self.Y_axis = None
		self.biasY = 0
		self.biasX = 0


		self.list = Button(disabled= True,
							background_disabled_normal= '',
							background_color= (0,0,0,0.3),
							size = (150,-200),
							pos = (self.width - (self.width - self.canvas_width )-140, height))


		self.graphics_manager = graphic_function(self.canvas_width,self.canvas_height,cell,self.canvas)

		self.y_coord_Xaxis = height - self.canvas_height + self.canvas_height/2 - 4		#высота для оси х
		self.x_coord_Yaxis =  self.canvas_width/2 - 4		#координата х для оси у

		self.acceptable_x = (cell * amount_cell) - self.canvas_width/2-100
		self.acceptable_y = (cell * amount_cell ) - self.canvas_height/2



	def on_touch_down(self,click):

		#если курсор находится в зоне холста
		if  self.collide_point(*click.pos)  and self.drawing_accept:

			if self.mode == 'pencil':
				with self.canvas:
					self.line = Line(points = (click.x+self.size_line/2,click.y +self.size_line/2,
												click.x+self.size_line/2,click.y +self.size_line/2+1),width = self.size_line)

					self.all_objects.append(self.line)    #сохраняем линию в список чтобы потом можно было удалить его отдельно или вернуть на экран
				

			elif self.mode == 'square':
				self.square = MakeSquare(click,self.size_line,self.filling,self.canvas)
				self.all_objects.append(self.square)

			elif self.mode == 'triangle':
				self.triangle = MakeTriangle(click,self.size_line,self.filling,self.canvas)
				self.all_objects.append(self.triangle)

			elif self.mode == 'ellipse':
				self.ellipse = MakeEllipse(click,self.size_line,self.filling,self.canvas)
				self.all_objects.append(self.ellipse)

			self.colors.append(self.curent_color)   #сохраняем цвет начатой линии в список 


	def on_touch_move(self,click) :


		if  self.collide_point(*click.pos) and self.drawing_accept:
			if self.mode == 'pencil':

				if self.new_line_needed:
					self.new_line_needed = False
					with self.canvas:
						self.line = Line(points = (),width = self.size_line)

					#сохраняем новую линию и его цвет в списки
						self.colors.append(self.curent_color)
						self.all_objects.append(self.line)

				if 4 % 3 != 0:    #регулятор частоты обновлений точек для линии(чем больше второе число тем чаще будут добавлятся новые точки)
					with self.canvas:
						self.line.points +=(click.x+self.size_line/2,click.y +self.size_line/2)

					self.count +=1


			elif self.mode == 'square':
				self.square.moving(click)

			elif self.mode == 'triangle':
				self.triangle.moving(click)

			elif self.mode == 'ellipse':
				self.ellipse.moving(click)

		#если курсор вышел за пределы холста начинаем новую линию(чтоб при возвращении курсора на холст не продолжолась предыдущая линия)
		else:
			self.new_line_needed = True







	#меняем цвет при нажатии на кнопку политры
	def change_color(self,button,bright=None):
		
		with self.canvas:
			#если до этого был полупрозрачный цвет
			if bright:
				Color(button.background_color[0],button.background_color[1],button.background_color[2],bright)

			#если прозрачность цвета не менялась
			else:
				Color(button.background_color[0],button.background_color[1],button.background_color[2],)
			

	def color_save(self,curent_color,bright=None):
		self.curent_color = copy.copy(curent_color.background_color)    #копируем цвет кнопки текущего цвета с помощью copy() чтобы мы не меняли цвет кнопки

		if (bright):
			self.curent_color[3] = bright    #если также цвет был полупрозрачным то добавляем прозрачность в скопированный цвет
			
		#with self.canvas:
			#Color(1,1,1)    #меняем цвет чтобы там не было прозрачности

	def color_load(self):
		with self.canvas:    #восстановление раннего загруженого цвета
			Color(self.curent_color[0],self.curent_color[1],self.curent_color[2],self.curent_color[3])


		#кнопка  удаления последнего созданного объекта с экрана
	def back(self):

		if len(self.all_objects)>0:

			last_object = self.all_objects.pop(-1)    #получааем последний объект

			if not(isinstance(last_object,Line)):	#если этот объект не является линией нарисованный режимом pencil
				self.canvas.remove(last_object.figure)	#каждая кастомная фигура хранится в атриуте figure экземпляра класса этой фигуры

			else:
				self.canvas.remove(last_object)

			self.deleted_objects.append(last_object)    #добавляем его в список удаленных обьектов

			self.colors_deleted_objects.append(self.colors.pop(-1))    #добавляем цвет этого обьекта в список цветов удаленных объектов

			with self.canvas:    #удалаем цвет удаленного объекта со списка цветов текущих объектов
				Color(self.curent_color[0],self.curent_color[1],self.curent_color[2],self.curent_color[3])


		#кнопка возвращения обьекта на экран
	def forward(self):


		if len(self.deleted_objects)>0 :
			color = self.colors_deleted_objects.pop(-1)    #получаем цвет которым был нарисован удаленный обьект
			self.colors.append(color)   #добавляем его в список текущих цветов

			with self.canvas:
				Color(color[0],color[1],color[2],color[3])    #устанавливаем нужный цвет


			Object = self.deleted_objects.pop(-1)	#получаем последний удаленный обьект
			if not(isinstance(Object,Line)):	#если этот объект не является линией нарисованный режимом pencil
				self.canvas.add(Object.figure)		#каждая кастомная фигура хранится в атриуте figure экземпляра класса этой фигуры

			else:
				self.canvas.add(Object)  

			self.all_objects.append(Object)    #добавляем удаленный объект в список активных объектов
			with self.canvas:
				Color(self.curent_color[0],self.curent_color[1],self.curent_color[2],self.curent_color[3])   #восстанавливаем цвет кисти



	def clear_canvas(self,button):

		self.canvas.clear()
		self.all_objects.clear()
		self.deleted_objects.clear()
		self.colors.clear()
		self.colors_deleted_objects.clear()
		self.background.clear()
		self.segments.clear()
		self.Y_axis = None
		self.graphics_manager.functions.clear()
		self.graphics_manager.dots_draw.clear()
		self.graphics_manager.generals.clear()
		self.graphics_manager.inactive_generals.clear()
		self.graphics_manager.dots.clear()

		self.strings.clear()

		for child in self.list.children:
			self.list.remove_widget(child)

		self.list.pos[1] = self.height
		self.list.size[1] = 200




		#после очищения окна заново рисуем внешний вид интерфейса
		self.recovery()


	def recovery(self,full = True):	#восстановление вида интерфейса
		with self.canvas:
			for object in self.gui:
				try:
					pass
					self.canvas.children.remove(object)
				except:
					pass
			self.gui.clear()
			if full:
				Color(0.1, 0.1, 0.1)
				Rectangle(pos=(0,0),size=(2000,1900))  #основной серый фон
				Color(1,1,1)
				Rectangle(pos=(0,height/4),size=(width/1.15,1000))    #белый холст

			else:	#здесь восстанавливаем только интерфейс без холста

				Color(0.1, 0.1, 0.1)
				self.gui.append(Rectangle(pos=(0,0),size = (width,self.pos[1])))
				self.gui.append(Rectangle(pos=(self.canvas_width+10,0),
		    				size = (1000,3000) ))

			Color(1,1,1,0.15)
			self.gui.append(Line(points=(width/1.13,height/4.5,width/1.05,height/4.5),width=5)) #линия ползунка смены размера кисти
			self.gui.append(Line(points=(width/1.13,height/6.2,width/1.05,height/6.2),width=5)) #линия ползунка смены прозрачности


		self.color_load()    #восстанавливаем цвет кисти т.к. для восстановления окна мы меняли ее цвет


	def draw_backgrounds(self):	# рисует клетчатый фон
		self.background = []
		self.recovery_coordinations()

		with self.canvas:
			Color(0,0,0,0.3)
			for x_line_coord in range(0,cell*amount_cell,cell):
				line = Line(points=(cell*amount_cell*(-1)+self.x_coord_Yaxis,self.y_coord_Xaxis + x_line_coord,cell*amount_cell+self.x_coord_Yaxis, self.y_coord_Xaxis + x_line_coord))
				line1 = Line(points=(cell*amount_cell*(-1)+self.x_coord_Yaxis,self.y_coord_Xaxis - x_line_coord ,cell*amount_cell+self.x_coord_Yaxis,self.y_coord_Xaxis - x_line_coord ))

				self.background += [line,line1]

			for y_line_coord in range(0,cell*50,cell):
				line = Line(points=(self.x_coord_Yaxis + y_line_coord,cell*amount_cell+ self.y_coord_Xaxis,self.x_coord_Yaxis + y_line_coord,cell*amount_cell*(-1) + self.y_coord_Xaxis))
				line1 = Line(points=(self.x_coord_Yaxis - y_line_coord, cell*amount_cell+ self.y_coord_Xaxis, self.x_coord_Yaxis - y_line_coord, cell*amount_cell*(-1) + self.y_coord_Xaxis))
				self.background += [line,line1]

		self.recovery(full=False)



	def remove_background(self):
		for line in self.background:
			self.canvas.remove(line)



	def draw_axis(self):	#рисует координатную плоскость
		self.recovery_coordinations()
		with self.canvas:
			Color(0,0,0)
			self.X_axis = Line(points = (-10000,self.y_coord_Xaxis,10000,self.y_coord_Xaxis),width = 3)
			self.Y_axis = Line(points = (self.x_coord_Yaxis,-10000,self.x_coord_Yaxis,10000),width = 3)
			self.recovery(full=False)

		self.color_load()

	def remove_axis(self):
		if self.Y_axis: 
			self.canvas.remove(self.X_axis)
			self.canvas.remove(self.Y_axis)



	def draw_segments(self):	#рисует еденичные отрезки
		self.recovery_coordinations()
		self.segments = []
		y_coord_Xaxis = height - self.canvas_height + self.canvas_height/2 + 5
		x_coord_Yaxis =  self.canvas_width/2 +5
		for x in range(cell*amount_cell*(-1),cell*amount_cell,cell):

			segment = Label(text = str(int(x/cell)),color=(0,0,0),center_x = x + self.canvas_width/2,
							center_y = y_coord_Xaxis,font_size=10 )

			self.segments.append(segment)
			self.add_widget(segment)

		for y in range(cell*amount_cell*(-1),cell*amount_cell,cell):

			segment = Label(text = str(int(y/cell)),color=(0,0,0),center_x = x_coord_Yaxis ,
							center_y = y  + self.canvas_height/2 + (height-self.canvas_height),font_size=10 )

			self.segments.append(segment)
			self.add_widget(segment)
		self.recovery(full= False)


	def remove_segments(self):
		for segment in self.segments:
			self.remove_widget(segment)



	def draw_dots(self):
		self.recovery_coordinations()
		with self.canvas:
			self.graphics_manager.draw_dots()

	def remove_dots(self):
		self.graphics_manager.remove_dots()


	def draw_generals(self):
		self.recovery_coordinations()
		with self.canvas:
			if len(self.graphics_manager.functions) >1:
				self.generals_active = True

				self.graphics_manager.draw_general_dots()

				self.color_load()
				self.recovery(full=False)

	def remove_generals(self):
		self.generals_active = False
		self.graphics_manager.remove_generals()


	def draw_function(self,function,dots):
		self.color_load()
		self.recovery_coordinations()

		self.functions = self.graphics_manager.new_function(function,dots)



	def draw_list(self):
		if not(self.list in self.children): 
			self.App_window.add_widget(self.list)
		for string in self.strings:
			try:
				self.App_window.add_widget(string)
			except:
				pass

	def remove_list(self):
		self.App_window.remove_widget(self.list)
		for string in self.strings:
			self.App_window.remove_widget(string)


	def add_string_in_line(self,string):

		if len(string) >= 8:
			font_size = 25 - len(string)  /2

		else:
			font_size = 25

		string = (Label(text = string,font_size = font_size,color = self.curent_color,
									x = self.list.pos[0]+15 + len(string)*5,
									center_y = height-15 - self.list_count*30))

		string1 = (Label(text = 'f(x):',font_size = font_size,color = self.curent_color,x = self.list.pos[0]-20 ,
									center_y = height-15 - self.list_count*30))

		self.App_window.add_widget(string)
		self.App_window.add_widget(string1)


		self.strings.append(string)
		self.strings.append(string1)


		if len(self.strings) > 6*2 :
			self.list.size[1] -= 25


		self.list_count +=1

	def move_accept(self,x,y):
		if self.acceptable_y* (-1) > self.biasY :
			if not(y <0):
				y = 0

		if self.acceptable_y <= self.biasY :
			if not(y >0):
				y = 0
		if self.acceptable_x* (-1) > self.biasX :
			if not(x <0):
				x = 0

		if self.acceptable_x < self.biasX :
			if not(x >0):
				x = 0
		self.move(x,y)



	def move(self,x,y):
		with self.canvas:
			self.biasX -=x
			self.biasY -=y
			for object in self.all_objects + self.background:

				if not(isinstance(object,Line)):

					object.move_directly(x,y)

				else:
					count = 0
					new_pos = []
					with self.canvas:
						for pos in object.points:
							if count %2 ==0:
								new_pos.append( pos + x)

							else:
								 new_pos.append( pos + y)

							object.points = new_pos
							count +=1
			if self.Y_axis:
				pos = self.X_axis.points
				self.X_axis.points = [pos[0]+x,pos[1]+y,pos[2]+x,pos[3]+y]

				pos = self.Y_axis.points
				self.Y_axis.points = [pos[0]+x,pos[1]+y,pos[2]+x,pos[3]+y]

			for graphic in self.functions:
				for segment in graphic:
					new_pos = []
					count =0
					for coord in segment.points:

						if count %2 ==0:
								new_pos.append( coord + x)

						else:
							new_pos.append( coord + y)
						count +=1

					segment.points = new_pos

			if self.segments:
				for segment in self.segments:
					segment.center_x += x
					segment.center_y += y
			for general in self.graphics_manager.generals:
				general  .pos = [general  .pos[0] + x, general  .pos[1] + y]

			for dot in self.graphics_manager.dots_draw:
				if not(isinstance(dot,Line)):

					dot.pos = [dot.pos[0]+x,dot.pos[1]+y]
				else:
					dotE = dot.ellipse
					dot.ellipse = [dotE[0]+x,dotE[1]+y,dotE[2],dotE[3]]
			self.recovery(full=False)

	def recovery_coordinations(self):
		self.move(self.biasX,self.biasY)
		self.biasX = 0
		self.biasY = 0