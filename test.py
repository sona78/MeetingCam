import os
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
rel_path = "../MeetingCam/filler/{}{}"
file_path = os.path.normpath(os.path.join(script_dir, rel_path))
print(file_path)
