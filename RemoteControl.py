# source: https://www.circuitbasics.com/how-to-detect-keyboard-and-mouse-inputs-on-a-raspberry-pi/

import pygame
import subprocess

import asyncio
import sys
import os
sys.path.append('/home/amizan8653/.venv/lib/python3.11/site-packages')
from pywizlight import wizlight, PilotBuilder, discovery


def write_out(txt):
    print(txt)



async def main(): 
        write_out("entering main loop")
        
        # lightbulb initiailzation
        wiz_bulb_ip = "192.168.4.21"

        """Sample code to work with bulbs."""
        wiz_light = wizlight(wiz_bulb_ip)

        
        pygame.init()
        window = pygame.display.set_mode((300, 300), pygame.HWSURFACE)
        pygame.display.set_caption("Pygame Demonstration")

        """
        key mappings: 

        backspace = f13
        = = f14
        kpslash = f15
        kpasterisk = F16

        kp7 = F17
        kp8 = F18
        kp9 = scroll lock
        kpminus = BrightnessDown

        kp4 = Cancel
        kp5 = menu
        kp6 = BrightnessUp
        kpplus = write_out screen

        kp1 = numlock
        kp2 = AudioStop
        kp3 = AudioPlay

        kpenter = Eject
        kp0 = help
        kpdot = AudioNext

        """

        mainloop=True
        while mainloop:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    mainloop = False

                if event.type == pygame.KEYDOWN:

                    write_out(pygame.key.name(event.key))
                    key_press = pygame.key.name(event.key).lower().replace(" ", "")
                    
                    

                    
                    # USB hub
                    if key_press == "f13":
                        # usb 1
                        write_out('backspace or virtual f13 pressed')
                        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO1", shell=True)
                    elif key_press == "f14":
                        # usb 2
                        write_out('= or virtual f14 pressed')
                        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO2", shell=True)
                    elif key_press == "f15":
                        # usb 3
                        write_out('/ or virtual f15 pressed')
                        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO3", shell=True)
                    elif key_press == "f16":
                        # usb 4
                        write_out('* or virtual f16 pressed')
                        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO4", shell=True)
                        
                        
                    # 4x2 HDMI Matrix
                    elif key_press == "f17":
                        # display 1 - gaming pc
                        # switch to display port on MSI monitor by pressing "ctrl shift alt f1 on keyboard". HDMI matrix - don't care.
                        write_out('7 or virtual f17 pressed')
                        
                    elif key_press == "f18":
                        # display 1 - mac
                        # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 4 out 1 with IR remote.
                        write_out('8 or virtual f18 pressed')
                        
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO5", shell=True)
                    elif key_press == "scrolllock":
                        # display 1 - gfe
                        # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 2 out 2 with IR remote.
                        write_out('9 or virtual scrolllock pressed')
                        
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO6", shell=True)
                    elif key_press == "cancel":
                        # display 1 - ps5
                        # switch to hdmi 2 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". HDMI matrix - don't care.
                        write_out('4 or virtual cancel pressed')

                    elif key_press == "menu":
                        # display 1 - switch
                        # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 3 out 2 with IR remote.
                        write_out('5 or virtual menu pressed')
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO7", shell=True)
                    elif key_press == "brightnessup":
                        # display 1 - raspberry pi
                        # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 4 out 2 with IR remote.
                        write_out('6 or virtual brightnessup pressed')
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO8", shell=True)
                        

                    # 8k_4x1_HDMI_SWITCH 
                    elif key_press == "numlock":
                        # display 2 - gaming pc
                        write_out('1 or virtual numlock pressed')
                        subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO3", shell=True)
                    elif key_press == "audiostop":
                        # display 2 - mac
                        write_out('2 or virtual audiostop pressed')
                        subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO4", shell=True)
                    elif key_press == "audioplay":
                        # display 2 - gfe
                        write_out('3 or virtual audioplay pressed')
                        subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO5", shell=True)
                        
                    # wiz light
                    # scenes are from: https://github.com/sbidy/pywizlight/blob/6c6e4a2c5c7c2b46e5f3159e6d290d9099f6b923/pywizlight/scenes.py#L7
                    elif key_press == "printscreen":
                        # warm light
                        write_out('+ or virtual write_outscreen pressed')
                        if wiz_light is not None:
                            await wiz_light.turn_on(PilotBuilder(scene = 11))
                    elif key_press == "eject":
                        # daylight
                        write_out('enter or virtual eject pressed')
                        if wiz_light is not None: 
                            await wiz_light.turn_on(PilotBuilder(scene = 12))
                    elif key_press == "help":
                        # off
                        write_out('0 or virtual help pressed')
                        if wiz_light is not None:
                            await wiz_light.turn_off()
                    elif key_press == "audionext":
                        # nightlight
                        write_out('. or virtual audionext pressed')
                        await wiz_light.turn_on(PilotBuilder(scene = 14))
                        
                    # not sure what to do with - or virutal brightnessdown
                    elif key_press == "brightnessdown":
                        # nightlight
                        write_out('- or virtual brightnessdown pressed')


              
                
        pygame.quit()


asyncio.run(main())

