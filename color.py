#!/usr/bin/env python 
#encoding: utf-8
#import ctypes
 
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
 
FOREGROUND_BLACK = 0x0
FOREGROUND_YELLOW = 0x0E # text color contains YELLOW.
FOREGROUND_GREEN= 0x0A # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_GRAY = 0x08 # text color contains gray.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
 
BACKGROUND_YELLOW = 0xE0 # background color contains YELLOW.
BACKGROUND_GREEN= 0xA0 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x00 # background color is intensified.
 
class Color:
    ''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs. - www.sharejs.com'''
    #std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    std_out_handle = 12
    def set_cmd_color(self, color, handle=std_out_handle):
        pass
        '''
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
        '''
     
    def reset_color(self):
        print '\033[0m',
     
    def set_print_red_text(self):
        print '\033[1;31m',
         
    def set_print_green_text(self):
        print '\033[1;32m',
     
    def set_print_yellow_text(self):
        print '\033[1;33m',

           
    def set_print_red_text_with_yellow_bg(self):
        print '\033[1;31;43m',


    def set_print_gray_text(self):
        print '\033[1;34m',
 
if __name__ == "__main__":
    clr = Color()
    clr.set_print_red_text()
    clr.set_print_green_text()
    clr.set_print_yellow_text()
    print 'yee'
    #clr.set_print_red_text_with_YELLOW_bg('background')
