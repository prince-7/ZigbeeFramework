from tkinter import Tk

class Lamp():
    def __init__(self):
        self.lamp = Tk()
        self.lamp.title("Secure Lamp")
        self.lamp['bg'] = '#000000'
        self.lamp.mainloop()

    def command(self, data):
        if data == 'ffff':
            print('ON')
            self.lamp['bg'] = '#ffffff'
        elif data == 'aaaa':
            print('OFF')
            self.lamp['bg'] = '#000000'