#!/usr/bin/python
import pygame, os, subprocess, sys
from pygame.locals import *
import gettemperatures, call_433, time, datetime, processcalendar
from gettemperatures import read_temps
from call_433 import publish_redis
from call_433 import send_boiler 
# Every sample_limit loops we need to re-read our parameters
sample_limit=150
sample=0
turbo_temp=14
fps = 4 
target_temp=14
#######THIS VALUE NEEDS CONFIGURING##################
standard_comfortable_temperature=20
#####################################################
boosted=False
boiler_request_time=20 # Seconds
last_boiler_req=False
working_temp_addition=0
bobcounter=0
###########################################################
from evdev import InputDevice, list_devices
devices = map(InputDevice, list_devices())
eventX=""
for dev in devices:
    if dev.name == "ADS7846 Touchscreen":
        eventX = dev.fn
#print eventX

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ["SDL_MOUSEDEV"] = eventX
pygame.init()
###########################################################
screen = pygame.display.set_mode((0, 0), 0, 32)
mainloop =  True
#screen = pygame.display.set_mode((320, 240))
screen_general_x=int(3*screen.get_width()/14)
clock = pygame.time.Clock() 
button_up_unlit = pygame.image.load('/home/pi/PiThermostat/icons/OSDChannelUpNF.png')
button_up_lit = pygame.image.load('/home/pi/PiThermostat/icons/OSDChannelUpFO.png')
button_down_unlit = pygame.image.load('/home/pi/PiThermostat/icons/OSDChannelDownNF.png')
button_down_lit = pygame.image.load('/home/pi/PiThermostat/icons/OSDChannelDownFO.png')
#bob = pygame.image.load('/home/pi/PiThermostat/icons/JR-BOB-DOBBS.png')
bob1 = pygame.image.load('/home/pi/PiThermostat/icons/bob_pipe1.png')
bob2 = pygame.image.load('/home/pi/PiThermostat/icons/bob_pipe2.png')
bob3 = pygame.image.load('/home/pi/PiThermostat/icons/bob_pipe3.png')
bob4 = pygame.image.load('/home/pi/PiThermostat/icons/bob_pipe4.png')
boost_lit = pygame.image.load('/home/pi/PiThermostat/icons/enjiia_button_lit.png')
boost_unlit = pygame.image.load('/home/pi/PiThermostat/icons/enjiia_button_unlit.png')
bob_images=[bob1,bob2,bob3,bob4]
myFont = pygame.font.SysFont("arial", 30)
button_up_x, button_up_y = screen_general_x,250
button_down_x, button_down_y = 140,250
screen.fill([0,255,0])
screen.blit(button_up_unlit, (button_up_x, button_up_y))
screen.blit(button_down_unlit, (button_down_x, button_down_y))
#screen.blit(boost_unlit, boost_unlit.get_rect(right=(14*screen_general_x), top=(screen_general_y/5)))
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
NAVY_BLUE = ( 0, 0, 192 )
PURPLE = ( 192, 0, 192 )
CYAN  = (  0, 255, 255)
MAGENTA=(255,   0, 255)
YELLOW =(204, 204,   240)

def screenupdate(time,temp,weather,ideal,tempcolour,boilerstate,bobcounter,boosted,turbo_temp):

#    print ("Boosted = %r" % boosted)
    tempfont = pygame.font.Font(None, 100)
    screen_general_x=int(1*screen.get_width()/14)
    screen_general_y=int(1*screen.get_height()/14)
    timepos = timenow.get_rect(left=1*screen_general_x,top=(screen_general_y/4))
    tempnow = tempfont.render("%.1f%sC" % (temp, chr(176)) , 1, (tempcolour))
    temppos = tempnow.get_rect(left=screen_general_x,top=2*(screen_general_y))
    weatherpos = weathernow.get_rect(left=2*screen_general_x,top=6*(screen_general_y))
    idealpos = idealnow.get_rect(right=13*screen_general_x,centery=8*(screen_general_y))
    bobpos = idealnow.get_rect(left=2*screen_general_x,centery=8*(screen_general_y))
    screen.fill([0,0,0])
    screen.blit(timenow, timepos)
    screen.blit(tempnow, temppos)
    screen.blit(weathernow, weatherpos)
    screen.blit(idealnow, idealpos)
    pygame.mouse.set_visible(False)
    screen.blit(button_up_unlit, (button_up_x, button_up_y))
    screen.blit(button_down_unlit, (button_down_x, button_down_y))
    if boosted:
#        print ("Enjiia logo boosted")
        screen.blit(boost_lit, boost_lit.get_rect(right=(14*screen_general_x), top=(screen_general_y/5)))
    else:
#        print ("Not boosted")
        screen.blit(boost_unlit, boost_unlit.get_rect(right=(14*screen_general_x), top=(screen_general_y/5)))
    if (boilerstate == True):
#        print bobcounter
        screen.blit(bob_images[bobcounter], bobpos)
    pygame.display.update()


while mainloop:
    from subprocess import call
    need_to_update=0
    pygame.mouse.set_visible(False)
    tick_time = clock.tick(fps)
    pygame.display.set_caption("Thermostat FPS: %.2f" % (clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mos_x, mos_y = pygame.mouse.get_pos()
#            print("Pos: %sx%s\n" % pygame.mouse.get_pos())
            if ((mos_x >= 160) and (mos_y >= 110)):
                  #Mouse if over icon Up
		  #sudo switch_on_off_backlight.sh on
		  subprocess.call(["/usr/local/bin/switch_on_off_backlight.sh","on"])
                  screen.blit(button_up_lit, (button_up_x, button_up_y))
                  need_to_update=1
                  working_temp_addition += 0.5
                  boiler_request_time=20 # Seconds
                  pygame.display.update()
            elif ((mos_x >= 160) and (mos_y < 110)):
                  #Mouse is over icon Down
		  #sudo switch_on_off_backlight.sh on
		  subprocess.call(["/usr/local/bin/switch_on_off_backlight.sh","on"])
                  screen.blit(button_down_lit, (button_down_x, button_down_y))
                  need_to_update=1
                  boiler_request_time=20 # Seconds
                  working_temp_addition -= 0.5
                  pygame.display.update()
            elif (( mos_x < 60 ) and (mos_y <60)):
                  #Mouse is over Boost
		  #sudo switch_on_off_backlight.sh on
		  subprocess.call(["/usr/local/bin/switch_on_off_backlight.sh","on"])
                  boosted = not boosted
                  need_to_update=1
#                  print "mouse over boost"
                  boiler_request_time=20 # Seconds
                  pygame.display.update()

####### If we are running for the first time

    if (sample == 0):
       (floattemp,target_temp,outside_temp,working_temp_addition,working_temp,boosted,turbo_temp) = read_temps() 
       boiler_request_time=20 # Seconds
       sample += 1
       need_to_update=1
####### If we are doing our regular update
    elif ( sample >= sample_limit):
#       print "attempting to run read_temps"
       old_target_temp=target_temp
#       (floattemp,target_temp,outside_temp) = read_temps() 
       (floattemp,target_temp,outside_temp,working_temp_addition,working_temp,boosted,turbo_temp) = read_temps() 
       need_to_update=1
       boiler_request_time=295 # Seconds
       if (old_target_temp != target_temp ):
           working_temp_addition=0 
           boosted=False
       sample = 1 
####### If we are doing our regular update just increment the sample
    elif ( sample <= sample_limit):
       sample += 1
###########################################
    if boosted:
        working_temp = turbo_temp
    else:
        working_temp = target_temp + working_temp_addition
    roundtemp =  (round(floattemp, 1))
    # Display some text
    font = pygame.font.Font(None, 64)
    now = datetime.datetime.now()
    formatted_time = now.strftime("%d-%h-%Y %H:%M")
    timefont = pygame.font.Font(None, 24)
    timenow = timefont.render("%s" % (formatted_time) , 1, (YELLOW))
    weatherfont = pygame.font.Font(None, 16)
    weathernow = weatherfont.render("External Temperature: %i%sC" % (outside_temp, chr(176)) , 1, (WHITE))
    idealfont = pygame.font.Font(None, 60)
    idealnow = idealfont.render("%.1f%sC" % (working_temp, chr(176)) , 1, (WHITE))
    temperature_ratio =  floattemp/working_temp
    if ( temperature_ratio >= 1 and temperature_ratio <= 1.025 ):
        fontcolour=GREEN
        boiler_req=True
    elif ( temperature_ratio <= 1 ):
        fontcolour=BLUE
        boiler_req=True
    elif ( temperature_ratio >= 1.025 ):
        fontcolour=RED
        boiler_req=False
    else:
        fontcolour=PURPLE
        boiler_req=False
#       Assume sample_limit is set to 150 @ 4 fps, will be called every 37.5s
    if (need_to_update == 1): 
        screenupdate(timenow,roundtemp, weathernow, idealnow,fontcolour,boiler_req,bobcounter,boosted,turbo_temp)
        bobcounter += 1
        if (bobcounter == 4):
            bobcounter = 0
        try:
           publish_redis(floattemp,target_temp, working_temp, working_temp_addition,boosted)
           send_boiler(boiler_req, boiler_request_time)
        except:
           print "Publishing error:", sys.exc_info()[0]
#       print "Unable to publish"
        need_to_update = 0
       
