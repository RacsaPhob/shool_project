from kivy.graphics import (Color, Ellipse,Triangle, Rectangle,Line)

from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.uix.button import Button
import copy
import math

import pyautogui
from shapely.geometry import LineString
width,height = pyautogui.size()
dot_s = 8   #размер выколотых и общих точек



class graphic_function():
	def __init__(self,canvas_width,canvas_height,cell,canvas):
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.cell = cell
		self.canvas = canvas
		self.functions = []
		self.dots = []
		self.dots_draw = []
		self.generals =[]
		self.inactive_generals = []



	def new_function(self,function,dots):
		for dot in dots:
			self.dots.append(dot)
		graphic = []
		with self.canvas:
			function_line = Line(points=[],width=2)
			for x in range(0,len(function-1)-2,2):

				x_coord =(function[x] *self.cell + self.canvas_width/2 - 4)
				y_coord =(function[x+1] *self.cell + height - self.canvas_height + self.canvas_height/2 - 4)
				for dot in dots:
					if function[x+2] ==dot[0]  or function[x-2] ==dot[0]:

						graphic.append(function_line)
						function_line = Line(points=[],width=2)
						break


					if abs(function[x] - dot[0]) <0.03:

						graphic.append(function_line)
						function_line = Line(points=[],width=2)

				if function_line.points:
					if abs(y_coord-function_line.points[-1])>2000:	#на случай тригонометрической функции, которая уходит за пределы экрана и имеет вык. точки
						graphic.append(function_line)
						function_line = Line(points=[], width=2)

				function_line.points +=(x_coord,y_coord)

			graphic.append(function_line)
			self.functions.append(graphic)

		return self.functions

	def draw_general_dots(self):
		Color(1,0,0,0.8)



		firstF = self.functions[-1]
		secondF = self.functions[-2]
		for chunk in firstF:
			chunk = chunk.points
			if len(chunk) <3:
				continue
			for chunk1 in secondF:
				chunk1 = chunk1.points
				if len(chunk1) <3:
					continue
				line = []
				line1 = []
				for x in range(0,len(chunk),2):
					line.append((chunk[x],chunk[x+1]))

				for x in range(0,len(chunk1),2):
					line1.append((chunk1[x],chunk1[x+1]))

				line = LineString(line)
				line1 = LineString(line1)
				intersects = line.intersection(line1)

				#поскольку библеотека shapely как то странно работает приходится применять разные методы что бы просто перебрать корды точек
				if str(intersects)[:10] == 'MULTIPOINT' or str(intersects)[:18] =='GEOMETRYCOLLECTION':
					for intersect in intersects.geoms:
						coords = intersect.coords[0]
						dot = Ellipse(size=(dot_s,dot_s),pos=(coords[0]-dot_s/2,coords[1]-dot_s/2))
						self.generals.append(dot)

				else:
					if intersects.coords:
						coords = intersects.coords[0]
						dot = Ellipse(size=(dot_s,dot_s),pos=(coords[0]-dot_s/2,coords[1]-dot_s/2))	

						self.generals.append(dot)


	def remove_generals(self):
		for dot in self.generals:
			self.canvas.remove(dot)
			self.inactive_generals.append(dot)
		self.generals.clear()


	def draw_dots(self):
		for coords in self.dots:
			if coords[1]:
				Color(1,1,1)
				pos_y = (coords[1][0]+ coords[1][1]) /2
				pos_x = coords[0] *self.cell + self.canvas_width/2 - dot_s
				pos_y = pos_y*self.cell + height - self.canvas_height + self.canvas_height/2 - dot_s
				dot = Ellipse(size=(dot_s,dot_s),pos=(pos_x,pos_y))
				Color(0,0,0)
				circle = Line(ellipse=(pos_x,pos_y,dot_s,dot_s),width=1)
				self.dots_draw.append(dot)
				self.dots_draw.append(circle)


	def remove_dots(self):
		for dot in self.dots_draw:
			self.canvas.remove(dot)

		self.dots_draw.clear()


class moving_painter_but(Button):
	def __init__(self,App_window,painter,**kwargs):
		self.App_window = App_window
		super((moving_painter_but),self).__init__(**kwargs)
		self.widget = moving_painter_widget(painter)

	def released(self):
		if not(self.widget in self.App_window.children):
			self.App_window.add_widget(self.widget)

		else:
			self.App_window.remove_widget(self.widget)

class moving_painter_widget(Widget):

	def __init__(self,painter,**kwargs):
		super((moving_painter_widget),self).__init__(**kwargs)

		self.painter = painter

	def pressed(self,x,y):
		self.painter.move_accept(x,y)


class MakeSquare():
	def __init__(self,click,size,filling,canvas):
		self.filling = filling
		self.canvas = canvas

		with self.canvas:
			if not(filling):
				#создаем цикличную линию из четырех точек
				self.figure = Line(points=(click.x,click.y),width=size/2,close=True)

			else:
				self.figure = Rectangle(pos = (click.x,click.y),size = (0,0))


	def moving(self,pos):
		#при движении зажатой мыши изменяются соответсвующие координаты у точек линии
		with self.canvas:
			if not(self.filling):
				square = self.figure.points
				self.figure.points = (square[0],square[1],square[0],pos.y,pos.x,pos.y,pos.x,square[1])

			else:
				self.figure.size = (pos.x - self.figure.pos[0],pos.y - self.figure.pos[1])


	def move_directly(self,x,y):
		with self.canvas:
			if self.filling:
				self.figure.pos = (self.figure.pos[0]+x,self.figure.pos[1]+y)

			else:
				pos = self.figure.points
				self.figure.points = [pos[0]+x,pos[1]+y,pos[2]+x,pos[3]+y,pos[4]+x,pos[5]+y,pos[6]+x,pos[7]+y]



class MakeTriangle():
	def __init__(self,click,size,filling,canvas):
		self.filling = filling
		self.canvas = canvas

		with self.canvas:
			if not (filling):
				#создаем цикличную линию из четырех точек
				self.figure = Line(points=(click.x,click.y,click.x,click.y),width=size/2,close=True)

			else:
				self.figure = Triangle(points=[click.x,click.y, 0,0])


	def moving(self,pos):
		#при движении зажатой мыши изменяются соответсвующие координаты у точек линии
		with self.canvas:
			triangle = self.figure.points
			self.figure.points = (triangle[0],triangle[1],pos.x,triangle[1],triangle[0] + ((pos.x-triangle[0])/2),pos.y)


	def move_directly(self,x,y):
		with self.canvas:
			pos = self.figure.points
			self.figure.points = [pos[0]+x,pos[1]+y,pos[2]+x,pos[3]+y,pos[4]+x,pos[5]+y]

class MakeEllipse():
	def __init__(self,click,size,filling,canvas):
		self.filling = filling
		self.canvas = canvas

		with self.canvas:
			if not(filling):
			#создаем цикличную линию из четырех точек
				self.figure = Line(ellipse=(click.x,click.y,0,0),width=size/2)
			else:
				self.figure = Ellipse(pos=(click.x,click.y),size=(0,0))
			self.start_pos = (click.x,click.y)


	def moving(self,pos):
		#при движении зажатой мыши изменяются соответсвующие координаты у точек линии
		with self.canvas:
			oval = self.start_pos
			if not self.filling:
				self.figure.ellipse = (oval[0],oval[1],pos.x-oval[0],pos.y-oval[1])

			else:
				self.figure.size = (pos.x-oval[0],pos.y-oval[1])

	def move_directly(self,x,y):
		with self.canvas:
			if self.filling:
				self.figure.pos = [self.figure.pos[0]+x,self.figure.pos[1]+y]

			else:
				pos = self.figure.ellipse
				self.figure.ellipse = [pos[0]+x,pos[1]+y,pos[2],pos[3]]
