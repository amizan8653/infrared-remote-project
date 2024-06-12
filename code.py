# source: https://www.circuitbasics.com/how-to-detect-keyboard-and-mouse-inputs-on-a-raspberry-pi/
# source ~/venv/bin/activate && cd ~/Desktop && python pyfile.py

import pygame
import subprocess

pygame.init()
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pygame Demonstration")

mainloop=True
while mainloop:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            mainloop = False

        if event.type == pygame.KEYDOWN:

            # print(pygame.key.name(event.key))
            
            # USB hub
            if pygame.key.name(event.key) == "backspace":
                # usb 1
                print('backspace pressed')
                subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO1", shell=True)
            elif pygame.key.name(event.key) == "=":
                # usb 2
                print('= pressed')
                subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO2", shell=True)
            elif pygame.key.name(event.key) == "[/]":
                # usb 3
                print('/ pressed')
                subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO3", shell=True)
            elif pygame.key.name(event.key) == "[*]":
                # usb 4
                print('* pressed')
                subprocess.run("irsend SEND_ONCE rybozen KEY_MACRO4", shell=True)
                
                
            # 4x2 HDMI Matrix
            elif pygame.key.name(event.key) == "[7]":
                # display 1 - gaming pc
                # switch to display port on MSI monitor by pressing "ctrl shift alt f1 on keyboard". HDMI matrix - don't care.
                print('4 pressed')
                
            elif pygame.key.name(event.key) == "[8]":
                # display 1 - mac
                # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 4 out 1 with IR remote.
                print('5 pressed')
                
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO5", shell=True)
            elif pygame.key.name(event.key) == "[9]":
                # display 1 - gfe
                # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 2 out 2 with IR remote.
                print('6 pressed')
                
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO6", shell=True)
            elif pygame.key.name(event.key) == "[4]":
                # display 1 - ps5
                # switch to hdmi 2 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". HDMI matrix - don't care.
                print('1 pressed')

            elif pygame.key.name(event.key) == "[5]":
                # display 1 - switch
                # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 3 out 2 with IR remote.
                print('2 pressed')
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO7", shell=True)
            elif pygame.key.name(event.key) == "[6]":
                # display 1 - raspberry pi
                # switch to hdmi 1 on MSI monitor by pressing "ctrl shift alt f2 on keyboard". Then set HDMI matrix in 4 out 2 with IR remote.
                print('3 pressed')
                subprocess.run("irsend SEND_ONCE matrix KEY_MACRO8", shell=True)
                

            # sgeyr 3x1 hdmi switch
            elif pygame.key.name(event.key) == "[1]":
                # display 2 - gaming pc
                print('7 pressed')
                subprocess.run("irsend SEND_ONCE sgeyr_3x1_hdmi_switch KEY_MACRO2", shell=True)
            elif pygame.key.name(event.key) == "[2]":
                # display 2 - mac
                print('8 pressed')
                subprocess.run("irsend SEND_ONCE sgeyr_3x1_hdmi_switch KEY_MACRO3", shell=True)
            elif pygame.key.name(event.key) == "[3]":
                # display 2 - gfe
                print('9 pressed')
                subprocess.run("irsend SEND_ONCE sgeyr_3x1_hdmi_switch KEY_MACRO4", shell=True)
        
            elif pygame.key.name(event.key) == "[+]":
                # warm light
                print('+ pressed')
            elif pygame.key.name(event.key) == "enter":
                # daylight
                print('enter pressed')
            elif pygame.key.name(event.key) == "[0]":
                # off
                print('0 pressed')
            elif pygame.key.name(event.key) == "[.]":
                # night light
                print('. pressed')
                
            # not sure what to do with this
            elif pygame.key.name(event.key) == "[-]":
                # not sure what to do with this. before it was the sgeyr 3x1 switch's switch button
                print('- pressed')
                subprocess.run("irsend SEND_ONCE sgeyr_3x1_hdmi_switch KEY_MACRO5", shell=True)
                
pygame.quit()
