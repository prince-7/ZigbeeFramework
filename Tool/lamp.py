from tkinter import Tk

class Lamp():
    def __init__(self):
        self.lamp = Tk()
        self.lamp.title("Secure Lamp")
        self.lamp['bg'] = '#000000'

    def command(self, data):
        if data == 'ffff':
            self.lamp['bg'] = '#ffffff'
            print('ON')
        elif data == 'aaaa':
            self.lamp['bg'] = '#000000'
            print('OFF')
        else:
            print('No Signal')
        self.lamp.update()