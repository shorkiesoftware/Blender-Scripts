import bpy
import os
import array

os.system('cls')

objName = 'tree'
outFile = 'C:/Users/Dave/Desktop/tree.meshPNU'

vertices = []
indices = []


obj = bpy.data.objects[objName]
verts = obj.data.vertices
polys = obj.data.polygons
uvs = obj.data.uv_layers[0].data

#for u in uvs:
#    print(u.uv)

for p in polys:
    for v, l in zip(p.vertices, p.loop_indices):
        vertices.append(verts[v].co.x)
        vertices.append(verts[v].co.z)
        vertices.append(verts[v].co.y)
        vertices.append(verts[v].normal.x)
        vertices.append(verts[v].normal.z)
        vertices.append(verts[v].normal.y)
        vertices.append(uvs[l].uv.x)
        vertices.append(1 - uvs[l].uv.y)
        weight = [0, 0, 0, 0]
        bone = [0, 0, 0, 0]
        for j, g in enumerate(verts[v].groups):
            if j > 3:
                break
            weight[j] = g.weight
            bone[j] = g.group
        vertices.extend(weight)
        vertices.extend(bone)
        
    li = list(reversed(p.loop_indices))
    indices.append(li[0])
    indices.append(li[1])
    indices.append(li[2])
    i = 3
    while i < len(li):
        indices.append(li[i - 1])
        indices.append(li[i])
        indices.append(li[0])
        i += 1
        
file = open(outFile, 'wb')
array.array("I", [len(vertices) * 4]).tofile(file)
array.array("I", [len(indices) * 2]).tofile(file)
array.array("f", vertices).tofile(file)
array.array("h", indices).tofile(file)
file.close()

os.system('C:\\\"Program Files\"\\lz4\\lz4 ' + outFile)