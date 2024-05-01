
from Kivy_code import *
from size_images import *
adjustment(width, height)

from kivy.lang import Builder

from kivy.config import Config



Config.set('graphics', 'width',str(width) )
Config.set('graphics', 'height',str(height))
Config.set('graphics', 'resizable','0')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout

from painter import painter
from graphic_calculating import Ask_function_but, Ask_function_settings
from brush_settings import change_size, change_bright

from painter_objects import moving_painter_widget


from tkinter import Tk
from tkinter.filedialog import asksaveasfilename    #  в Tkinter можно создать окно сохранения файла
Tk().withdraw()    #убирает окно Tkinter



class Figure_Buttons(GridLayout):
	def __init__(self,painter,App_window,**kwargs):

		self.painter = painter
		self.App_window = App_window
		super(Figure_Buttons,self).__init__(**kwargs)

	def pressed(self,mode):
		self.painter.mode = mode



class Figure_buttons_settings(GridLayout):
	def __init__(self,painter,**kwargs):
		self.painter = painter
		super(Figure_buttons_settings,self).__init__(**kwargs)


	def pressed(self,option):
		self.painter.filling = not(self.painter.filling)

		self.background_normal = 'images/check_mark.png'


class Personal_color_but(Button):
	def __init__(self,AppWindow,painter,curent_color,**kwargs):
		self.AppWindow = AppWindow
		self.painter = painter
		self.curent_color = curent_color
		self.ask_color = Ask_Color(self.AppWindow,self,self.curent_color,self.painter)
		self.active = False

		super(Personal_color_but,self).__init__(**kwargs)



	def pressed(self):
		if not(self.active):
			self.painter.drawing_accept = False
			self.active = True
			self.AppWindow.add_widget(self.ask_color)

	def remove_window(self):
		self.painter.drawing_accept = True
		self.active = False
		self.ask_color.parent.remove_widget(self.ask_color)




class Ask_Color(Widget):
	def __init__(self,AppWindow,button,curent_color,painter,**kwargs):

		super((Ask_Color),self).__init__(**kwargs)
		self.AppWindow = AppWindow
		self.button = button
		self.curent_color = curent_color
		self.painter = painter
		self.red_value = 0
		self.green_value = 0
		self.blue_value = 0

	def back(self,):
		self.button.remove_window()

	def red(self,value,color_view):
		self.red_value = (value/100)
		color_view.background_color[0] = self.red_value

	def green(self,value,color_view):
		self.green_value = (value/100)
		color_view.background_color[1] = self.green_value

	def blue(self,value,color_view):
		self.blue_value = (value/100)
		color_view.background_color[2] = self.blue_value


	def accept(self):
		self.curent_color.background_color = (self.red_value,self.green_value,self.blue_value)
		self.painter.change_color(self.curent_color)
		self.painter.color_save(self.curent_color)

		self.button.remove_window()


class clear_window(Button):

	def __init__(self, painter,  settings, button,func_but, **kwargs):
		self.painter = painter
		self.settings = settings
		self.button = button
		self.func_but = func_but
		super(clear_window, self).__init__(**kwargs)

	def yes(self):
		# при нажатии на кнопку ДА сначало стирается окно, а потом очищается холст
		self.no()

		self.func_but.remove_window()

		self.settings.change_all_settings(('down', 'normal'))
		self.painter.clear_canvas(None)

	def no(self):
		self.button.active = False
		self.button.remove()


class save_pic_but(Button):

	def __init__(self, painter, **kwargs):
		super(save_pic_but, self).__init__(**kwargs)
		self.painter = painter
		self.count = 0

	# эффект нажатой кнопки путем уменьшения размера кнопки
	def pressed(self, button):
		button.size = (width / 20 - 5, width / 20 - 5)
		button.center_x = width / 40
		button.center_y = width / 40

	# возвращение в исходное состоянии кнопки и открытиеокна сохранения файла
	def on_touch_up(self, click):

		if self.collide_point(*click.pos):
			if self.count % 2 == 0:
				filename = asksaveasfilename(defaultextension='png')
				self.painter.export_to_png(filename)

			self.count += 1

		self.size = ((width / 20, width / 20))
		self.center_x = width / 40
		self.center_y = width / 40


class returns_buttons(Widget):
	def __init__(self, painter, **kwargs):
		self.painter = painter
		super(returns_buttons, self).__init__(**kwargs)


	def pressed_left(self, button):
		button.size = (width / 21, height / 21)
		button.center_x = width / 1.1
		button.center_y = height - height / 25

	def pressed_right(self, button):
		button.size = (width / 21, height / 21)
		button.center_x = width / 1.1 + width / 20 + (width / 340)
		button.center_y = height - height / 25

	def touch_up(self, button,direct):
		button.size = (width / 21, height / 21)
		button.center_y = (height - height / 50) - height / 47

		if direct == 'left':
			button.center_x = width/1.0955

		else:
			button.center_x = width/1.0955+width/21+(width/340)

	def release_left(self):
		self.painter.back()

	def release_right(self):
		self.painter.forward()


class App(App):

	def build(self):
		AppWindow = Widget()    #главное окно приложения
		self.painter = painter(AppWindow)    #создание холста

		AppWindow.add_widget(self.painter)    # добавление слоя с холстом на главное окно
		color_buttons = self.making_buttons()    #создание кнопок смены цвета


		AppWindow.add_widget(color_buttons)

		self.curent_color = Button(size=(width/13,width/13),   #создание виджета для показа текущего выбранного цвета
			background_color = (0,0,0),    #черный цвет по умолчанию
			pos = (width/1.1,0),
			disabled = True,     #кнопка всегда нажата
			background_disabled_normal= '')   #убираем дефолтный фон нажатой кнопки


		personal_color_but = Personal_color_but(AppWindow,self.painter,self.curent_color)
		ask_function_settings = Ask_function_settings(self.painter)
		ask_function_but = Ask_function_but(AppWindow,self.painter,ask_function_settings)


		self.change_bright = change_bright(self.painter,self.curent_color)   #создание ползунка для смены прозрачности
		self.change_bright.bind(state=self.change_bright.touch)     #биндим эту кнопку т.к. надо отслеживать ее нажатие и отжатие

		Change_size = change_size(self.painter,self.curent_color,self.change_bright)
		Change_size.bind(state=Change_size.touch)


		save_but = save_pic_but(self.painter)
		Returns_Buttons = returns_buttons(self.painter)

		clear_button = Clear_button(self.painter,AppWindow,ask_function_settings, ask_function_but)    #кнопка очищения холста

		figures_buttons = Figure_Buttons(self.painter,AppWindow)    #кнопки фигур
		figure_buttons_settings = Figure_buttons_settings(self.painter)


		#сохраняем текущий черный цвет
		self.painter.color_save(self.curent_color)
		self.painter.color_load()

		#добавление виджетов на главное окно
		AppWindow.add_widget(self.curent_color)
		AppWindow.add_widget(personal_color_but)
		AppWindow.add_widget(ask_function_but)
		AppWindow.add_widget(ask_function_settings)


		AppWindow.add_widget(clear_button)
		AppWindow.add_widget(save_but)
		AppWindow.add_widget(Returns_Buttons)


		AppWindow.add_widget(figures_buttons)
		AppWindow.add_widget(figure_buttons_settings)

		AppWindow.add_widget(moving_painter_widget(self.painter))


		AppWindow.add_widget(Change_size)
		AppWindow.add_widget(self.change_bright)

		return AppWindow


	def making_buttons(self):

		#создание слоя с кнопками
		buttons = GridLayout(size = (width / 11,height/1.5),pos = [width/1.122,height/3.8],cols = 2,rows = 9,spacing = 8)

		#все цвета для политры
		colors = [(1,0,0),(0.58, 0.28, 0.28),
		    (1,0.5,0.5),(0.87, 0.01, 1),
		    (0.14, 0.01, 1),(0.01, 0.77, 1),
		    (0.01, 1, 0.77),(0.01, 1, 0.0),
		    (0.1, 0.34, 0.01),(1,1,0),
		    (1, 0.53, 0),(1,1,1),
		    (0.36, 0.36, 0.36),(0,0,0),
		    (0.45, 0.24, 0.01)]

		for color in colors:
			buttons.add_widget(Button(background_color = color,
		     	on_press= self.color_pressed,
		     	background_normal = '',
		     	background_down= ''))

		return buttons

	#при нажатие на кнопку из палитры
	def color_pressed(self,button):

		self.painter.change_color(button,self.change_bright.bright)    #меняем цвет текущей кисти
		self.curent_color.background_color = (button.background_color)    #меняем цвет виджета текущего цвета
		self.painter.color_save(self.curent_color,self.change_bright.bright)


class Clear_button(Button):
	def __init__(self,painter,window,ask_function_settings,func_but ,**kwargs):
		super(Clear_button, self).__init__(**kwargs)
		self.active = False
		self.window = window
		self.Clear_window = clear_window(painter, ask_function_settings, self, func_but)

	def on_press(self):
		self.size = (width / 20 - 5, width / 20 - 5)
		self.center_x = width / 40
		self.pos_y = height/9

	def on_touch_up(self, touch):
		self.size = (width // 20, width // 20)
		if self.collide_point(*touch.pos) and not(self.active):
			self.active = True
			self.window.add_widget(self.Clear_window)


	def remove(self):
		self.window.remove_widget(self.Clear_window)



if __name__ == '__main__': 
	Builder.load_string(kivy_code)
	App = App().run()
