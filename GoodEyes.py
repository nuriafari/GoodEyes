# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 12:14:08 2022

@author: nuria



#todo
- change so that it does not pop up two times if I am already away (maybe sleep for 1sec? lets try)
"""
from __future__ import print_function
from threading import Thread
import pygame
import datetime
import time

import os
import json
import cv2 as cv
import argparse
import ctypes  # An included library with Python install.


pygame_title = "GoodEyes"
pygame_icon_png = "eye.png" 


stream = cv.VideoCapture(0, cv.CAP_DSHOW)
pygame.init()


screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


font_title = pygame.font.SysFont("Segoe UI", 40, bold = True)

font_30 = pygame.font.SysFont("calibri", 30)
font_24 = pygame.font.SysFont("calibri", 24)
font_18 = pygame.font.SysFont("calibri", 18) 
font_16 = pygame.font.SysFont("calibri", 16)
font_14 = pygame.font.SysFont("calibri", 16)



filepath = os.path.dirname(__file__)

pygame.display.set_caption(pygame_title)
programIcon = pygame.image.load(os.path.join(filepath,pygame_icon_png))
pygame.display.set_icon(programIcon)


class button():
    def __init__(self, color, x,y,width,height, text='', font=font_30):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self,screen):
        #Call this method to draw the button on the screen            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0,5)
        
        if self.text != '':
            text = self.font.render(self.text, 1, (255,255,255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def change_button_color(button_key, pos, default_color=(0,0,0), isOver_color=(0,0,255)):
    if button_key.isOver(pos):
        button_key.color = isOver_color
    else:
        button_key.color = default_color
    button_key.draw(screen)
    pygame.display.update()


def detectWidth(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    faces = face_cascade.detectMultiScale(frame_gray,1.3,5)
    width = 0
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y + h, x:x + w]
        # -- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)

        for (x2, y2, w2, h2) in eyes:

            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

        width = w
    cv.imshow('Capture - Face detection', frame)
    return width

def Mbox(title, text, style):
    
    
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def write_json(totalAlertTime, totalTime, num_popups):

    HOUR        = datetime.datetime.now().hour
    MINUTE      = datetime.datetime.now().minute
    
    with open(os.path.join(filepath,"dict.json"),"r") as json_file:
        json_dictionary = json.load(json_file)
        
    with open(os.path.join(filepath,"dict.json"),"w") as json_file:
        json_dictionary["h_{}_m_{}".format(HOUR,MINUTE)] = {}
        json_dictionary["h_{}_m_{}".format(HOUR,MINUTE)]["AlertTime"] = round(totalAlertTime/totalTime*100, 1)
        json_dictionary["h_{}_m_{}".format(HOUR,MINUTE)]["num_popups"] = round(num_popups/totalTime*60, 1)
        
        json.dump(json_dictionary, json_file)


def draw_graph (x,y,width,height,x_lst,y_lsts):
    
    colors = ((0,0,150),(0,150,0),(150,0,0))
    
    pygame.draw.line(screen, (0,0,0),(x,y+height),(x+width, y+height))
    pygame.draw.line(screen, (0,0,0), (x,y),(x,y+height))
    max_x = float(max(x_lst))
    for index, y_lst in enumerate(y_lsts):
        max_y = float(max(y_lst))
        prev_y_pos = 0
        prev_x_pos = 0
        color = colors[index]
        for index, val in enumerate(y_lst):
            i=index
            y_pos = int(y+height-val/max_y*height)
            x_pos = int(x+i/max_x*width)
            pygame.draw.circle(screen, color,(x_pos,y_pos), 1)
            if index >0:
                pygame.draw.line(screen, color, (prev_x_pos, prev_y_pos),(x_pos,y_pos), )
                     
            prev_y_pos = y_pos
            prev_x_pos = x_pos

def give_averages():
    with open(os.path.join(filepath,"dict.json"),"r") as json_file:
        json_dictionary = json.load(json_file)
     
    alerttime_list = []
    num_popups_list = []
    hours_list = []
    previous_hour = None  
    for index, sth in enumerate(json_dictionary):
        next_hour = sth.split("_")[1]
        if next_hour != previous_hour:
            alerttime_list.append([])
            num_popups_list.append([])
            hours_list.append(next_hour)
            
        alerttime_list[-1].append(json_dictionary[sth]["AlertTime"]) 
        num_popups_list[-1].append(json_dictionary[sth]["num_popups"])
        previous_hour = next_hour 
    
    width = 20
    height = 270

    
    write_message("week", rectangle=(width, height), font=font_16)
    write_message("% time being", rectangle=(width, height+25), font=font_16)
    write_message("too close", rectangle=(width, height+40), font=font_16)
    
    write_message("avg alerts/min", rectangle=(width, height+70), font=font_16)
    width +=150
    
    y_lst = [[],[]]
    for index, hours in enumerate(hours_list):
       
        
        alert = sum(alerttime_list[index])/len(alerttime_list[index]) 
        popups = sum(num_popups_list[index])/len(num_popups_list[index])
        
        y_lst[0].append(alert)
        y_lst[1].append(popups)
       
        write_message(str(hours), rectangle=(width, height), centered=True, font=font_16)
        write_message("{:.0f}".format(alert), rectangle=(width, height+37), centered=True, font=font_14)
        write_message("{:.1f}".format(popups), rectangle=(width, height+70), centered=True, font=font_14)
        width += 40
        
    write_message("alert time", rectangle=(55,430), font=font_16, color=(0,0,150))
    write_message("popups", rectangle=(55,450), font=font_16, color=(0,150,0))
    
    draw_graph(50,370,400,100,hours_list, y_lst)
        
def draw_Initial_Screen():
    ini=170
    sp=20
    
    screen.fill((255,255,255))
    write_message("G", rectangle=(ini, 20), font=font_title, color=(148,0,211))
    write_message("o", rectangle=(ini+sp, 20), font=font_title, color=(75,0,130))
    write_message("o", rectangle=(ini+sp*2, 20), font=font_title, color=(75, 0, 130))
    write_message("d", rectangle=(ini+sp*3, 20), font=font_title, color=(0, 0, 255))
    write_message("E", rectangle=(ini+sp*4, 20), font=font_title, color=(0, 255, 0))
    write_message("y", rectangle=(ini+sp*5, 20), font=font_title, color=(220, 220, 0))
    write_message("e", rectangle=(ini+sp*6, 20), font=font_title, color=(255, 127, 0))
    write_message("s", rectangle=(ini+sp*7, 20), font=font_title, color=(255, 0 , 0))
    
    
    #write_message("GoodEyes", rectangle=(screen_width/2, 20), centered=True, font=font_title)
    
    write_message("Welcome to GoodEyes!", rectangle=(screen_width/2, 95), centered=True, font=font_16)
    write_message("You will be warned if you are too close to the screen", rectangle=(screen_width/2, 120), centered=True, font=font_16)
    write_message("Press the button to start tracking!", rectangle=(screen_width/2, 140), centered=True, font=font_16)
    
    give_averages()
    
    button_off = button((255,0,0),220,180,50,50,text="OFF")
    button_off.draw(screen)

    pygame.display.update()
    
    
    
    return(button_off)
    
    draw_Initial_Screen()



        
    
def write_message(message, color = (0,0,0), rectangle=[0,0], font=font_18, update = True, centered = False):
    mesg = font.render(message, True, color)
    if centered:
        w,h = rectangle
        rectangle = [w-mesg.get_width()/2,h]
    screen.blit(mesg, rectangle)
    if update:
        pygame.display.update()    
        
def change_button_colors(button_off):
    
    Open = True
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_off.color == (100,0,0):
                button_off = button((0,255,0),220,180,50,50,text="ON")
                button_off.draw(screen) 
            if button_off.color == (0,100,0):
                button_off = button((255,0,0),220,180,50,50,text="OFF")
                button_off.draw(screen)
                Open = False
            
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if button_off.isOver(pos):
                if button_off.color == (255,0,0):
                        button_off = button((100,0,0),220,180,50,50,text="OFF")
                        button_off.draw(screen)

                elif button_off.color == (0,255,0):
                        button_off = button((0,100,0),220,180,50,50,text="ON")
                        button_off.draw(screen)

                
            else:
                if button_off.color == (100,0,0):
                    button_off = button((255,0,0),220,180,50,50,text="OFF")
                    button_off.draw(screen)
                elif button_off.color == (0,100,0):
                    button_off = button((0,255,0),220,180,50,50,text="ON")
                    button_off.draw(screen)


        if event.type == pygame.QUIT:
            Open = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                Open = False
            if event.key == pygame.K_q:
                Open = False

        
        pygame.display.update()
    return(Open, button_off)
                


                        
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default= cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default= cv.data.haarcascades + 'haarcascade_eye.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera


def updateGUI():
    clock.tick(60)
    

#pygame_intro() change to:
button_off = draw_Initial_Screen()
Open = True

while True:
    Open, button_off = change_button_colors(button_off)
    if button_off.color == (0,255,0) or Open==False:
        break

Thread(target=updateGUI, args=()).start()



start = time.time()
timeLast = start
alertTimeLimit = 5 #seconds. Change this variable with the interface code
alertTime = 0
totalAlertTime = 0
distance_list=[]
num_popups = 0
already_seen = False
while Open:

    Open, button_off = change_button_colors(button_off)
    
    timeNow = time.time()
    ret, frame = stream.read()
    width = detectWidth(frame)
    distance_list.append(width)

    if width > 220:
        print(timeNow - timeLast)
        alertTime = timeNow - timeLast
        #This line creates the popup after a period of time has past where face is too close to screen
        if(timeNow - timeLast > alertTimeLimit):
            if already_seen:
                already_seen = False
                continue
            else: 
                already_seen = True
            MB_YESNO = 4
            MB_TOPMOST = 0x40000
            uType = 0 | MB_TOPMOST
            Mbox('Get away!', 'You are too close to the screen', uType)
            num_popups +=1
            
    else:
        totalAlertTime += alertTime
        alertTime = 0
        screen.fill((255,255,255), (20,200,150,30))
        write_message("total alert time: {:.1f}s".format(totalAlertTime), rectangle=[20,200])
        pygame.display.update
        print("total aleart time", totalAlertTime)
        timeLast = timeNow
    
    
    pygame.display.flip()
    
    if (cv.waitKey(1) & 0xFF == ord('q')):
        break


end = time.time()
totalTime = end - start

if totalTime > 0:
    write_json(totalAlertTime, totalTime, num_popups)
stream.release()
cv.destroyAllWindows()
pygame.quit()
