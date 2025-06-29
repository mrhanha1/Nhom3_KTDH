import pygame
import math
import file_2D

# Hàm chuyển đổi từ tọa độ thực tế sang pixel pygame (gốc O giữa màn hình)
def to_pygame_coords(x, y, draw_area=None, UNIT_SIZE=3, zoom_level=1.0, camera_offset=(0,0)):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    center_x = draw_area.x + draw_area.width / 2 + camera_offset[0]
    center_y = draw_area.y + draw_area.height / 2 + camera_offset[1]
    px = center_x + x * UNIT_SIZE * zoom_level
    py = center_y - y * UNIT_SIZE * zoom_level
    return (px, py)

def project_cabinet(x, y, z, UNIT_SIZE=3, draw_area=None, zoom_level=1.0, camera_offset=(0, 0)):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    center_x = draw_area.x + draw_area.width / 2 + camera_offset[0]
    center_y = draw_area.y + draw_area.height / 2 + camera_offset[1]
    angle = math.radians(225)
    scale_z = 0.5
    proj_x = x * zoom_level + scale_z * z * math.cos(angle) * zoom_level
    proj_y = y * zoom_level + scale_z * z * math.sin(angle) * zoom_level
    pygame_x = center_x + proj_x * UNIT_SIZE
    pygame_y = center_y - proj_y * UNIT_SIZE
    return (pygame_x, pygame_y)

def draw_3d_axes(screen, UNIT_SIZE=3, draw_area=None, axis_length=100, zoom_level=1.0, camera_offset=(0,0)):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    # Gốc O thực tế (0,0,0)
    origin = project_cabinet(0, 0, 0, UNIT_SIZE, draw_area, zoom_level, camera_offset)
    x_end = project_cabinet(axis_length, 0, 0, UNIT_SIZE, draw_area, zoom_level, camera_offset)
    y_end = project_cabinet(0, axis_length, 0, UNIT_SIZE, draw_area, zoom_level, camera_offset)
    z_end = project_cabinet(0, 0, axis_length, UNIT_SIZE, draw_area, zoom_level, camera_offset)
    # Vẽ trục
    pygame.draw.line(screen, (255,0,0), origin, x_end, 2)
    pygame.draw.line(screen, (0,255,0), origin, y_end, 2)
    pygame.draw.line(screen, (0,0,255), origin, z_end, 2)
    font = pygame.font.SysFont('arial', 15)
    # Vẽ vạch chia và số trên trục X
    tick_interval = 10
    for i in range(1, axis_length // tick_interval + 1):
        # Trục X
        tx, ty, tz = i * tick_interval, 0, 0
        tick_pos = project_cabinet(tx, ty, tz, UNIT_SIZE, draw_area, zoom_level, camera_offset)
        # Vạch chia nhỏ (vuông góc trục X, dài 8px)
        pygame.draw.line(screen, (255,0,0), (tick_pos[0], tick_pos[1]-4), (tick_pos[0], tick_pos[1]+4), 1)
        # Số
        label = font.render(str(i * tick_interval), True, (255,0,0))
        screen.blit(label, (tick_pos[0]-8, tick_pos[1]+8))
    # Trục Y
    for i in range(1, axis_length // tick_interval + 1):
        tx, ty, tz = 0, i * tick_interval, 0
        tick_pos = project_cabinet(tx, ty, tz, UNIT_SIZE, draw_area, zoom_level, camera_offset)
        pygame.draw.line(screen, (0,255,0), (tick_pos[0]-4, tick_pos[1]), (tick_pos[0]+4, tick_pos[1]), 1)
        label = font.render(str(i * tick_interval), True, (0,255,0))
        screen.blit(label, (tick_pos[0]+6, tick_pos[1]-8))
    # Trục Z
    for i in range(1, axis_length // tick_interval + 1):
        tx, ty, tz = 0, 0, i * tick_interval
        tick_pos = project_cabinet(tx, ty, tz, UNIT_SIZE, draw_area, zoom_level, camera_offset)
        pygame.draw.line(screen, (0,0,255), (tick_pos[0]-4, tick_pos[1]), (tick_pos[0]+4, tick_pos[1]), 1)
        label = font.render(str(i * tick_interval), True, (0,0,255))
        screen.blit(label, (tick_pos[0]+6, tick_pos[1]-8))
    # Lùi label X vừa phải (lùi 40px so với mép phải draw_area)
    # Đẩy label X lên trên trục một chút để không bị cắt ngang
    label_x = (draw_area.right - 40, x_end[1] - 30)
    # Lùi label Y xuống dưới một chút để tránh mép trên
    label_y = (y_end[0] + 10, draw_area.top + 60)
    # Label Z giữ nguyên hoặc chỉnh lại cho cân đối
    label_z = (z_end[0] + 5, z_end[1])
    screen.blit(font.render('X', True, (255, 0, 0)), label_x)
    screen.blit(font.render('Y', True, (0, 255, 0)), label_y)
    screen.blit(font.render('Z', True, (0, 0, 255)), label_z)

def draw_2d_line_3d(x0, y0, x1, y1, style, screen, draw_area=None, UNIT_SIZE=3, zoom_level=1.0, camera_offset=(0, 0)):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    
    # Chuyển đổi tọa độ thực tế sang pixel pygame
    start = to_pygame_coords(x0, y0, draw_area, UNIT_SIZE, zoom_level, camera_offset)
    end = to_pygame_coords(x1, y1, draw_area, UNIT_SIZE, zoom_level, camera_offset)
    
    # Chuyển đổi tọa độ pixel về tọa độ lưới Bresenham (tương tự file_2D)
    center_x = draw_area.x + draw_area.width / 2 + camera_offset[0]
    center_y = draw_area.y + draw_area.height / 2 + camera_offset[1]
    grid_x0 = round((start[0] - center_x) / UNIT_SIZE)
    grid_y0 = round((center_y - start[1]) / UNIT_SIZE)
    grid_x1 = round((end[0] - center_x) / UNIT_SIZE)
    grid_y1 = round((center_y - end[1]) / UNIT_SIZE)
    
    # Sử dụng Bresenham để lấy danh sách pixel
    pixels = file_2D.Bresenham(grid_x0, grid_y0, grid_x1, grid_y1)
    pixel_index = 0
    for x, y in pixels:
        # Chuyển đổi lại sang tọa độ pixel thực tế để vẽ
        pixel_x = center_x + x * UNIT_SIZE * zoom_level
        pixel_y = center_y - y * UNIT_SIZE * zoom_level
        file_2D.putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
        pixel_index += 1

def draw_3d_line(screen, start, end, color=(0, 0, 0), dashed=False, UNIT_SIZE=3, draw_area=None, zoom_level=1.0, camera_offset=(0, 0)):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    pygame_start = project_cabinet(*start, UNIT_SIZE, draw_area, zoom_level, camera_offset)
    pygame_end = project_cabinet(*end, UNIT_SIZE, draw_area, zoom_level, camera_offset)
    # Tính toán tọa độ thực tế cho draw_2d_line_3d
    center_x = draw_area.x + draw_area.width / 2 + camera_offset[0]
    center_y = draw_area.y + draw_area.height / 2 + camera_offset[1]
    x0 = (pygame_start[0] - center_x) / (UNIT_SIZE * zoom_level)
    y0 = (center_y - pygame_start[1]) / (UNIT_SIZE * zoom_level)
    x1 = (pygame_end[0] - center_x) / (UNIT_SIZE * zoom_level)
    y1 = (center_y - pygame_end[1]) / (UNIT_SIZE * zoom_level)
    style = "Dut" if dashed else "Lien"
    # Gọi hàm draw_2d_line_3d
    draw_2d_line_3d(x0, y0, x1, y1, style, screen, draw_area, UNIT_SIZE, zoom_level, camera_offset)

def draw_dashed_line(screen, start, end, color=(0, 0, 0), dash_length=5, gap_length=3):
    try:
        from pygame import Vector2
        start_vec = Vector2(start)
        end_vec = Vector2(end)
        direction = (end_vec - start_vec).normalize()
        distance = (end_vec - start_vec).length()
        
        current_pos = 0
        while current_pos < distance:
            segment_start = start_vec + direction * current_pos
            segment_end = start_vec + direction * min(current_pos + dash_length, distance)
            file_2D.DoanThang(segment_start[0], segment_start[1], segment_end[0], segment_end[1], "Lien", screen)
            current_pos += dash_length + gap_length
    except ImportError:
        print("Lỗi: pygame.Vector2 không khả dụng. Hàm draw_dashed_line không được sử dụng trong vẽ 3D.")

def rotate_3d_point(x, y, z, angles):
    new_y = y * math.cos(angles[0]) - z * math.sin(angles[0])
    new_z = y * math.sin(angles[0]) + z * math.cos(angles[0])
    y, z = new_y, new_z
    
    new_x = x * math.cos(angles[1]) + z * math.sin(angles[1])
    new_z = -x * math.sin(angles[1]) + z * math.cos(angles[1])
    x, z = new_x, new_z
    
    new_x = x * math.cos(angles[2]) - y * math.sin(angles[2])
    new_y = x * math.sin(angles[2]) + y * math.cos(angles[2])
    x, y = new_x, new_y
    
    return (x, y, z)

def draw_3d_cuboid_rotated(screen, start_pos, length, width, height, angles=(0,0,0), show_labels=True, UNIT_SIZE=3, draw_area=None, zoom_level=1.0, camera_offset=(0, 0)):
    x, y, z = start_pos
    vertices = [
        (x, y, z),           # 0: A
        (x+length, y, z),    # 1: B
        (x+length, y+width, z), # 2: C
        (x, y+width, z),     # 3: D
        (x, y, z+height),    # 4: E
        (x+length, y, z+height), # 5: F
        (x+length, y+width, z+height), # 6: G
        (x, y+width, z+height)  # 7: H
    ]
    
    rotated_vertices = [rotate_3d_point(*v, angles) for v in vertices]
    
    edges = [
        (0, 1, True),   # AB - nét đứt
        (1, 2, False),  # BC - nét liền
        (2, 3, False),  # CD - nét liền
        (3, 0, True),   # DA - nét đứt
        (4, 5, False),  # EF - nét liền
        (5, 6, False),  # FG - nét liền
        (6, 7, False),  # GH - nét liền
        (7, 4, False),  # HE - nét liền
        (0, 4, True),   # AE - nét đứt
        (1, 5, False),  # BF - nét liền
        (2, 6, False),  # CG - nét liền
        (3, 7, False)   # DH - nét liền
    ]
    
    for start_idx, end_idx, is_hidden in edges:
        start_point = rotated_vertices[start_idx]
        end_point = rotated_vertices[end_idx]
        draw_3d_line(screen, start_point, end_point, (0, 0, 0), dashed=is_hidden, UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
    
    if show_labels:
        vertex_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        font = pygame.font.SysFont('arial', 15)
        for vertex, label in zip(rotated_vertices, vertex_labels):
            screen_pos = project_cabinet(*vertex, UNIT_SIZE, draw_area, zoom_level, camera_offset)
            label_surface = font.render(label, True, (0, 0, 255))
            screen.blit(label_surface, (screen_pos[0] + 5, screen_pos[1] - 15))
        
        display_coordinates(screen, rotated_vertices, vertex_labels, font, UNIT_SIZE, draw_area, zoom_level, camera_offset)

def draw_3d_sphere_rotated(screen, center, radius, angles=(0,0,0), show_labels=True, UNIT_SIZE=3, draw_area=None, zoom_level=1.0, camera_offset=(0, 0)):
    cx, cy, cz = center
    segments = 24
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
    for axis in range(3):
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            next_angle = 2 * math.pi * (i+1) / segments
            
            if axis == 0:
                x1, y1 = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
                z1 = cz
                x2, y2 = cx + radius * math.cos(next_angle), cy + radius * math.sin(next_angle)
                z2 = cz
            elif axis == 1:
                x1, z1 = cx + radius * math.cos(angle), cz + radius * math.sin(angle)
                y1 = cy
                x2, z2 = cx + radius * math.cos(next_angle), cz + radius * math.sin(next_angle)
                y2 = cy
            else:
                y1, z1 = cy + radius * math.cos(angle), cz + radius * math.sin(angle)
                x1 = cx
                y2, z2 = cy + radius * math.cos(next_angle), cz + radius * math.sin(next_angle)
                x2 = cx
            
            p1 = rotate_3d_point(x1, y1, z1, angles)
            p2 = rotate_3d_point(x2, y2, z2, angles)
            draw_3d_line(screen, p1, p2, colors[axis], UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
    
    if show_labels:
        rotated_center = rotate_3d_point(cx, cy, cz, angles)
        screen_center = project_cabinet(*rotated_center, UNIT_SIZE, draw_area, zoom_level, camera_offset)
        
        edge_x = cx + radius * math.cos(math.pi/4)
        edge_y = cy + radius * math.sin(math.pi/4)
        edge_point = rotate_3d_point(edge_x, edge_y, cz, angles)
        screen_edge = project_cabinet(*edge_point, UNIT_SIZE, draw_area, zoom_level, camera_offset)
        draw_3d_line(screen, rotated_center, edge_point, (0, 0, 0), False, UNIT_SIZE, draw_area, zoom_level, camera_offset)
        
        label_offset = 15
        label_pos = (screen_center[0] + label_offset, screen_center[1] + label_offset)
        font = pygame.font.SysFont('arial', 15)
        pygame.draw.circle(screen, (255, 0, 0), (int(screen_center[0]), int(screen_center[1])), 3)
        
        label_o = font.render('O', True, (0, 0, 0))
        screen.blit(label_o, label_pos)
        
        mid_point = ((screen_center[0] + screen_edge[0])/2 + 5, (screen_center[1] + screen_edge[1])/2 - 5)
        label_r = font.render(f'R={radius}', True, (0, 0, 0))
        screen.blit(label_r, mid_point)
        
        display_coordinates(screen, [rotated_center], ['O'], font, UNIT_SIZE, draw_area, zoom_level, camera_offset)

def draw_3d_streetlight(screen, base_pos, height, width, angles=(0,0,0), UNIT_SIZE=3, draw_area=None, zoom_level=1.0, camera_offset=(0, 0)):
    try:
        x, y, z = base_pos
        if height <= 0 or width <= 0:
            print("Lỗi: Chiều cao và chiều rộng phải lớn hơn 0")
            return

        base_size = width * 0.25
        base_height = height * 0.08
        draw_3d_cuboid_rotated(screen, (x, y, z), base_size, base_height, base_size, angles, show_labels=False, UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
        
        pole_width = width * 0.15
        pole_height = height * 0.8
        pole_x = x + (base_size - pole_width)/2
        pole_z = z + (base_size - pole_width)/2
        draw_3d_cuboid_rotated(screen, (pole_x, y + base_height, pole_z), pole_width, pole_height, pole_width, angles, show_labels=False, UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
        
        lamp_radius = width * 0.2
        lamp_pos = (pole_x + pole_width/2, y + base_height + pole_height, pole_z + pole_width/2)
        draw_3d_sphere_rotated(screen, lamp_pos, lamp_radius, angles, show_labels=False, UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
        
    except Exception as e:
        print(f"Lỗi khi vẽ Light Stick: {str(e)}")

def display_coordinates(screen, vertices, labels, font, UNIT_SIZE=3, draw_area=None, zoom_level=1.0, camera_offset=(0, 0)):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    offset_x = 20
    offset_y = 100
    title = font.render("Toa Do Diem", True, (0, 0, 0))
    screen.blit(title, (offset_x, offset_y - 30))
    
    for i, (vertex, label) in enumerate(zip(vertices, labels)):
        x, y, z = vertex
        # Áp dụng camera_offset cho tọa độ x và z
        offset_x_coord, offset_z_coord = camera_offset
        x_display = x + offset_x_coord / (UNIT_SIZE * zoom_level)
        z_display = z + offset_z_coord / (UNIT_SIZE * zoom_level)
        coord_text = f"{label}({x_display:.1f}, {y:.1f}, {z_display:.1f})"
        text_surface = font.render(coord_text, True, (0, 0, 0))
        screen.blit(text_surface, (offset_x, offset_y + i * 25))