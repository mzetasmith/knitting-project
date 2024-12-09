from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

import opencvclean

class KnitApp(App):
    position = ""
    filepath = ""
    stitch_per_row = -1
    num_of_rows = -1
    instructions = ""

    def load(self, chooser, filename, touch):
        try:
            self.filepath = filename[0]
            self.image.source = filename[0]
            self.popup.dismiss()
        except:
            pass
    
    def convert(self, button):
        layout = GridLayout(cols = 1)
        if (self.filepath):
            self.instructions = opencvclean.convert(self.filepath, self.stitch_per_row, self.num_of_rows, self.position)
        else:
            self.instructions = "Error"
        pattern_instruct = Label(text = self.instructions)
        closeButton = Button(text="Close", size_hint=(None, None), size=(100, 75), on_release = self.close)
        layout.add_widget(pattern_instruct)
        layout.add_widget(closeButton)
        self.popup = Popup(title='Knitting Pattern', content=layout, auto_dismiss=False, size_hint=(None, None), size=(400, 400))
        self.popup.open()

    def upload(self, button):
        layout = BoxLayout(orientation="vertical")
        fc = FileChooserIconView(filters=["*.png"])
        fc.bind(on_submit = self.load)
        closeButton = Button(text="Close", size_hint=(None, None), size=(100, 75), on_release=self.close)
        layout.add_widget(fc)
        layout.add_widget(closeButton)
        self.popup = Popup(title='Choose Knitting Chart', content=layout, auto_dismiss=False, size_hint=(None, None), size=(400, 400))
        self.popup.open()
    
    def close(self, event):
        self.popup.dismiss()

    def on_left(self, instance, value):
        if value:
            KnitApp.position = "left"

    def on_center(self, instance, value):
        if value:
            KnitApp.position = "center"

    def on_right(self, instance, value):
        if value:
            KnitApp.position = "right"

    def build(self):
        BL = BoxLayout(orientation = 'vertical')
        
        horizontal = BoxLayout(orientation = 'horizontal')
        vertical = BoxLayout(orientation = 'horizontal')
        position = BoxLayout(orientation = 'horizontal')

        head = Label(text = 'Knitting App', font_size = 20, size_hint = (1, 0.1))
        instruct = Label(text = 'Please upload a chart image', font_size = 20, size_hint = (1, 0.1))
        
        btn1 = Button(text ="Click here to choose a file", font_size = 20, size_hint =(1, .1), on_press = self.upload)
        
        horizontal.add_widget(Label(text = 'Amount of stitches per row: ', size_hint= (1,0.2)))
        self.horizontal_stitch = TextInput(multiline = False, input_filter='int', size_hint= (1,0.2))
        horizontal.add_widget(self.horizontal_stitch)
        horizontal.add_widget(Label(text = 'stitches/row',  size_hint= (1,0.2)))

        vertical.add_widget(Label(text = 'Amount of rows: ', size_hint= (1,0.2)))
        self.vertical_stitch = TextInput(multiline = False, input_filter='int', size_hint= (1,0.2))
        vertical.add_widget(self.vertical_stitch)
        vertical.add_widget(Label(text = 'rows', size_hint= (1,0.2)))

        position.add_widget(Label(text = 'Position: '))
        position.add_widget(Label(text = 'Left'))
        self.left = CheckBox(group = 'position')
        self.left.bind(active = self.on_left)
        position.add_widget(self.left)

        position.add_widget(Label(text = 'Center'))
        self.center = CheckBox(active= False, group = 'position')
        self.center.bind(active = self.on_center)
        position.add_widget(self.center)


        position.add_widget(Label(text = 'Right'))
        self.right = CheckBox(active= False, group = 'position')
        self.right.bind(active = self.on_right)
        position.add_widget(self.right)

        convert = Button(text ="Convert!",font_size = 20, size_hint =(1, .2), on_release = self.convert)

        self.image = Image(source ="")

        BL.add_widget(head)
        BL.add_widget(instruct)
        BL.add_widget(btn1)
        BL.add_widget(self.image)
        BL.add_widget(horizontal)
        BL.add_widget(vertical)
        BL.add_widget(position)
        BL.add_widget(convert)
        return BL

if __name__ == '__main__':
    KnitApp().run()
