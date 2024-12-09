from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

import opencvclean

class KnitApp(App):
    x_position = "center"
    y_position = "center"
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
            self.instructions = opencvclean.convert(self.filepath, self.stitch_per_row, self.num_of_rows, self.x_position, self.y_position)
        else:
            self.instructions = "Error"
        pattern_instruct = Label(text = self.instructions)
        closeButton = Button(text="Close", size_hint=(None, None), size=(100, 75), on_release = self.close)
        layout.add_widget(pattern_instruct)
        layout.add_widget(closeButton)
        self.popup = Popup(title='Knitting Pattern', content=layout, auto_dismiss=False, size_hint=(0.8, 0.8))
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

    def get_rows(self, instance, value):
        if(value):
            self.stitch_per_row = value
        else:
            self.stitch_per_row = -1

    def get_cols(self, instance, value):
        if(value):
            self.num_of_rows = value
        else:
            self.num_of_rows = -1

    def on_left(self, instance, value):
        if value:
            KnitApp.x_position = "left"
        else:
            KnitApp.x_position ="center"

    def x_on_center(self, instance, value):
        if value:
            KnitApp.x_position = "center"

    def on_right(self, instance, value):
        if value:
            KnitApp.x_position = "right"
        else:
            KnitApp.x_position ="center"

    def on_down(self, instance, value):
        if value:
            KnitApp.y_position = "down"
        else:
            KnitApp.x_position ="center"

    def y_on_center(self, instance, value):
        if value:
            KnitApp.y_position = "center"

    def on_up(self, instance, value):
        if value:
            KnitApp.y_position = "up"
        else:
            KnitApp.x_position ="center"

    def build(self):
        BL = BoxLayout(orientation = 'vertical')
        
        horizontal = BoxLayout(orientation = 'horizontal')
        vertical = BoxLayout(orientation = 'horizontal')
        xposition = BoxLayout(orientation = 'horizontal')
        yposition = BoxLayout(orientation = 'horizontal')

        head = Label(text = 'Knitting App', font_size = 20, size_hint = (1, 0.1))
        instruct = Label(text = 'Please upload a chart image', font_size = 20, size_hint = (1, 0.1))
        
        btn1 = Button(text ="Click here to choose a file", font_size = 20, size_hint =(1, .1), on_press = self.upload)
        
        horizontal.add_widget(Label(text = 'Amount of stitches per row: ', size_hint= (1,0.2)))
        self.horizontal_stitch = TextInput(multiline = False, 
                                          input_filter='int', 
                                          size_hint= (1,0.2),)
        self.horizontal_stitch.bind(text = self.get_rows)
        horizontal.add_widget(self.horizontal_stitch)
        horizontal.add_widget(Label(text = 'stitches/row',  size_hint= (1,0.2)))

        vertical.add_widget(Label(text = 'Amount of rows: ', size_hint= (1,0.2)))
        self.vertical_stitch = TextInput(multiline = False, input_filter='int', size_hint= (1,0.2))
        self.vertical_stitch.bind(text = self.get_cols)
        vertical.add_widget(self.vertical_stitch)
        vertical.add_widget(Label(text = 'rows', size_hint= (1,0.2)))

        xposition.add_widget(Label(text = 'Horzizontal position: '))
        xposition.add_widget(Label(text = 'Left'))
        self.left = CheckBox(group = 'x_position')
        self.left.bind(active = self.on_left)
        xposition.add_widget(self.left)

        xposition.add_widget(Label(text = 'Center'))
        self.xcenter = CheckBox(active= False, group = 'x_position')
        self.xcenter.bind(active = self.x_on_center)
        xposition.add_widget(self.xcenter)

        xposition.add_widget(Label(text = 'Right'))
        self.right = CheckBox(active= False, group = 'x_position')
        self.right.bind(active = self.on_right)
        xposition.add_widget(self.right)

        yposition.add_widget(Label(text = 'Vertical position: '))
        yposition.add_widget(Label(text = 'Top'))
        self.up = CheckBox(group = 'y_position')
        self.up.bind(active = self.on_up)
        yposition.add_widget(self.up)

        yposition.add_widget(Label(text = 'Center'))
        self.ycenter = CheckBox(active= False, group = 'y_position')
        self.ycenter.bind(active = self.y_on_center)
        yposition.add_widget(self.ycenter)

        yposition.add_widget(Label(text = 'Bottom'))
        self.down = CheckBox(active= False, group = 'y_position')
        self.down.bind(active = self.on_down)
        yposition.add_widget(self.down)

        convert = Button(text ="Convert!",font_size = 20, size_hint =(1, .2), on_release = self.convert)

        self.image = Image(source ="")

        BL.add_widget(head)
        BL.add_widget(instruct)
        BL.add_widget(btn1)
        BL.add_widget(self.image)
        BL.add_widget(horizontal)
        BL.add_widget(vertical)
        BL.add_widget(xposition)
        BL.add_widget(yposition)
        BL.add_widget(convert)
        return BL

if __name__ == '__main__':
    KnitApp().run()
