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
    
    
class VIRTUAL_KEY_PRESS(Enum):
    BACKSPACE = "f13" 
    EQUAL = "f14"
    FORWARD_SLASH = "f15"
    ASTERISK = "f16"
    MINUS = "brightnessdown"
    PLUS = "printscreen"
    SEVEN = "f17"
    EIGHT = "f18"
    NINE = "scrolllock"
    FOUR = "cancel"
    FIVE = "menu"
    SIX = "brightnessup"
    THREE = "audioplay"
    ONE = "numlock"
    TWO = "audiostop"
    ENTER = "eject"
    ZERO = "help"    
    DOT = "audionext"
    

class DeviceSwitcher:

    def __init__(self):
            # light level 0 = just main light to be turned on. level 1 means also turn on candle lights
            self.light_level = 1
            self.main_wiz_light = self.get_main_light()
            self.candle_lights = self.get_candle_lights()
            self.all_lights = self.main_wiz_light + self.candle_lights

            pygame.init()
            self.window = pygame.display.set_mode((300, 300), pygame.HWSURFACE)
            pygame.display.set_caption("Pygame Demonstration")
            
            self.current_volume = self.get_monitor_volume()
            self.last_light_mode = None

     
    @staticmethod
    def get_monitor_volume():
        shell_output = subprocess.run("ddcutil getvcp 62", shell=True, capture_output=True, text=True)
        if shell_output is not None and shell_output.stdout is not None:
            exp = re.compile(r"(current value =\s*)(\d+)")
            result = exp.search(shell_output.stdout)
            if result is not None and len(result.groups()) == 2:
                return int(result.group(2).strip())
        print("error in getting volume... returning a default to not crash rest of app")
        return 70
        

    @staticmethod
    def get_next_volume(current, step):
        new_value = current + step
        new_value = min(100, new_value)
        new_value = max(0, new_value)
        return new_value

    @staticmethod
    def set_monitor_volume(volume):
        subprocess.run("ddcutil setvcp 62 " + str(volume), shell=True)


    @staticmethod
    def write_out(txt):
        print(txt)
        
    @staticmethod
    def write_out_keypress(virtual_key):
        DeviceSwitcher.write_out('{real} or virtual {virtual} pressed'.format(real=virtual_key, virtual=virtual_key.value))
        

    @staticmethod
    async def lights_off(lights):
            for light in lights: 
                    if light is not None:
                        try: 
                            await asyncio.wait_for(light.turn_off(), timeout=2)
                        except asyncio.TimeoutError:
                            print("timeout occur on light ON operation. aborting")

    @staticmethod
    async def lights_on(lights, scene_number):
            for light in lights: 
                    if light is not None:
                        try:
                            await asyncio.wait_for(light.turn_on(PilotBuilder(scene = scene_number)), timeout=2)
                        except asyncio.TimeoutError:
                            print("timeout occur on light OFF operation. aborting")

    def get_candle_lights(self): 
            # candle lightbulb initialization
            candle_wiz_bulb_ip_1 = "192.168.4.78"
            candle_wiz_bulb_ip_2 = "192.168.4.79"
            candle_wiz_bulb_ip_3 = "192.168.4.80"
            self.candle_lights = [wizlight(ip_address) for ip_address in [candle_wiz_bulb_ip_1, candle_wiz_bulb_ip_2, candle_wiz_bulb_ip_3]]
            return self.candle_lights
            
            
    def get_main_light(self):
            # main lightbulb initiailzation
            main_wiz_bulb_ip = "192.168.4.21"
            self.main_wiz_light = [wizlight(main_wiz_bulb_ip)]
            return self.main_wiz_light

    @staticmethod
    def monitor_hdmi_2():
            subprocess.run("ddcutil setvcp 60 18", shell=True)

    @staticmethod
    def monitor_hdmi_1():
            subprocess.run("ddcutil setvcp 60 17", shell=True)

    @staticmethod
    def monitor_dp():
            subprocess.run("ddcutil setvcp 60 15", shell=True)

    @staticmethod
    def usb_1():
        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO1", shell=True)

    @staticmethod
    def usb_2(): 
        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO2", shell=True)

    @staticmethod
    def usb_3():
        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO3", shell=True) 

    @staticmethod
    def usb_4():
        subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO4", shell=True)
        

    async def execute_keypress(self, key_press):
        match key_press:
            # USB hub
            case VIRTUAL_KEY_PRESS.BACKSPACE.value:
                self.write_out_keypress(VIRTUAL_KEY_PRESS.BACKSPACE)
                self.usb_1()
            case VIRTUAL_KEY_PRESS.EQUAL.value:
                self.write_out_keypress(VIRTUAL_KEY_PRESS.EQUAL)
                self.usb_2()
            case VIRTUAL_KEY_PRESS.FORWARD_SLASH.value:
                self.write_out_keypress(VIRTUAL_KEY_PRESS.FORWARD_SLASH)
                self.usb_3()
            case VIRTUAL_KEY_PRESS.ASTERISK.value:
                self.write_out_keypress(VIRTUAL_KEY_PRESS.ASTERISK)
                self.usb_4()
                   
            # Main Monitor input and 4x2 HDMI Matrix
            case VIRTUAL_KEY_PRESS.SEVEN.value:
                # display 1 - gaming pc
                # switch to display port on MSI monitor. HDMI matrix - don't care.
                self.write_out_keypress(VIRTUAL_KEY_PRESS.SEVEN)
                self.monitor_dp()
                
            case VIRTUAL_KEY_PRESS.EIGHT.value:
                # display 1 - mac
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 4 out 1 with IR remote.
                self.write_out_keypress(VIRTUAL_KEY_PRESS.EIGHT)
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO5", shell=True)
            case VIRTUAL_KEY_PRESS.NINE.value:
                # display 1 - gfe
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 2 out 2 with IR remote.
                self.write_out_keypress(VIRTUAL_KEY_PRESS.NINE)
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO6", shell=True)
            case VIRTUAL_KEY_PRESS.FOUR.value:
                # display 1 - ps5
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 4 out 2 with IR remote.
                self.write_out_keypress(VIRTUAL_KEY_PRESS.FOUR)
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO8", shell=True)
            case VIRTUAL_KEY_PRESS.FIVE.value:
                # display 1 - switch
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 3 out 2 with IR remote.
                self.write_out_keypress(VIRTUAL_KEY_PRESS.FIVE)
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO7", shell=True)
            case VIRTUAL_KEY_PRESS.SIX.value:
                # display 1 - raspberry pi
                # switch to hdmi 2 on MSI monitor. HDMI matrix - don't care.
                self.write_out_keypress(VIRTUAL_KEY_PRESS.SIX)
                self.monitor_hdmi_2()
            
            # 8k_4x1_HDMI_SWITCH 
            case VIRTUAL_KEY_PRESS.ONE.value:
                # display 2 - gaming pc
                self.write_out_keypress(VIRTUAL_KEY_PRESS.ONE)
                subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO3", shell=True)
            case VIRTUAL_KEY_PRESS.TWO.value:
                # display 2 - mac
                self.write_out_keypress(VIRTUAL_KEY_PRESS.TWO)
                subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO4", shell=True)
                
            # main monitor volume
            case VIRTUAL_KEY_PRESS.MINUS.value:
                # volume up
                self.write_out_keypress(VIRTUAL_KEY_PRESS.MINUS)
                self.current_volume = self.get_next_volume(self.current_volume, 10)
                self.set_monitor_volume(self.current_volume)
            case VIRTUAL_KEY_PRESS.PLUS.value:
                self.write_out_keypress(VIRTUAL_KEY_PRESS.PLUS)
                # volume down
                self.current_volume = self.get_next_volume(self.current_volume, -10)
                self.set_monitor_volume(self.current_volume)
                
            # wiz light
            # scenes are from: https://github.com/sbidy/pywizlight/blob/6c6e4a2c5c7c2b46e5f3159e6d290d9099f6b923/pywizlight/scenes.py#L7
            case VIRTUAL_KEY_PRESS.THREE.value:
                # warm light
                self.write_out_keypress(VIRTUAL_KEY_PRESS.THREE)
                if self.light_level == 0 or self.last_light_mode is not LAST_LIGHT_MODE.WARM:
                        await self.lights_on(self.main_wiz_light, 11)
                        await self.lights_off(self.candle_lights)
                else: 
                        await self.lights_on(self.all_lights, 11)
                self.light_level = (self.light_level + 1) % 2
                self.last_light_mode = LAST_LIGHT_MODE.WARM
                
            case VIRTUAL_KEY_PRESS.ENTER.value:
                # daylight
                self.write_out_keypress(VIRTUAL_KEY_PRESS.ENTER)
                if self.light_level == 0 or self.last_light_mode is not LAST_LIGHT_MODE.DAYLIGHT:
                        await self.lights_on(self.main_wiz_light, 12)
                        await self.lights_off(self.candle_lights)
                else: 
                        await self.lights_on(self.all_lights, 12)
                self.light_level = (self.light_level + 1) % 2
                self.last_light_mode = LAST_LIGHT_MODE.DAYLIGHT
            case VIRTUAL_KEY_PRESS.ZERO.value:
                # off
                self.write_out_keypress(VIRTUAL_KEY_PRESS.ZERO)
                await self.lights_off(self.all_lights)
                self.light_level = 0
                self.last_light_mode = None
            case VIRTUAL_KEY_PRESS.DOT.value:
                # nightlight
                self.write_out_keypress(VIRTUAL_KEY_PRESS.DOT)
                if self.light_level == 0 or self.last_light_mode is not LAST_LIGHT_MODE.NIGHTLIGHT:
                        await self.lights_on(self.main_wiz_light, 14)
                        await self.lights_off(self.candle_lights)
                else: 
                        await self.lights_on(self.all_lights, 14)
                self.light_level = (self.light_level + 1) % 2
                self.last_light_mode = LAST_LIGHT_MODE.NIGHTLIGHT 
            

    async def main(self): 
            self.write_out("entering main loop")

            mainloop=True
            while mainloop:
                time.sleep(0.1)
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        mainloop = False

                    if event.type == pygame.KEYDOWN:

                        self.write_out(pygame.key.name(event.key))
                        key_press = pygame.key.name(event.key).lower().replace(" ", "")
                        await self.execute_keypress(key_press) 
            pygame.quit()


if __name__ == "__main__":
    deviceSwitcher = DeviceSwitcher()
    asyncio.run(deviceSwitcher.main())
