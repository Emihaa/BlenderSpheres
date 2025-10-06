import bpy
from mathutils import Vector
import random
import numpy as np

# Amount of spheres to be initialized
amount = 10
# Range to randomize the s_radius
min_radius = 0.1
max_radius = 2.0
# Range to randomize location
min_loc = -25.0
max_loc = 15.0
# Collection name
col_name = "spheres"
epsilon = 0.01

# Do the cage
# also redo the spawn points by checking the collision
# are the spheres supposed to grow the same amount or do they have their invidual len that they grow?
# invidual len for each sphere but grow all 0.1 once and then check collision for all and give boolean attribute of TRUE??
# shrink it backwards? halfen the amount it grows

class Sphere:
    def __init__(self, radius, pos, len, grow):
        self.radius = radius
        self.pos = pos
        self.len = len
        self.grow = grow

def phi(d):
    x = 2.0
    for i in range(10):
        x = (1 + x)**(1/(d+1))
    return (x)

def generate_points(n, d, seed):
    g = phi(d)
    alpha = np.array([pow(1/g, j+1) for j in range(d)])
    z = np.zeros((n, d))
    for i in range(n):
        z[i] = (seed + alpha*(i+1)) % 1
    return (z)

# Check if the collection exist if not create it, also delete possible spheres if any
def createCollection():
    if col_name in bpy.data.collections:
        print(f" correct collection found:")
        sphe_col = bpy.data.collections[col_name]
        array = [obj for obj in sphe_col.objects]
        for i in range(len(array)):
            s1 = array[i]
            bpy.data.objects.remove(s1, do_unlink=True) 
            #TODO: there might need to be a check that collection exists but there are no spheres
            #so that i dont delete things that dont exist
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

# grow spheres by scale of + 0.1 till it detects collision. When collision is detected
# divide by 2 the growth and try again, if len is less than 0.001 then stop and make grow = False
def growSpheres(spheres):
    grow = True
    while grow is True:
        grow = False
        for i in range(amount):
            if (spheres[i].grow is True):
                while (checkCollision(spheres[i], spheres) is True):
                    spheres[i].len /= 2
                    if (spheres[i].len < epsilon):
                        spheres[i].grow = False
                        break
                else:
                    spheres[i].radius += spheres[i].len
                    grow = True
    return (spheres)


# new code down here
# returns the sphere classes with the randomized radius and pos
def createSpheres():
    # Generate quasi-random points
    points = generate_points(amount, 3, seed = random.random())
    
    # Scale points to world space, leaving max_radius buffer
    world_min = min_loc + max_radius
    world_max = max_loc - max_radius
    scaled_points = world_min + points * (world_max - world_min)
    
    spheres = []
    for i in range(amount): #radius, pos, len, grow
        spheres.append(Sphere(random.uniform(min_radius, max_radius), Vector(scaled_points[i]), 0.1, True))
            
    return (spheres)

def main():
    spheres = createSpheres()
    growSpheres(spheres)
    spawnSpheres(spheres)
    

if __name__ == "__main__":
    main()