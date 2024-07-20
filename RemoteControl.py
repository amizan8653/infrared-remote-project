# source: https://www.circuitbasics.com/how-to-detect-keyboard-and-mouse-inputs-on-a-raspberry-pi/

import pygame
import subprocess

import time
import asyncio
import sys
import os
import re
from enum import Enum

# load virutal python environment libraries
sys.path.append('/home/amizan8653/.venv/lib/python3.11/site-packages')

# wiz lights library from virtual environment
from pywizlight import wizlight, PilotBuilder, discovery



class LAST_LIGHT_MODE(Enum):
    WARM = 1
    DAYLIGHT = 2
    NIGHTLIGHT = 3
    

def get_monitor_volume():
    shell_output = subprocess.run("ddcutil getvcp 62", shell=True, capture_output=True, text=True)
    if shell_output is not None and shell_output.stdout is not None:
        exp = re.compile(r"(current value =\s*)(\d+)")
        result = exp.search(shell_output.stdout)
        if result is not None and len(result.groups()) == 2:
            return int(result.group(2).strip())
    print("error in getting volume... returning a default to not crash rest of app")
    return 70
    


def get_next_volume(current, step):
    new_value = current + step
    new_value = min(100, new_value)
    new_value = max(0, new_value)
    return new_value


def set_monitor_volume(volume):
    subprocess.run("ddcutil setvcp 62 " + str(volume), shell=True)



def write_out(txt):
    print(txt)
    


async def lights_off(lights):
        for light in lights: 
                if light is not None:
                    try: 
                        await asyncio.wait_for(light.turn_off(), timeout=2)
                    except asyncio.TimeoutError:
                        print("timeout occur on light ON operation. aborting")

async def lights_on(lights, scene_number):
        for light in lights: 
                if light is not None:
                    try:
                        await asyncio.wait_for(light.turn_on(PilotBuilder(scene = scene_number)), timeout=2)
                    except asyncio.TimeoutError:
                        print("timeout occur on light OFF operation. aborting")

def get_candle_lights(): 
        # candle lightbulb initialization
        candle_wiz_bulb_ip_1 = "192.168.4.78"
        candle_wiz_bulb_ip_2 = "192.168.4.79"
        candle_wiz_bulb_ip_3 = "192.168.4.80"
        candle_lights = [wizlight(ip_address) for ip_address in [candle_wiz_bulb_ip_1, candle_wiz_bulb_ip_2, candle_wiz_bulb_ip_3]]
        return candle_lights
        
        
def get_main_light():
        # main lightbulb initiailzation
        main_wiz_bulb_ip = "192.168.4.21"
        main_wiz_light = [wizlight(main_wiz_bulb_ip)]
        return main_wiz_light


def monitor_hdmi_2():
        subprocess.run("ddcutil setvcp 60 18", shell=True)

def monitor_hdmi_1():
        subprocess.run("ddcutil setvcp 60 17", shell=True)

def monitor_dp():
        subprocess.run("ddcutil setvcp 60 15", shell=True)
        
async def main(): 
        write_out("entering main loop")


        # light level 0 = just main light to be turned on. level 1 means also turn on candle lights
        light_level = 1
        
        main_wiz_light = get_main_light()
        
        candle_lights = get_candle_lights()

        all_lights = main_wiz_light + candle_lights

        pygame.init()
        window = pygame.display.set_mode((300, 300), pygame.HWSURFACE)
        pygame.display.set_caption("Pygame Demonstration")
        
        current_volume = get_monitor_volume()

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
        
        last_light_mode = None

        mainloop=True
        while mainloop:
            time.sleep(0.1)
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
                        
                        
                    # Main Monitor input and 4x2 HDMI Matrix
                    elif key_press == "f17":
                        # display 1 - gaming pc
                        # switch to display port on MSI monitor. HDMI matrix - don't care.
                        write_out('7 or virtual f17 pressed')
                        monitor_dp()
                        
                    elif key_press == "f18":
                        # display 1 - mac
                        # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 4 out 1 with IR remote.
                        write_out('8 or virtual f18 pressed')
                        monitor_hdmi_1()
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO5", shell=True)
                    elif key_press == "scrolllock":
                        # display 1 - gfe
                        # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 2 out 2 with IR remote.
                        write_out('9 or virtual scrolllock pressed')
                        monitor_hdmi_1()
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO6", shell=True)
                    elif key_press == "cancel":
                        # display 1 - ps5
                        # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 4 out 2 with IR remote.
                        write_out('4 or virtual cancel pressed')
                        monitor_hdmi_1()
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO8", shell=True)
                    elif key_press == "menu":
                        # display 1 - switch
                        # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 3 out 2 with IR remote.
                        write_out('5 or virtual menu pressed')
                        monitor_hdmi_1()
                        subprocess.run("irsend SEND_ONCE matrix KEY_MACRO7", shell=True)
                    elif key_press == "brightnessup":
                        # display 1 - raspberry pi
                        # switch to hdmi 2 on MSI monitor. HDMI matrix - don't care.
                        monitor_hdmi_2()
                        write_out('6 or virtual brightnessup pressed')
                        
                        

                    # 8k_4x1_HDMI_SWITCH 
                    elif key_press == "numlock":
                        # display 2 - gaming pc
                        write_out('1 or virtual numlock pressed')
                        subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO3", shell=True)
                    elif key_press == "audiostop":
                        # display 2 - mac
                        write_out('2 or virtual audiostop pressed')
                        subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO4", shell=True)
                        
                        
                        
                        
                    # main monitor volume
                    elif key_press == "brightnessdown":
                        # volume up
                        write_out('- or virtual brightnessdown pressed')
                        current_volume = get_next_volume(current_volume, 10)
                        set_monitor_volume(current_volume)
                    elif key_press == "printscreen":
                        write_out('+ or virtual printscreen pressed')
                        # volume down
                        current_volume = get_next_volume(current_volume, -10)
                        set_monitor_volume(current_volume)
                        
                        
                    # wiz light
                    # scenes are from: https://github.com/sbidy/pywizlight/blob/6c6e4a2c5c7c2b46e5f3159e6d290d9099f6b923/pywizlight/scenes.py#L7
                    elif key_press == "audioplay":
                        # warm light
                        write_out('3 or virtual audioplay pressed')
                        if light_level == 0 or last_light_mode is not LAST_LIGHT_MODE.WARM:
                                await lights_on(main_wiz_light, 11)
                                await lights_off(candle_lights)
                        else: 
                                await lights_on(all_lights, 11)
                        light_level = (light_level + 1) % 2
                        last_light_mode = LAST_LIGHT_MODE.WARM
                        
                    elif key_press == "eject":
                        # daylight
                        write_out('enter or virtual eject pressed')
                        if light_level == 0 or last_light_mode is not LAST_LIGHT_MODE.DAYLIGHT:
                                await lights_on(main_wiz_light, 12)
                                await lights_off(candle_lights)
                        else: 
                                await lights_on(all_lights, 12)
                        light_level = (light_level + 1) % 2
                        last_light_mode = LAST_LIGHT_MODE.DAYLIGHT
                    elif key_press == "help":
                        # off
                        write_out('0 or virtual help pressed')
                        await lights_off(all_lights)
                        light_level = 0
                        last_light_mode = None
                    elif key_press == "audionext":
                        # nightlight
                        write_out('. or virtual audionext pressed')
                        if light_level == 0 or last_light_mode is not LAST_LIGHT_MODE.NIGHTLIGHT:
                                await lights_on(main_wiz_light, 14)
                                await lights_off(candle_lights)
                        else: 
                                await lights_on(all_lights, 14)
                        light_level = (light_level + 1) % 2
                        last_light_mode = LAST_LIGHT_MODE.NIGHTLIGHT
                        


              
                
        pygame.quit()


asyncio.run(main())

