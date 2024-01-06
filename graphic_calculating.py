import numpy as np
import sympy as sp
import math
import pyautogui
resolution = pyautogui.size()
width = resolution[0]-1
height = resolution[1]-1
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton


def Building_function(inputs,devisions,text,Window):
	rounding = 3

	function = ''
	count = 0
	if devisions:
		for Input in inputs:
			if len(devisions) > count:
				function +=  Input.text 	#добавляем в строку то что было до деления
				function += '((' +  devisions[count][0].text + ')/'	#добавляем в строку числитель
				function +=  '(' + devisions[count][1].text + '))'		#добавляем в строку знаменатель

			else:	#как только все деления будут записаны в строку
				function +=  inputs[-1].text 	 #добавится запись которая была после всех делений
				break

			count +=1


	else:
		function = text.text
	function = function.replace(' ','')
	function = function.replace(')(',')*(')
	function = function.replace('√' ,'sqrt')

	if "ctan" in function:
		function = function.replace('cot','1/tan')

	if not('sin') in function and not ('cos') in function and not ('tan') in function:
		rounding = 3

	x = sp.symbols('x')
	y = sp.symbols('y')
	coords = np.array([])	#массив с координатами точек графика вида (x1,y1,x2,y2,x3,y3,...)
	try:
		expression = (sp.sympify(function.replace('π','3.14159')))		#парсинг полученного выражения(получаем выражение удобного вида для пайтона и numpy)
	except:
		Window.show_error('ошибка:формула введена некоректно')
		return False



	try:
		fun = (sp.lambdify((x),expression,'numpy'))
	except:
		Window.show_error('ошибка: функция не имеет смысла')
		return False

	for x in range(-4000,4000):
		x = x/80
		try:
			result =round(fun(x),2)
		except:
			pass
		try:
			if result > 1000 or result < -1000:		#следим чтобы координаты точек не были слишком большими
				continue

			elif str(result) != 'nan':
				coords = np.append(coords,np.array([x,round(result,rounding)]))

		except:
			Window.show_error('ошибка:формула введена некоректно')
			return False

	dots = finding_dots(fun,devisions,coords,function)


	return coords, dots, function

def find_devision(function,coords):
	dots = []
	if not('/') in function:
		return False
	else:
		count = 0
		devision_chs = []
		for ch in function:
			if ch=='/':
				devision_chs.append(count)
			count +=1
		expressions = []
		for devisions in devision_chs:
			count = 0
			count1 = 0
			new_function = function[devisions:]
			if '(' in new_function:

				for ch in new_function:
					count1 +=1
					if ch =='(':
						count +=1
					elif ch ==')':
						count -=1
						if count ==0:
							expressions.append((new_function[1:count1]))
							break
		else:
			count = 0
			symbols = ['+','-','/','*']
			for ch in new_function[1:]:
				if ch in symbols:

					expressions.append((new_function[1:count+1]))
				count +=1


		x = sp.symbols('x')
		for expression in expressions:
			try:
				equation = sp.Eq(eval(expression), 0)
				for dot in sp.solve(equation, x):
					dots.append((dot, find_near_coord_dot(dot, coords)))
			except:
				pass
		return dots

def finding_dots(function,devisions,coords,fun_str):
	dots = []	#список в котором находятся выколотые точки
	another_checking_needed = False
	if not ('cos') in fun_str and not ('tan') in fun_str and not ('sin') in fun_str and not ('cot') in fun_str:
		if not ('√') in fun_str:
			dots == find_devision(fun_str,coords)
			if not(dots):
				dots = []
	for devision in devisions:
		znamen = devision[1].text

		if not('cos') in znamen and not('tan') in znamen and not('sin') in znamen and not('cot') in znamen:
			if not('√') in znamen:
				znamen = znamen.replace('^','**')
				x= sp.symbols('x')
				equation = sp.Eq(eval(znamen),0)

				for dot in sp.solve(equation,x):
					dots.append((dot,find_near_coord_dot(dot,coords)))

			else:
				another_checking_needed = True
		else:
			another_checking_needed = True


	if another_checking_needed:

		for x in np.arange(-50000,50000):

				result = function(x/100)
				if str(result) == 'inf':
					dots.append((x/100,find_near_coord_dot(x/100,coords)))


	return dots	


def find_near_coord_dot(dot,coords):
	if -50 <dot<50:
		for i in range(0,len(coords),2):
			if not(coords[i] <= dot >-40):

				if -50 < coords[i+1] < 50 and abs(coords[i+1] - coords[i-1])< 10:
					return (coords[i+1],coords[i-1])
				else:
					break

class ask_function_buttons(Widget):
	def __init__(self,painter,window,**kwargs):
		super(ask_function_buttons,self).__init__(**kwargs)
		self.painter = painter
		self.window = window

	def typing(self,text):

		self.window.typing(text)



class Window_ask_function(Widget):
	def __init__(self,painter,button,settings,**kwargs):
		super(Window_ask_function,self).__init__(**kwargs)

		self.button = button
		self.devisions = []
		self.input_s = []
		self.painter = painter
		self.settings = settings
		self.delits = []
		self.active = None
		self.orig_text = None
		self.error_l = None

		self.add_widget(ask_function_buttons(painter,self))


	def devision(self,text):

		if not(self.orig_text):
			self.orig_text = text
		if len(self.devisions)<5 :

			if len(self.input_s) !=0:
				text = self.input_s[-1]
			text.size[0] = len(text.text)*25 - (len(text.text)-1)*8

			posx = text.size[0]+ text.pos[0]

			self.input_s.append(text)



			self.delit = TextInput(x = posx,center_y= height/2 +220,size = (35,30),font_size=13, on_text = self.make_active)
			self.delit.bind(text=self.increase_size)
			self.delit.bind(focus=self.make_active)


			self.znamen = TextInput(x =posx,center_y= height/2 +190,size = (35,30),font_size=13, on_text = self.make_active)
			self.znamen.bind(text=self.increase_size)
			self.znamen.bind(focus=self.make_active)


			self.devisions.append((self.delit,self.znamen))


			size_new_input = (350 - (posx-width/3-135),60)

			self.new_input = TextInput(x = posx+self.delit.size[0],
										center_y = height/2+190,size=size_new_input,
										multiline = False,font_size = 30,
									   on_text = self.make_active)
			self.new_input.bind(focus=self.make_active)


			self.input_s.append(self.new_input)

			self.add_widget(self.new_input)
			self.add_widget(self.delit)
			self.add_widget(self.znamen)


	def accept(self,text,size_cell):
		if not(self.orig_text):
			self.orig_text = text
		function = Building_function(self.input_s,self.devisions,text,self)

		if function:
			self.painter.cell = 20 + (5*int(size_cell))
			self.painter.add_string_in_line(function[2])
			self.painter.draw_function(function[0],function[1])
			self.settings.change_all_settings(('normal','down'))
			self.painter.draw_dots()
			self.back(text)

			self.painter.color_load()

	def increase_size(self,Object,value):
		new_size = len(value) * 11
		sub_size = 0
		for delit in self.devisions:
			sub_size += delit[0].size[0]

		for Input in self.input_s[:-1]:
			sub_size += Input.size[0]
		if Object == self.delit or Object == self.znamen:
			if new_size > self.delit.size[0]-5:
				self.delit.size[0] = new_size
				self.znamen.size[0] = new_size
				self.new_input.size[0] =  350 - sub_size
				if 350 - sub_size <0:
					self.new_input.size[0] = 0
				self.new_input.pos[0] = self.devisions[-1][0].pos[0] + new_size

	def back(self,text):
		self.button.remove_window()
		if self.error_l:
			self.error_l.text = ''
		self.clear(text)

	def clear(self,text):

		if not(self.orig_text):
			self.orig_text = text

		for object in self.devisions:
			self.remove_widget(object[0])
			self.remove_widget(object[1])

		for object in self.input_s[1:]:
			if not (object == self.orig_text):
				self.remove_widget(object)
				self.input_s.remove(object)
		if self.orig_text:
			self.orig_text.size[0] = 350
			self.orig_text.text = ''



		self.input_s.append(self.orig_text)
		self.devisions.clear()



	def show_error(self,text):
		if not(self.error_l) or not(self.error_l.text):
			self.error_l = Label(text=text,color=(1,0,0),font_size=20,center_x=width/2-50,center_y=height/2+220)
			self.add_widget(self.error_l)
		self.clear(self.orig_text)

	def change_size_cell(self,input,action):
		if action =='+' and int(input.text)<5:
			input.text = str(int(input.text)+1)

		if action =='-' and int(input.text)>1:
			input.text = str(int(input.text)-1)


	def change_De_Ra(self,button):
		mode = button.text
		if mode == 'de':
			button.text = 'ra'
			self.painter.dera = 'ra'
		elif mode == 'ra':
			button.text = 'de'
			self.painter.dera = 'de'

	def typing(self,text):
		if not self.active:
			for object in self.children:
				if isinstance(object,TextInput):
					self.active = object
		old_text = self.active.text
		if text != 'π':
			self.active.text = old_text + text + '()'
		else:
			self.active.text = old_text + text


	def make_active(self,input,value):
		if value:

			self.active = input




class Ask_function_but(Button):
	def __init__(self,AppWindow,painter,settings,**kwargs):
		super((Ask_function_but),self).__init__(**kwargs)

		self.AppWindow = AppWindow
		self.painter = painter
		self.window = Window_ask_function(painter,self,settings)
		self.active = False


	def released(self):
		if not(self.active):
			self.active = True
			self.painter.drawing_accept = False
			self.AppWindow.add_widget(self.window)

	def remove_window(self):
		self.active = False
		self.painter.drawing_accept = True
		self.window.parent.remove_widget(self.window)



class Ask_function_settings(GridLayout):
	def __init__(self,painter,**kwargs):
		self.painter = painter
		super((Ask_function_settings),self).__init__(**kwargs)


	def pressed_1(self,state):
		if 	state == 'down':
			self.painter.draw_backgrounds()
		else:
			self.painter.remove_background()


	def pressed_2(self,state):
		if 	state == 'down':
			self.painter.draw_axis()
		else:
			self.painter.remove_axis()


	def pressed_3(self,state):
		if 	state == 'down':
			self.painter.draw_segments()
		else:
			self.painter.remove_segments()

	def pressed_4(self,state):
		if 	state == 'down':
			self.painter.draw_dots()
		else:
			self.painter.remove_dots()

	def pressed_5(self,state):
		if 	state == 'down':
			self.painter.draw_generals()
		else:
			self.painter.remove_generals()


	def pressed_6(self,state):
		if 	state == 'down':
			self.painter.draw_list()
		else:
			self.painter.remove_list()


	def change_all_settings(self,states):
		functions = [self.pressed_1,self.pressed_4,self.pressed_2,self.pressed_5,self.pressed_3,self.pressed_6]
		count = 0
		children = self.children.copy()
		children.reverse()
		for child in children:		#виджеты хронятся в children в виде: кнопка, описание, кнопка, описание
			if isinstance(child,ToggleButton):	# так что необходимо изменять состояние каждого второго элемента из children

				if child.state == states[0] :
					if not(count == 6 and states[1] == 'down'):		#меняем все функции кроме общих точек
						functions[int(count/2)](states[1])

						child.state = states[1]

			count +=1	



