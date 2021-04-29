import cv2
import pyvirtualcam
import PySimpleGUI as sg
import os
import keyboard
import imageio

video = cv2.VideoCapture(0)


def main():
    inputShape = video.read()[1].shape
    camHeight = inputShape[0]
    camWidth = inputShape[1]
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
        if event == sg.WIN_CLOSED:
            exit(0)
        if event == 'Continue':
            window.close()
            break
        window.FindElement('image').Update(data=cv2.imencode('.png', video.read()[1])[1].tobytes()) 


    layout = [  [sg.Text('Please enter the file name of the image or video to use from the filler folder:'), sg.InputText()],
                [sg.Text('What is the file type?'), sg.Combo(['.png', '.avi'], enable_events=True)],
                [sg.Button('Continue'), sg.Button('Take a New Photo'), sg.Button('Make a New Video')],]
    window = sg.Window('Virtual Camera Hub', layout)


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event == sg.WIN_CLOSED:
            exit(0)
        if event == 'Continue' and values[0] != "" and values[1] != "":
            fileName = values[0]
            fileType = values[1]
            window.close()
            break
        if event == "Take a New Photo" or event == "Make a New Video":
            window.close()
            break

    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path = "./filler/"
    dir_path = os.path.normpath(os.path.join(script_dir, rel_path))

    photoLayout = [[sg.Text('Take a New Photo', size=(40, 1), justification='center', font='Helvetica 20')],[sg.Image(filename='', key='image')], [sg.Button("Take Photo")],]
    photoWindow = sg.Window('Virtual Camera Hub', photoLayout)

    if event == "Take a New Photo":
        while True:
            button, values = photoWindow.Read(timeout=20, timeout_key='timeout')
            ret, frame = video.read()
            if button == 'Take Photo':
                fileName = 'Capture'
                fileType = '.png'
                fileCombine = fileName + fileType
                os.chdir(dir_path)
                cv2.imwrite(fileCombine, frame)
                photoWindow.close()
                break
            photoWindow.FindElement('image').Update(data=cv2.imencode('.png', video.read()[1])[1].tobytes())
                
    videoLayout = [[sg.Text('Make a New Video', size=(40, 1), justification='center', font='Helvetica 20')],[sg.Image(filename='', key='image')], [sg.Button("Start Video"), sg.Button("Stop Video")]]
    videoWindow = sg.Window('Virtual Camera Hub', videoLayout)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path = "./filler/Video.avi"
    dir_path = os.path.normpath(os.path.join(script_dir, rel_path))

    if event == "Make a New Video":
        events = []
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(dir_path, fourcc, 30, (640, 480))

        while True:
            button, values = videoWindow.Read(timeout=20, timeout_key='timeout')
            events.append(button)
            ret, frame = video.read()
            if button == 'Start Video' or 'Start Video' in events:
                fileName = 'Video'
                fileType = '.avi'
                fileCombine = fileName + fileType
                out.write(frame)
            if button == 'Stop Video' and 'Start Video' in events:
                out.release()
                videoWindow.close()
                break
            videoWindow.FindElement('image').Update(data=cv2.imencode('.png', video.read()[1])[1].tobytes())



    layout = [  [sg.Text('Activate Virtual Camera', size=(40, 1), justification='center', font='Helvetica 20')],
                [sg.Button('Webcam'), sg.Button('Filler'), sg.Button('Exit')],]

    window = sg.Window('Virtual Camera Hub', layout)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path = "./filler/{}{}".format(fileName, fileType)
    
    if event == "Take a New Photo":
        rel_path = "../filler/{}{}".format(fileName, fileType)
    file_path = os.path.normpath(os.path.join(script_dir, rel_path))

    if fileType == '.png':
        filler = imageio.imread(file_path)
        frameFinal = cv2.resize(filler, (640, 480))
        frameFinal = cv2.cvtColor(frameFinal, cv2.COLOR_RGBA2RGB)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path = "./filler/{}{}".format(fileName, fileType)
    file_path = os.path.normpath(os.path.join(script_dir, rel_path))

    if fileType == '.avi':
        frameVideo = cv2.VideoCapture(file_path)
        length = int(frameVideo.get(cv2.CAP_PROP_FRAME_COUNT))

    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        exit(0)
    if event == "Webcam":
        window.close()
    if event == "Filler":
        window.close()

    with pyvirtualcam.Camera(height=camHeight, width=camWidth, fps=30) as cam:
            print(f'Using virtual camera: {cam.device}')
            if fileType == '.avi':
                count = 1
                reverse = False
                frameList = []

                while len(frameList) != length:
                    ret, frame = frameVideo.read()
                    if not ret:
                        raise RuntimeError('Error fetching frame')
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frameList.append(frame)
                
            while True:
                ret, frame = video.read()
                
                if not ret:
                    raise RuntimeError('Error fetching frame')
                
                RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if event == "Webcam":
                    cam.send(RGBframe)
                if event == "Filler":
                    if fileType == ".png":
                        cam.send(frameFinal)
                    elif fileType == ".avi":
                        frame = frameList[count]
                        if count == length - 1 or count == 0:
                            reverse = not reverse           
                        cam.send(frame)
                        if reverse == True:
                            count -= 1
                        elif reverse == False:
                            count += 1

                if keyboard.is_pressed(chr(27)):
                    break


                cam.sleep_until_next_frame()


main()
