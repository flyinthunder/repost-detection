import os
from PIL import Image

#move images to folder:images
def move():
    script_dir = os.path.dirname(os.path.dirname(__file__)) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, "fetcher_main\\Images")

    if (os.path.exists(abs_file_path) == False):
        os.mkdir(abs_file_path)

    files = os.listdir(script_dir)

    for file in files:
        #print(file)
        try:
            typ = file.split(".")[1]
            if ((typ == "jpg") or (typ == "png")):
                img = Image.open(os.path.join(script_dir, file))
                img.save(os.path.join(abs_file_path, file))
                os.remove(os.path.join(script_dir, file))
        except Exception as e:
            #print(e)
            pass



