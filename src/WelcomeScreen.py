#!/usr/bin/env python
import pygame
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_button import UIButton
from pygame.rect import Rect
import os

import Traffic as traffic

def start():

    pygame.init()

    window_surface = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("File Selector")

    background = pygame.Surface((600, 400))
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager((600, 400))
    clock = pygame.time.Clock()

    file_selection_label_button_message =pygame_gui.elements.UILabel(relative_rect=Rect(0, 50, 600, 100), manager=manager, text="Welcome to Vehicle Detector, press the button below to select a video file")
    file_selection_button               =UIButton                   (relative_rect=Rect(200, 150, 200, 50),manager=manager, text='Select File')
    file_selection_label_help_info_1    =pygame_gui.elements.UILabel(relative_rect=Rect(0, 225, 600, 100), manager=manager, text="Once the video is loaded, press p to pause the video")
    file_selection_label_help_info_2    =pygame_gui.elements.UILabel(relative_rect=Rect(157, 250, 275, 100), manager=manager, text="and")
    file_selection_label_help_info_3    =pygame_gui.elements.UILabel(relative_rect=Rect(0, 275, 600, 100), manager=manager, text="Press q to quit")


    while 1:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == file_selection_button:
                    file_selection = UIFileDialog(
                        rect=Rect(0, 0, 600, 600), manager=manager, allow_picking_directories=False)

                if event.ui_element == file_selection.ok_button:
                    print(file_selection.current_file_path)

                    if(os.path.exists(file_selection.current_file_path)):
                        traffic.traffic_detector(str(file_selection.current_file_path))

            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()

if __name__=="__main__":
    start()
