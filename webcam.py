import cv2
import pyvirtualcam
from PIL import Image
import numpy as np
import PySimpleGUI as sg
import os
import imageio

video = cv2.VideoCapture(0)


def main():
    inputShape = video.read()[1].shape
    camHeight = inputShape[0]
    camWidth = inputShape[1]
    toggle = True
    fileName = ""
    sg.theme('Black')

    layout = [[sg.Text("Welcome to the Virtual Camera Hub!")], [sg.Button("Continue")]]
    window = sg.Window("Virtual Camera Hub", layout)


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event == "Continue" or event == sg.WIN_CLOSED:
            window.close()
            break

    layout = [[sg.Text('Continue if this is the correct webcam', size=(40, 1), justification='center', font='Helvetica 20')],[sg.Image(filename='', key='image')], [sg.Button("Continue")],]
    window = sg.Window('Virtual Camera Hub', layout)

    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event == 'Continue' or event == sg.WIN_CLOSED:
            window.close()
            break
        window.FindElement('image').Update(data=cv2.imencode('.png', video.read()[1])[1].tobytes()) 


    layout = [  [sg.Text('Please enter the file name of the image or video to use from the filler folder:'), sg.InputText()],
                [sg.Text('What is the file type?'), sg.Combo(['.png', '.jpg'], enable_events=True)],
                [sg.Button('Continue'), sg.Button('Take a New Photo'), sg.Button('Make a New Video')],]
    window = sg.Window('Virtual Camera Hub', layout)

    photoLayout = [[sg.Text('Take a New Photo', size=(40, 1), justification='center', font='Helvetica 20')],[sg.Image(filename='', key='image')], [sg.Button("Take Photo")],]
    photoWindow = sg.Window('Virtual Camera Hub', photoLayout)
        

    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event == 'Continue' or event == sg.WIN_CLOSED:
            fileName = values[0]
            fileType = values[1]
            window.close()
            break
        if event == "Take a New Photo":
            while True:
                button, values = photoWindow.Read(timeout=20, timeout_key='timeout')
                photoWindow.FindElement('image').Update(data=cv2.imencode('.png', video.read()[1])[1].tobytes())
                print(cv2.imencode('.png', video.read()[1])[1].tobytes())
                
    

    layout = [  [sg.Text('Virtual Camera is Active', size=(40, 1), justification='center', font='Helvetica 20')],
                [sg.Button('Webcam'), sg.Button('Filler'), sg.Button('Exit')],]

    window = sg.Window('Virtual Camera Hub', layout)

    script_dir = os.path.dirname(__file__)
    rel_path = "../MeetingCam/filler/{}{}".format(fileName, fileType)
    file_path = os.path.normpath(os.path.join(script_dir, rel_path))

    filler = imageio.imread(file_path)

    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        window.close()
    if event == "Webcam":
        window.close()
    if event == "Filler":
        frameFinal = cv2.resize(filler, (640, 480))
        frameFinal = cv2.cvtColor(frameFinal, cv2.COLOR_RGBA2RGB)
        window.close()

    with pyvirtualcam.Camera(height=camHeight, width=camWidth, fps=30) as cam:
            print(f'Using virtual camera: {cam.device}')
            while True:
                ret, frame = video.read()
                if not ret:
                    raise RuntimeError('Error fetching frame')
                
                RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                if event == "Webcam":
                    cam.send(RGBframe)
                if event == "Filler":
                    cam.send(frameFinal)
                
                cam.sleep_until_next_frame()
'''
try:
    main()
except:
    layout = [[sg.Text("Error")], [sg.Button("Exit")]]
    window = sg.Window("Virtual Camera Hub", layout)


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            break
'''
main()
