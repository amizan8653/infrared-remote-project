# source: https://www.circuitbasics.com/how-to-detect-keyboard-and-mouse-inputs-on-a-raspberry-pi/

import pygame
import subprocess

import time
import asyncio
import sys
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
    PLUS = "print screen"
    SEVEN = "f17"
    EIGHT = "f18"
    NINE = "scroll lock"
    FOUR = "cancel"
    FIVE = "menu"
    SIX = "brightnessup"
    THREE = "audioplay"
    ONE = "numlock"
    TWO = "audiostop"
    ENTER = "eject"
    ZERO = "help"    
    DOT = "ac bookmarks"
    A = "displayswitch"
    B = "mediaselect"
    C = "calculator"
    D = "ac search"
    E = "audionext"
    F = "audiofastforward"
    G = "ac home"
    

class DeviceSwitcher:

    def __init__(self, light_timeout=3):
            # light level 0 = just main light to be turned on. level 1 means also turn on candle lights
            self.lumen_level = 1
            self.all_lights = self.get_main_light() + self.get_candle_lights()

            pygame.init()
            
            # for some reason when running this as a service, leaving the mixer on breaks main monitor audio
            # disabling... we don't output sound anyways in this script.
            pygame.mixer.stop()
            pygame.mixer.quit()

            self.window = pygame.display.set_mode((300, 300), pygame.HWSURFACE)
            pygame.display.set_caption("Pygame Demonstration")
            
            self.current_volume = self.get_monitor_volume()
            self.last_light_mode = None

            self.light_timeout = light_timeout

            self.enum_value_to_key = {x.value: x for x in VIRTUAL_KEY_PRESS}

     
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
        DeviceSwitcher.write_out('\t{real} or virtual {virtual} pressed'.format(real=virtual_key, virtual=virtual_key.value))
        
        
    async def light_operation(self, lights, scene_numbers):
            try:
                # gather tasks with a timeout
                async with asyncio.timeout(self.light_timeout):
                    # run the tasks
                    await asyncio.gather(
                         *[
                              light.turn_on(PilotBuilder(scene = scene)) 
                              if scene is not None 
                              else light.turn_off() 
                              for light, scene in zip(lights, scene_numbers)])
                    print("\tLights operation completed successfully!")
                    return True
            except asyncio.TimeoutError:
                 print("\ttimeout during lights on operations. Aborting...")
                 return False
            

    def get_candle_lights(self): 
            # candle lightbulb initialization
            candle_wiz_bulb_ip_1 = "192.168.4.78"
            candle_wiz_bulb_ip_2 = "192.168.4.79"
            candle_wiz_bulb_ip_3 = "192.168.4.80"
            return [wizlight(ip_address) for ip_address in [candle_wiz_bulb_ip_1, candle_wiz_bulb_ip_2, candle_wiz_bulb_ip_3]]
            
            
    def get_main_light(self):
            # main lightbulb initiailzation
            main_wiz_bulb_ip = "192.168.4.21"
            return [wizlight(main_wiz_bulb_ip)]

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
                self.usb_1()
            case VIRTUAL_KEY_PRESS.EQUAL.value:
                self.usb_2()
            case VIRTUAL_KEY_PRESS.FORWARD_SLASH.value:
                self.usb_3()
            case VIRTUAL_KEY_PRESS.ASTERISK.value:
                self.usb_4()
                   
            # Main Monitor input and 4x2 HDMI Matrix
            case VIRTUAL_KEY_PRESS.SEVEN.value:
                # display 1 - gaming pc
                # switch to display port on MSI monitor. HDMI matrix - don't care.
                self.monitor_dp()
                
            case VIRTUAL_KEY_PRESS.EIGHT.value:
                # display 1 - mac
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 4 out 1 with IR remote.
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO5", shell=True)
            case VIRTUAL_KEY_PRESS.NINE.value:
                # display 1 - gfe
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 2 out 2 with IR remote.
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO6", shell=True)
            case VIRTUAL_KEY_PRESS.FOUR.value:
                # display 1 - ps5
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 4 out 2 with IR remote.
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO8", shell=True)
            case VIRTUAL_KEY_PRESS.FIVE.value:
                # display 1 - switch
                # switch to hdmi 1 on MSI monitor. Then set HDMI matrix in 3 out 2 with IR remote.
                self.monitor_hdmi_1()
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO7", shell=True)
            case VIRTUAL_KEY_PRESS.SIX.value:
                # display 1 - raspberry pi
                # switch to hdmi 2 on MSI monitor. HDMI matrix - don't care.
                self.monitor_hdmi_2()
            
            # 8k_4x1_HDMI_SWITCH 
            case VIRTUAL_KEY_PRESS.ONE.value:
                # display 2 - gaming pc
                subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO3", shell=True)
            case VIRTUAL_KEY_PRESS.TWO.value:
                # display 2 - mac
                subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO4", shell=True)
            case VIRTUAL_KEY_PRESS.THREE.value:
                # display 3 - raspberry pi
                subprocess.run("irsend SEND_ONCE 8K_4X1_HDMI_SWITCH KEY_MACRO5", shell=True)

            # main monitor volume
            case VIRTUAL_KEY_PRESS.MINUS.value:
                # volume up
                self.current_volume = self.get_next_volume(self.current_volume, 10)
                self.set_monitor_volume(self.current_volume)
            case VIRTUAL_KEY_PRESS.PLUS.value:
                # volume down
                self.current_volume = self.get_next_volume(self.current_volume, -10)
                self.set_monitor_volume(self.current_volume)
                
            # wiz light
            # scenes are from: https://github.com/sbidy/pywizlight/blob/6c6e4a2c5c7c2b46e5f3159e6d290d9099f6b923/pywizlight/scenes.py#L7
            # case VIRTUAL_KEY_PRESS.THREE.value:
            #     # warm light
            #     if self.lumen_level == 0 or self.last_light_mode is not LAST_LIGHT_MODE.WARM:
            #             print("\tturning on main warm light only")
            #             await self.light_operation(self.all_lights, [11, None, None, None])
            #     else: 
            #             print("\tturning all warm lights")
            #             await self.light_operation(self.all_lights, [11,11,11,11])
            #     self.lumen_level = (self.lumen_level + 1) % 2
            #     self.last_light_mode = LAST_LIGHT_MODE.WARM
                
            case VIRTUAL_KEY_PRESS.ENTER.value:
                # daylight
                if self.lumen_level == 0 or self.last_light_mode is not LAST_LIGHT_MODE.DAYLIGHT:
                        print("\tturning on main day light only")
                        await self.light_operation(self.all_lights, [12, None, None, None])
                else: 
                        print("\tturning all day lights")
                        await self.light_operation(self.all_lights, [12,12,12,12])
                self.lumen_level = (self.lumen_level + 1) % 2
                self.last_light_mode = LAST_LIGHT_MODE.DAYLIGHT
            case VIRTUAL_KEY_PRESS.ZERO.value:
                # off
                print("\tturning off all lights.")
                await self.light_operation(self.all_lights, [None, None, None, None])
                self.lumen_level = 0
                self.last_light_mode = None
            case VIRTUAL_KEY_PRESS.DOT.value:
                # nightlight
                if self.lumen_level == 0 or self.last_light_mode is not LAST_LIGHT_MODE.NIGHTLIGHT:
                        print("\tturning on main night light only")
                        await self.light_operation(self.all_lights, [14, None, None, None])
                else: 
                        print("\tturning all night lights")
                        await self.light_operation(self.all_lights, [14,14,14,14])
                self.lumen_level = (self.lumen_level + 1) % 2
                self.last_light_mode = LAST_LIGHT_MODE.NIGHTLIGHT 
            

    async def main(self): 
            self.write_out("entering main loop")

            mainloop=True
            while mainloop:
                time.sleep(0.05)
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        mainloop = False

                    if event.type == pygame.KEYDOWN:

                        self.write_out(pygame.key.name(event.key))
                        key_press = pygame.key.name(event.key).lower()

                        if key_press in self.enum_value_to_key.keys():
                             self.write_out_keypress(self.enum_value_to_key[key_press])
                             await self.execute_keypress(key_press) 
            pygame.quit()


if __name__ == "__main__":
    deviceSwitcher = DeviceSwitcher(light_timeout=5)
    asyncio.get_event_loop().run_until_complete(deviceSwitcher.main())
