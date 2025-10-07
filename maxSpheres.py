import bpy
from mathutils import Vector
import random

# Amount of spheres to be initialized
amount = 7
# Range to randomize the s_radius
min_radius = 0.1
max_radius = 2.0
# Range to randomize location
min_loc = -10.0
max_loc = 15.0
# Collection name
col_name = "spheres"
epsilon = 0.01

# Do the cage, how do i do cage and how do i check the collision with the cage?

class Sphere:
    def __init__(self, radius, pos, len, grow, collision):
        self.radius = radius
        self.pos = pos
        self.len = len
        self.grow = grow
        self.collision = collision

# Check if the collection exist if not create it, also delete possible spheres if any
def createCollection():
    if col_name in bpy.data.collections:
        print(f" correct collection found:")
        sphe_col = bpy.data.collections[col_name]
        for obj in sphe_col.objects:
            bpy.data.objects.remove(obj, do_unlink=True) 
    else:
        print(f" creating a new collection:")
        sphe_col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(sphe_col)
    return (sphe_col)

# Uses shadeSmooth on the sphere
def shadeSmooth():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()

# in the end we spawn the spheres to the collection
def spawnSpheres(spheres):
    sphe_col = createCollection()
    for i in range(amount):
        bpy.ops.mesh.primitive_uv_sphere_add(radius = spheres[i].radius, enter_editmode=False, location=spheres[i].pos, scale=(1, 1, 1))
        sphere = bpy.context.active_object
        shadeSmooth()
        if (sphe_col not in sphere.users_collection):
            sphe_col.objects.link(sphere)

# Check the collision by calculating the distance between the spheres and minuses the radiuses
# if ANY collision happens the function will stop and return True
def checkCollision(s1, spheres):
    for s2 in spheres:
        if (s1 is not s2):
            distance = (s1.pos - s2.pos).length
            distance -= (s1.radius + s2.radius)
            if (distance < 0):
                return (True)
    return (False)

# grow the spheres by the len
# on the second loop check if collisions happens
# if collision is happening then move the radius back by len and /2 the len
# or then the len is smaller than epsilon and we are done growing
def growSpheres(spheres):
    loop = True
    while loop is True:
        loop = False
        for i in range(amount):
            if (spheres[i].grow is True):
                if (spheres[i].collision is True):
                    spheres[i].radius -= spheres[i].len
                    spheres[i].len /= 2
                    spheres[i].collision = False
                    if (spheres[i].len < epsilon):
                        spheres[i].grow = False
                        continue
                else:
                    spheres[i].radius += spheres[i].len
                    loop = True
        for i in range(amount):
            if (spheres[i].grow is True):
                spheres[i].collision = checkCollision(spheres[i], spheres)

# generate 3 times more than the sphere amount, randomized positions within the given boundaries
# also gives as end point of how many tries we will give this code to generate random pos
def generateRandomPoints():
    points = []

    for i in range(amount * 3):
        pos = Vector((random.uniform(min_loc, max_loc), random.uniform(min_loc, max_loc), random.uniform(min_loc, max_loc)))
        points.append(pos)
    return (points)


# returns the sphere classes with the randomized radius and pos
# or returns empthy list
def createSpheres():
    points = generateRandomPoints()

    spheres = []
    s_amount = 0
    for i in range(amount * 3):
        s = Sphere ( #radius, pos, len, grow
            random.uniform(min_radius, max_radius), 
            Vector(points[i]), 0.1, 
            True, 
            False )
        spheres.append(s)
        if (checkCollision(spheres[i], spheres) is False):
            s_amount += 1
        else:
            spheres.pop()
        if (s_amount == amount):
            return (spheres) 
    return ()

# Should now create a box in wire displaymode to show case the boundaries
def createBox():
    col_name = "Collection"
    if col_name in bpy.data.collections:
        col = bpy.data.collections[col_name]
        for obj in col.objects:
            if obj.name == "Box":
                bpy.data.objects.remove(obj, do_unlink=True)
        dimension = (abs(min_loc) + max_loc)
        bpy.ops.mesh.primitive_cube_add(size=2.0, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(dimension, dimension, dimension))
        box = bpy.context.active_object
        box.name = "Box"
        box.display_type = 'WIRE'
        box = bpy.context.active_object
        col.objects.link(box)

def main():
    spheres = createSpheres()
    if not (spheres):
        print(f"No valid positions for spheres, check the limitations")
        return 
    growSpheres(spheres)
    spawnSpheres(spheres)
    createBox()
    

if __name__ == "__main__":
    main()