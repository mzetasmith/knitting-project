from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
import opencvclean

class BoxLayoutApp(App):

    def build(self):
        BL = BoxLayout(orientation = 'vertical')
        head = Label(text = 'Knitting App',
                        font_size = 20,
                        size_hint = (1, 0.1))
        instruct = Label(text = 'Please upload a chart image',
                        font_size = 20,
                        size_hint = (1, 0.1))
        btn1 = Button(text ="B1",
                      font_size = 20,
                      size_hint =(1, .1))
        btn2 = Button(text ="B2",
                      font_size = 20,
                      size_hint =(.2, .1))
        btn3 = Button(text ="B3",
                      font_size = 20,
                      size_hint =(.2, .1))
        btn4 = Button(text ="B4",
                      font_size = 20,
                      size_hint =(.2, .1))
        btn5 = Button(text ="B5",
                      font_size = 20,
                      size_hint =(.2, .1))

        BL.add_widget(head)
        BL.add_widget(instruct)
        BL.add_widget(btn1)
        BL.add_widget(btn2)
        BL.add_widget(btn3)
        BL.add_widget(btn4)
        BL.add_widget(btn5)

        return BL
if __name__ == '__main__':
    BoxLayoutApp().run()
