import bpy
import array
import math
import mathutils
from os import system

system('cls')

startFrame = 400
endFrame = 424
resetDuration = 1 / 24
outputFile = "D:/code/skateboard/assets/animations/walk.animation"
armatureName = 'Armature'

arm = bpy.data.objects[armatureName]
scene = bpy.data.scenes['Scene']
fcurves = arm.animation_data.action.fcurves
bones = arm.pose.bones
orientations = []
rootPositions = []
frameDurations = []

class Counter:
    ctr = 0

def getKeyframesInRange(fcurves, startFrame, endFrame):
    keyframes = []
    for f in fcurves:
        for k in f.keyframe_points:
            kf = k.co.x
            if kf >= startFrame and kf <= endFrame:
                keyframes.append(kf)
                
    keyframes = list(set(keyframes))
    keyframes.sort()
    return keyframes


def parseBone(bone, parent, pid, counter):
    index = counter.ctr
    counter.ctr += 1
    
    mat = 0
    if parent is not None:
        mat = parent.matrix.inverted() @ bone.matrix
    else:
        mat = bone.matrix
        
    rot = mat.to_quaternion()
    orientations.append(-rot.x)
    orientations.append(-rot.y)
    orientations.append(rot.z)
    orientations.append(rot.w)
    
    for c in bone.children:
        parseBone(c, bone, index, counter)
    

scene.frame_set(startFrame)

kfms = getKeyframesInRange(fcurves, startFrame, endFrame)

bpy.ops.object.select_all(action='DESELECT')
arm.select_set(True)
arm.rotation_euler = mathutils.Euler((-1.5707963, 0, 0), 'XYZ')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

for i, k in enumerate(kfms):
    if i < len(kfms) - 1:
        frameDurations.append((kfms[i + 1] - k) / bpy.context.scene.render.fps)
    else:
        frameDurations.append(resetDuration)
    
    scene.frame_set(int(k))
    count = Counter()
    rootPositions.append(bones[0].matrix[0][3])
    rootPositions.append(bones[0].matrix[1][3])
    rootPositions.append(-bones[0].matrix[2][3])
    parseBone(bones[0], None, 0, count)

arm.rotation_euler = mathutils.Euler((1.5707963, 0, 0), 'XYZ')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


file = open(outputFile, "wb")
array.array("I", [len(kfms)]).tofile(file)
array.array("I", [len(arm.data.bones)]).tofile(file)
array.array("f", frameDurations).tofile(file)
array.array("f", rootPositions).tofile(file)
array.array("f", orientations).tofile(file)
file.close()
    
print("DONE")