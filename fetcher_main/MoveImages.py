import sys, os, glob, shutil

#move images to folder:images
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Images"
abs_file_path = os.path.join(script_dir, rel_path)
if not os.path.exists(abs_file_path):
    os.mkdir(abs_file_path)

in_dir = script_dir
out_dir = abs_file_path
new_dirs = os.listdir(in_dir)
old_dirs = os.listdir(out_dir)

#See if directory already exists. If it doesnt exists, move entire directory. If it does exists, move only new images.
for dir in new_dirs:
    if ((dir not in old_dirs) and (dir.endswith(".jpg"))):
        shutil.move(dir, out_dir)
    else:
        new_images = glob.glob(in_dir + dir + '*.jpg')
        for i in new_images:
            shutil.move(i, os.path.join(out_dir, dir, os.path.basename(i)))
