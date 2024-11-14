import pygame as pg
import math
import os

pg.init()

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

size_multiplier = 1.5
rotation_speed = 0.05

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

vertices, edges = load_obj("cube.obj")
vertices = [[coord * size_multiplier for coord in vertex] for vertex in vertices]

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

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # check for held down keys
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        angle_y += rotation_speed
    if keys[pg.K_d]:
        angle_y -= rotation_speed
    if keys[pg.K_w]:
        angle_x += rotation_speed
    if keys[pg.K_s]:
        angle_x -= rotation_speed

    screen.fill(BLACK)

    rotated_vertices = []

    for vertex in vertices:
        rotated_vertex = rotate_y(rotate_x(vertex, angle_x), angle_y)
        rotated_vertices.append(rotated_vertex)

    projected_vertices = [project(v) for v in rotated_vertices]

    for edge in edges:
        start = projected_vertices[edge[0]]
        end = projected_vertices[edge[1]]
        pg.draw.line(screen, WHITE, start, end, 2)

    pg.display.flip()

    clock.tick(60)

os._exit(0)