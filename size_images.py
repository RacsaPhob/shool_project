from PIL import Image
def adjustment(width,height):
    size = (width//18 - 10,height//8 - 15)

    img = Image.open('images\ellipseOrig.png')
    img = img.resize(size)
    img.save('images\ellipse.png')

    img = Image.open('images/squareOrig.png')
    img = img.resize(size)
    img.save('images\square.png')

    img = Image.open('images/triangleOrig.png')
    img = img.resize(size)
    img.save('images/triangle.png')

    img = Image.open('images/pen_iconOrig.png')
    img = img.resize(size)
    img.save('images/pen_icon.png')

    img = Image.open('images/rulerOrig.png')
    img = img.resize(size)
    img.save('images/ruler.png')

    img = Image.open('images/arrowOrig.png')
    img = img.resize(size)
    img.save('images/arrow.png')

    size = (width//20,height//20)

    img = Image.open('images/return_buttonOrig.png')
    img = img.resize(size)
    img.save('images/return_button.png')

    img = Image.open('images/return_button_leftOrig.png')
    img = img.resize(size)
    img.save('images/return_button_left.png')

    size = [width//40,height//30]

    img = Image.open('images/confirmOrig.png')
    img = img.resize(size)
    img.save('images/confirm.png')

    img = Image.open('images/confirm_pressedOrig.png')
    img = img.resize(size)
    img.save('images/confirm_pressed.png')

    size = (width//60, width//60)

    img = Image.open('images/confirmOrig.png')
    img = img.resize(size)
    img.save('images/confirm1.png')

    img = Image.open('images/confirm_pressedOrig.png')
    img = img.resize(size)
    img.save('images/confirm_pressed1.png')


    size = (width//20,width//20)

    img = Image.open('images/save_butOrig.png')
    img = img.resize(size)
    img.save('images/save_but.png')

    size = (width // 20, width // 20)

    img = Image.open('images/trashOrig.png')
    img = img.resize(size)
    img.save('images/trash.png')

    size = (width // 22, width // 22)

    img = Image.open('images/add_colorOrig.png')
    img = img.resize(size)
    img.save('images/add_color.png')

    size = (width // 60, width // 60)

    img = Image.open('images/buttonOrig.png')
    img = img.resize(size)
    img.save('images/button.png')