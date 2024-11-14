import pygame as pg
import math
import os
import json

pg.init()

with open("config.json", "r") as file:
    jdata = json.load(file)

def load_obj(filename):
    vertices = []
    edges = []

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("v "):
                parts = line.split()
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                vertices.append([x, y, z])

            elif line.startswith("f "):
                parts = line.split()
                edge_indices = [int(p.split("/")[0]) - 1 for p in parts[1:]]
                for i in range(len(edge_indices)):
                    edges.append((edge_indices[i], edge_indices[(i + 1) % len(edge_indices)]))
            else: pass

    return vertices, edges

WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("3D Engine with Pygame :)")

SIZE_MULTIPLIER = jdata["size-multiplier"]
ROTATION_SPEED = jdata["rotation-speed"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

vertices, edges = load_obj(jdata["object"])
vertices = [[coord * SIZE_MULTIPLIER for coord in vertex] for vertex in vertices]

def rotate_x(vertex, angle):
    x, y, z = vertex
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return [x, y * cos_angle - z * sin_angle, y * sin_angle + z * cos_angle]

def rotate_y(vertex, angle):
    x, y, z = vertex
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return [x * cos_angle + z * sin_angle, y, -x * sin_angle + z * cos_angle]

def rotate_z(vertex, angle):
    x, y, z = vertex
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return [x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle, z]

def project(vertex):
    x, y, z = vertex
    factor = 200 / (z + 5)
    x = x * factor + WIDTH // 2
    y = -y * factor + HEIGHT // 2
    return [int(x), int(y)]

running = True
clock = pg.time.Clock()
angle_x = 0
angle_y = 0
angle_z = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # check for held down keys
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        angle_y += ROTATION_SPEED
    if keys[pg.K_d]:
        angle_y -= ROTATION_SPEED
    if keys[pg.K_w]:
        angle_x += ROTATION_SPEED
    if keys[pg.K_s]:
        angle_x -= ROTATION_SPEED
    if keys[pg.K_LEFT]:
        angle_z += ROTATION_SPEED
    if keys[pg.K_RIGHT]:
        angle_z -= ROTATION_SPEED

    screen.fill(BLACK)

    rotated_vertices = []

    for vertex in vertices:
        rotated_vertex = rotate_y(vertex, angle_y)
        rotated_vertex = rotate_x(rotated_vertex, angle_x)
        rotated_vertex = rotate_z(rotated_vertex, angle_z)
        rotated_vertices.append(rotated_vertex)

    projected_vertices = [project(v) for v in rotated_vertices]

    for edge in edges:
        start = projected_vertices[edge[0]]
        end = projected_vertices[edge[1]]
        pg.draw.line(screen, WHITE, start, end, 2)

    pg.display.flip()

    clock.tick(60)

os._exit(0)
