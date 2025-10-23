import bpy
import array
import os
import subprocess

os.system('cls')

w = 1024
h = 1024

PI = 3.14159
HALF_PI = 1.570796

def checkImage(name):
    for i in bpy.data.images:
        if i.name == name:
            bpy.data.images.remove(i)

camDat = bpy.data.cameras.new(name='Camera')
cam = bpy.data.objects.new('Camera', camDat)
bpy.context.scene.collection.objects.link(cam)

totalPixelData = []


scene = bpy.data.scenes[0]
scene.render.resolution_x = w
scene.render.resolution_y = h
scene.render.image_settings.file_format = 'PNG'
scene.camera = cam

cam.data.lens_unit = 'FOV'
cam.data.angle = HALF_PI

cam.rotation_euler[0] = HALF_PI
cam.rotation_euler[2] = -HALF_PI
bpy.ops.render.render(write_still=True)
checkImage('posx')
pxImg = bpy.data.images.load("C:/tmp/.png")
pxImg.name = 'posx'
pxImg.pack()
pxImg.filepath_raw = "C:/Users/Dave/Desktop/px.png"
pxImg.save()

cam.rotation_euler[2] = HALF_PI
bpy.ops.render.render(write_still=True)
checkImage('negx')
nxImg = bpy.data.images.load("C:/tmp/.png")
nxImg.name = 'negx'
nxImg.pack()
nxImg.filepath_raw = "C:/Users/Dave/Desktop/nx.png"
nxImg.save()

cam.rotation_euler[2] = 0
cam.rotation_euler[0] = PI
bpy.ops.render.render(write_still=True)
checkImage('posy')
pyImg = bpy.data.images.load("C:/tmp/.png")
pyImg.name = 'posy'
pyImg.pack()
pyImg.filepath_raw = "C:/Users/Dave/Desktop/py.png"
pyImg.save()


cam.rotation_euler[0] = 0
bpy.ops.render.render(write_still=True)
checkImage('negy')
nyImg = bpy.data.images.load("C:/tmp/.png")
nyImg.name = 'negy'
nyImg.pack()
nyImg.filepath_raw = "C:/Users/Dave/Desktop/ny.png"
nyImg.save()

cam.rotation_euler[0] = HALF_PI
bpy.ops.render.render(write_still=True)
checkImage('posz')
pzImg = bpy.data.images.load("C:/tmp/.png")
pzImg.name = 'posz'
pzImg.pack()
pzImg.filepath_raw = "C:/Users/Dave/Desktop/pz.png"
pzImg.save()

cam.rotation_euler[2] = PI
bpy.ops.render.render(write_still=True)
checkImage('negz')
nzImg = bpy.data.images.load("C:/tmp/.png")
nzImg.name = 'negz'
nzImg.pack()
nzImg.filepath_raw = "C:/Users/Dave/Desktop/nz.png"
nzImg.save()


#inputFile = 'C:/tmp/skybox_pixel_data.spd'
#outputFile = 'D:/code/skateboard/assets/textures/outside.cubemap'
#program = 'D:/code/hdri_prefilterer/hdri_prefilterer'
#with open(inputFile, 'wb') as file:
#    array.array('I', [w, h, mips]).tofile(file)
#    array.array('f', totalPixelData).tofile(file)
#file.closed

#subprocess.run([program, inputFile, outputFile])

##CLEANUP
#cam.select_set(True)
#bpy.ops.object.delete()
#checkImage('posx')
#checkImage('negx')
#checkImage('posy')
#checkImage('negy')
#checkImage('posz')
#checkImage('negz')
#os.remove("C:/tmp/.hdr")
#os.remove(inputFile)

#print('DONE')