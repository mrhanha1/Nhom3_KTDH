import pygame
import math
import datetime
import numpy as np

def putPixel(pos, style="Lien", pixel_index=0, screen=None, UNIT_SIZE=5):
    if style == "Dut":
        position_in_cycle = (pixel_index % 10) + 1
        if position_in_cycle not in [1, 2, 3, 4, 5, 6, 7]:
            return
    elif style == "Cham":
        position_in_cycle = (pixel_index % 10) + 1
        if position_in_cycle not in [1, 2, 3, 4, 5, 8]:
            return
    pygame.draw.rect(screen, (0, 0, 0), 
                    (pos[0] - UNIT_SIZE//2,
                     pos[1] - UNIT_SIZE//2,
                     UNIT_SIZE, UNIT_SIZE))

def Bresenham(x0, y0, x1, y1):
    pixels = []
    dx = x1 - x0
    dy = y1 - y0
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    
    if abs_dx >= abs_dy:
        err = 2 * abs_dy - abs_dx
        while True:
            pixels.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            if err >= 0:
                y0 += sy
                err += 2 * abs_dy - 2 * abs_dx
            else:
                err += 2 * abs_dy
            x0 += sx
    else:
        err = 2 * abs_dx - abs_dy
        while True:
            pixels.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            if err >= 0:
                x0 += sx
                err += 2 * abs_dx - 2 * abs_dy
            else:
                err += 2 * abs_dx
            y0 += sy
    return pixels

def DoanThang(x0, y0, x1, y1, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5):
    pixel_index = 0
    pixels = Bresenham(round(x0), round(y0), round(x1), round(y1))
    for x, y in pixels:
        pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
        putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
        pixel_index += 1

def MuiTen(x0, y0, x1, y1, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5):
    pixel_index = 0
    pixels = Bresenham(round(x0), round(y0), round(x1), round(y1))
    for x, y in pixels:
        pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
        putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
        pixel_index += 1
    
    dx = x1 - x0
    dy = y1 - y0
    length = (dx**2 + dy**2)**0.5
    if length == 0:
        return
    
    dx_norm = dx / length
    dy_norm = dy / length
    c = 3
    D = (x1 + (-dy_norm) * (c/2), y1 + dx_norm * (c/2))
    E = (x1 + dy_norm * (c/2), y1 + (-dx_norm) * (c/2))
    F = (x1 + dx_norm * (c * math.sqrt(3)/2), y1 + dy_norm * (c * math.sqrt(3)/2))
    
    pixels_de = Bresenham(round(D[0]), round(D[1]), round(E[0]), round(E[1]))
    pixels_ef = Bresenham(round(E[0]), round(E[1]), round(F[0]), round(F[1]))
    pixels_fd = Bresenham(round(F[0]), round(F[1]), round(D[0]), round(D[1]))
    
    for x, y in pixels_de + pixels_ef + pixels_fd:
        pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
        putPixel((pixel_x, pixel_y), style="Lien", screen=screen, UNIT_SIZE=UNIT_SIZE)

def HinhChuNhat(points, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5, fill_color=None):
    if fill_color is not None and screen is not None and draw_area is not None:
        poly_points = [revert_pos(p, draw_area, UNIT_SIZE) for p in points]
        pygame.draw.polygon(screen, fill_color, poly_points)
    pixel_index = 0
    for i in range(4):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % 4]
        pixels = Bresenham(round(x0), round(y0), round(x1), round(y1))
        for x, y in pixels:
            pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
            putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
            pixel_index += 1

def VeHinhVuong(xA, yA, a, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5, fill_color=None):
    points = [
        (xA, yA),
        (xA + a, yA),
        (xA + a, yA + a),
        (xA, yA + a)
    ]
    HinhChuNhat(points, style, screen, draw_area, UNIT_SIZE, fill_color=fill_color)

def HinhThangCan(x0, y0, top_base, bottom_base, height, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5, fill_color=None):
    offset = (bottom_base - top_base) / 2
    points = [
        (x0, y0),
        (x0 + top_base, y0),
        (x0 + offset + top_base, y0 - height),
        (x0 - offset, y0 - height)
    ]
    if fill_color is not None and screen is not None and draw_area is not None:
        poly_points = [revert_pos(p, draw_area, UNIT_SIZE) for p in points]
        pygame.draw.polygon(screen, fill_color, poly_points)
    pixel_index = 0
    for i in range(4):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % 4]
        pixels = Bresenham(round(x0), round(y0), round(x1), round(y1))
        for x, y in pixels:
            pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
            putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
            pixel_index += 1

def BresenhamCircle(R):
    pixels = []
    x = 0
    y = R
    P = 3 - 2 * R
    while x <= y:
        pixels.append((x, y))
        if P < 0:
            P = P + 4 * x + 6
        else:
            y -= 1
            P = P + 4 * (x - y) + 10
        x += 1
    return pixels

def VeCircle(center_x, center_y, R, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5, fill_color=None):
    if fill_color is not None and screen is not None and draw_area is not None:
        pixel_x, pixel_y = revert_pos((center_x, center_y), draw_area, UNIT_SIZE)
        pygame.draw.circle(screen, fill_color, (int(pixel_x), int(pixel_y)), int(R * UNIT_SIZE))
    R_pixels = R * UNIT_SIZE
    pixels = BresenhamCircle(round(R))
    pixel_index = 0
    for x, y in pixels:
        points = [
            (center_x + x, center_y + y),
            (center_x + y, center_y + x),
            (center_x + y, center_y - x),
            (center_x + x, center_y - y),
            (center_x - x, center_y - y),
            (center_x - y, center_y - x),
            (center_x - y, center_y + x),
            (center_x - x, center_y + y)
        ]
        for px, py in points:
            pixel_x, pixel_y = revert_pos((px, py), draw_area, UNIT_SIZE)
            putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
        pixel_index += 1

def MidpointEllipse(a, b):
    if a <= 0 or b <= 0:
        return []
    pixels = []
    x = 0
    y = b
    a2 = a * a
    b2 = b * b
    P = b2 - a2 * b + a2 // 4
    while b2 * x <= a2 * y:
        pixels.append((x, y))
        if P < 0:
            P += b2 * (2 * x + 3)
        else:
            P += b2 * (2 * x + 3) + a2 * (-2 * y + 2)
            y -= 1
        x += 1
    Q = b2 * (x + 0.5)**2 + a2 * (y - 1)**2 - a2 * b2
    while y >= 0:
        pixels.append((x, y))
        if Q < 0:
            Q += b2 * (2 * x + 2)
            x += 1
        else:
            Q += a2 * (-2 * y + 3)
        y -= 1
    return pixels

def VeEllipse(center_x, center_y, a, b, angle=0, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5, rotate_center=None, rotate_angle=0, reflect_mode=None, fill_color=None):
    # reflect_mode: None, 'Ox', 'Oy', 'O'
    if reflect_mode is not None:
        center_x, center_y, a, b, angle = ellipse_reflect(center_x, center_y, a, b, angle, reflect_mode)
    if rotate_angle != 0:
        if rotate_center is not None:
            cx, cy = center_x, center_y
            ox, oy = rotate_center
            rad = math.radians(rotate_angle)
            cos_r = math.cos(rad)
            sin_r = math.sin(rad)
            dx = cx - ox
            dy = cy - oy
            center_x = ox + dx * cos_r - dy * sin_r
            center_y = oy + dx * sin_r + dy * cos_r
            angle += rotate_angle
        else:
            angle += rotate_angle
    a_pixels = a * UNIT_SIZE
    b_pixels = b * UNIT_SIZE
    if fill_color is not None and screen is not None and draw_area is not None:
        # Tô màu elip bằng pygame.draw.ellipse (gần đúng)
        pixel_x, pixel_y = revert_pos((center_x, center_y), draw_area, UNIT_SIZE)
        rect = pygame.Rect(0, 0, int(a * 2 * UNIT_SIZE), int(b * 2 * UNIT_SIZE))
        rect.center = (int(pixel_x), int(pixel_y))
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, fill_color, (0, 0, rect.width, rect.height))
        if angle != 0:
            surface = pygame.transform.rotate(surface, -angle)
        screen.blit(surface, (rect.centerx - surface.get_width() // 2, rect.centery - surface.get_height() // 2))
    pixels = MidpointEllipse(round(a), round(b))
    pixel_index = 0
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    for x, y in pixels:
        points = [
            (x, y),
            (-x, y),
            (-x, -y),
            (x, -y)
        ]
        for px, py in points:
            px_rot = px * cos_a + py * sin_a
            py_rot = -px * sin_a + py * cos_a
            px_final = center_x + px_rot
            py_final = center_y + py_rot
            pixel_x, pixel_y = revert_pos((px_final, py_final), draw_area, UNIT_SIZE)
            putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
        pixel_index += 1

def VeNgoiSao(center_x, center_y, R, angle=0, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5):
    # Ensure angle is a float
    try:
        angle = float(angle)
    except Exception:
        angle = 0
    points = []
    for i in range(10):
        angle_deg = 90 - i * 36 + angle  # Add rotation
        angle_rad = math.radians(angle_deg)
        if i % 2 == 0:
            r = R
        else:
            r = R * 0.4
        x = center_x + r * math.cos(angle_rad)
        y = center_y + r * math.sin(angle_rad)
        points.append((x, y))
    poly_points = [revert_pos(p, draw_area, UNIT_SIZE) for p in points]
    pygame.draw.polygon(screen, (255, 215, 0), poly_points)
    pygame.draw.polygon(screen, (200, 150, 0), poly_points, 2)
    if style != "Lien":
        for i in range(10):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % 10]
            pixels = Bresenham(round(x0), round(y0), round(x1), round(y1))
            pixel_index = 0
            for x, y in pixels:
                pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
                putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
                pixel_index += 1

def get_trapezoid_points(x0, y0, top_base, bottom_base, height):
    offset = (bottom_base - top_base) / 2
    points = [
        (x0, y0),
        (x0 + top_base, y0),
        (x0 + offset + top_base, y0 - height),
        (x0 - offset, y0 - height)
    ]
    return points

def create_tank(center_x, center_y, size, style="Lien", group=None):
    shapes = []
    radius = size / 4
    spacing = radius * 3
    rect_height = radius
    group_origin = (center_x, center_y)

    # Khi append shape, thêm group_origin nếu có group
    def add_shape_with_origin(shape):
        if group:
            shape['group_origin'] = group_origin
        shapes.append(shape)
    # Track (Hình chữ nhật - bánh xích)
    track_points = [
        (center_x - spacing * 1.5, center_y + radius),
        (center_x + spacing * 1.5, center_y + radius),
        (center_x + spacing * 1.5, center_y - radius),
        (center_x - spacing * 1.5, center_y - radius)
    ]
    add_shape_with_origin({
        "type": "Hinh Chu Nhat",
        "data": track_points,
        "style": style,
        "group": group,
        "initial_data": track_points.copy()
    })
    # Bánh xe (4 hình tròn)
    for i in range(4):
        wheel_x = center_x + (i - 1.5) * spacing
        add_shape_with_origin({
            "type": "Hinh Tron",
            "data": (wheel_x, center_y, radius),
            "style": style,
            "group": group,
            "initial_data": (wheel_x, center_y, radius)
        })
    # Thân pháo (Hình thang cân)
    trap_x0 = center_x - spacing * 0.75
    trap_y0 = center_y + radius + rect_height * 2
    thap_phao_height = rect_height * 2
    thap_phao_top_base = spacing * 1.5
    thap_phao_bottom_base = spacing * 3
    thap_phao_points = get_trapezoid_points(trap_x0, trap_y0, thap_phao_top_base, thap_phao_bottom_base, thap_phao_height)
    add_shape_with_origin({
        "type": "HinhThang",
        "data": thap_phao_points,
        "style": style,
        "group": group,
        "initial_data": thap_phao_points.copy()
    })
    # Nòng pháo (Hình chữ nhật dài)
    points = thap_phao_points
    center_thap_x = sum([p[0] for p in points]) / 4
    center_thap_y = sum([p[1] for p in points]) / 4
    barrel_width = size / 8
    barrel_length = size * 1.1
    barrel_base_x = center_thap_x + size * 0.2
    barrel_center_y = center_thap_y
    barrel_tip_x = barrel_base_x + barrel_length
    barrel_points = [
        (barrel_base_x, barrel_center_y - barrel_width / 2),
        (barrel_base_x, barrel_center_y + barrel_width / 2),
        (barrel_tip_x, barrel_center_y + barrel_width / 2),
        (barrel_tip_x, barrel_center_y - barrel_width / 2)
    ]
    add_shape_with_origin({
        "type": "Hinh Chu Nhat",
        "data": barrel_points,
        "style": style,
        "group": group,
        "initial_data": barrel_points.copy()
    })
    # Hình tròn đỏ (nền ngôi sao - lá cờ)
    star_x = center_thap_x - radius * 0.5
    star_y = center_thap_y
    star_radius = radius * 0.7
    add_shape_with_origin({
        "type": "Hinh Tron",
        "data": (star_x, star_y, star_radius * 1.2),
        "style": style,
        "group": group,
        "initial_data": (star_x, star_y, star_radius * 1.2)
    })
    # Ngôi sao vàng
    add_shape_with_origin({
        "type": "Ngoi Sao",
        "data": (star_x, star_y, star_radius, 0),
        "style": style,
        "group": group,
        "initial_data": (star_x, star_y, star_radius, 0)
    })
    return shapes

def create_clock(center_x, center_y, radius, style="Lien", group=None):
    shapes = []
    # Mặt đồng hồ (Hình tròn)
    shapes.append({
        "type": "Hinh Tron",
        "data": (center_x, center_y, radius),
        "style": style,
        "group": group,
        "initial_data": (center_x, center_y, radius)
    })

    # Vạch giờ (12 đoạn thẳng)
    for hour in range(12):
        angle = math.radians(-hour * 30 + 90)
        start_x = center_x + (radius - 3) * math.cos(angle)
        start_y = center_y + (radius - 3) * math.sin(angle)
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        shapes.append({
            "type": "Doan Thang",
            "data": ((start_x, start_y), (end_x, end_y)),
            "style": style,
            "group": group,
            "initial_data": ((start_x, start_y), (end_x, end_y))
        })

    # Kim đồng hồ (3 đoạn thẳng) - sẽ được cập nhật trong update_scene
    now = datetime.datetime.now()
    hours, minutes, seconds = now.hour % 12, now.minute, now.second

    hour_angle = math.radians(-(hours * 30 + minutes * 0.5) + 90)
    hour_end_x = center_x + radius * 0.5 * math.cos(hour_angle)
    hour_end_y = center_y + radius * 0.5 * math.sin(hour_angle)
    shapes.append({
        "type": "Doan Thang",
        "data": ((center_x, center_y), (hour_end_x, hour_end_y)),
        "style": style,
        "group": group,
        "initial_data": ((center_x, center_y), (hour_end_x, hour_end_y)),
        "hand": "hour"
    })

    minute_angle = math.radians(-minutes * 6 + 90)
    minute_end_x = center_x + radius * 0.7 * math.cos(minute_angle)
    minute_end_y = center_y + radius * 0.7 * math.sin(minute_angle)
    shapes.append({
        "type": "Doan Thang",
        "data": ((center_x, center_y), (minute_end_x, minute_end_y)),
        "style": style,
        "group": group,
        "initial_data": ((center_x, center_y), (minute_end_x, minute_end_y)),
        "hand": "minute"
    })

    second_angle = math.radians(-seconds * 6 + 90)
    second_end_x = center_x + radius * 0.9 * math.cos(second_angle)
    second_end_y = center_y + radius * 0.9 * math.sin(second_angle)
    shapes.append({
        "type": "Doan Thang",
        "data": ((center_x, center_y), (second_end_x, second_end_y)),
        "style": style,
        "group": group,
        "initial_data": ((center_x, center_y), (second_end_x, second_end_y)),
        "hand": "second"
    })

    return shapes

def DongHo(center_x, center_y, radius, style="Lien", screen=None, draw_area=None, UNIT_SIZE=5, show_coords=False, font=None):
    pixel_x, pixel_y = revert_pos((center_x, center_y), draw_area, UNIT_SIZE)
    pygame.draw.circle(screen, (180, 240, 240), (int(pixel_x), int(pixel_y)), int(radius * UNIT_SIZE))
    now = datetime.datetime.now()
    hours, minutes, seconds = now.hour % 12, now.minute, now.second
    VeCircle(center_x, center_y, radius, style, screen, draw_area, UNIT_SIZE)
    for hour in range(12):
        angle = math.radians(-hour * 30 + 90)
        start_x = center_x + (radius - 3) * math.cos(angle)
        start_y = center_y + (radius - 3) * math.sin(angle)
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        pixels = Bresenham(round(start_x), round(start_y), round(end_x), round(end_y))
        pixel_index = 0
        for x, y in pixels:
            pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
            putPixel((pixel_x, pixel_y), style=style, pixel_index=pixel_index, screen=screen, UNIT_SIZE=UNIT_SIZE)
            pixel_index += 1
    hour_angle = math.radians(-(hours * 30 + minutes * 0.5) + 90)
    hour_end_x = center_x + radius * 0.5 * math.cos(hour_angle)
    hour_end_y = center_y + radius * 0.5 * math.sin(hour_angle)
    pixels = Bresenham(round(center_x), round(center_y), round(hour_end_x), round(hour_end_y))
    pixel_index = 0
    for x, y in pixels:
        pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
        pygame.draw.rect(screen, (0, 102, 204), (pixel_x - UNIT_SIZE//2, pixel_y - UNIT_SIZE//2, UNIT_SIZE, UNIT_SIZE))
        pixel_index += 1
    minute_angle = math.radians(-minutes * 6 + 90)
    minute_end_x = center_x + radius * 0.7 * math.cos(minute_angle)
    minute_end_y = center_y + radius * 0.7 * math.sin(minute_angle)
    pixels = Bresenham(round(center_x), round(center_y), round(minute_end_x), round(minute_end_y))
    pixel_index = 0
    for x, y in pixels:
        pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
        pygame.draw.rect(screen, (0, 180, 0), (pixel_x - UNIT_SIZE//2, pixel_y - UNIT_SIZE//2, UNIT_SIZE, UNIT_SIZE))
        pixel_index += 1
    second_angle = math.radians(-seconds * 6 + 90)
    second_end_x = center_x + radius * 0.9 * math.cos(second_angle)
    second_end_y = center_y + radius * 0.9 * math.sin(second_angle)
    pixels = Bresenham(round(center_x), round(center_y), round(second_end_x), round(second_end_y))
    pixel_index = 0
    for x, y in pixels:
        pixel_x, pixel_y = revert_pos((x, y), draw_area, UNIT_SIZE)
        pygame.draw.rect(screen, (220, 0, 0), (pixel_x - UNIT_SIZE//2, pixel_y - UNIT_SIZE//2, UNIT_SIZE, UNIT_SIZE))
        pixel_index += 1
    pixel_x, pixel_y = revert_pos((center_x, center_y), draw_area, UNIT_SIZE)
    pygame.draw.circle(screen, (0, 0, 0), (int(pixel_x), int(pixel_y)), int(UNIT_SIZE * 0.7))

    hands = {
        "hour_hand": (hour_end_x, hour_end_y),
        "minute_hand": (minute_end_x, minute_end_y),
        "second_hand": (second_end_x, second_end_y)
    }
    if show_coords and font is not None:
        info = [
            f"Tam: ({center_x:.0f}, {center_y:.0f})",
            f"Hour: ({hour_end_x:.0f}, {hour_end_y:.0f})",
            f"Minute: ({minute_end_x:.0f}, {minute_end_y:.0f})",
            f"Second: ({second_end_x:.0f}, {second_end_y:.0f})"
        ]
        for i, text in enumerate(info):
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, (10, 10 + i * 20))
    return hands

def draw_grid(screen, grid_size, draw_area):
    for x in range(draw_area.x, draw_area.x + draw_area.width, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (x, draw_area.y), (x, draw_area.y + draw_area.height))
    for y in range(draw_area.y, draw_area.y + draw_area.height, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (draw_area.x, y), (draw_area.x + draw_area.width, y))

def draw_axes_2d(screen, draw_area=None):
    if draw_area is None:
        draw_area = pygame.Rect(0, -50, 800, 800)
    center_x, center_y = draw_area.x + draw_area.width // 2, draw_area.y + draw_area.height // 2
    pygame.draw.line(screen, (0, 0, 0), (draw_area.x, center_y), (draw_area.x + draw_area.width, center_y))
    pygame.draw.line(screen, (0, 0, 0), (center_x, draw_area.y), (center_x, draw_area.y + draw_area.height))
    UNIT_MARK_LEN = 8
    UNIT_SIZE = 5
    font = pygame.font.SysFont('arial', 12)
    for i, x in enumerate(range(draw_area.x, draw_area.x + draw_area.width + 1, UNIT_SIZE)):
        pygame.draw.line(screen, (0, 0, 0), (x, center_y - UNIT_MARK_LEN//2), (x, center_y + UNIT_MARK_LEN//2), 1)
        if i % 5 == 0:
            value = (x - center_x) // UNIT_SIZE
            label = str(int(value))
            text_surface = font.render(label, True, (0, 0, 0))
            screen.blit(text_surface, (x - text_surface.get_width() // 2, center_y + UNIT_MARK_LEN//2 + 2))
    for i, y in enumerate(range(draw_area.y, draw_area.y + draw_area.height + 1, UNIT_SIZE)):
        pygame.draw.line(screen, (0, 0, 0), (center_x - UNIT_MARK_LEN//2, y), (center_x + UNIT_MARK_LEN//2, y), 1)
        if i % 5 == 0:
            value = (center_y - y) // UNIT_SIZE
            label = str(int(value))
            text_surface = font.render(label, True, (0, 0, 0))
            screen.blit(text_surface, (center_x + UNIT_MARK_LEN//2 + 2, y - text_surface.get_height() // 2))

def convert_pos(pos, draw_area, UNIT_SIZE):
    center_x = draw_area.x + draw_area.width / 2
    center_y = draw_area.y + draw_area.height / 2
    x, y = pos
    rel_x = (x - center_x) / UNIT_SIZE
    rel_y = (center_y - y) / UNIT_SIZE
    return (rel_x, rel_y)

def revert_pos(pos, draw_area, UNIT_SIZE):
    if not hasattr(draw_area, 'x'):
        class DummyRect:
            x = 0
            y = -50
            width = 800
            height = 800
        draw_area = DummyRect()
    center_x = draw_area.x + draw_area.width / 2
    center_y = draw_area.y + draw_area.height / 2
    rel_x, rel_y = pos
    x = rel_x * UNIT_SIZE + center_x
    y = center_y - rel_y * UNIT_SIZE
    return (x, y)

# --- Đối xứng elip ---
def ellipse_reflect(center_x, center_y, a, b, angle, mode):
    # mode: 'Ox', 'Oy', 'O'
    if mode == 'Ox':
        new_cx = center_x
        new_cy = -center_y
        new_angle = -angle
    elif mode == 'Oy':
        new_cx = -center_x
        new_cy = center_y
        new_angle = 180 - angle
    elif mode == 'O':
        new_cx = -center_x
        new_cy = -center_y
        new_angle = 180 + angle
    else:
        new_cx, new_cy, new_angle = center_x, center_y, angle
    # Đảm bảo góc nằm trong [0, 360)
    new_angle = new_angle % 360
    return new_cx, new_cy, a, b, new_angle

def update_clock_hands_in_shapes(shapes):
    import datetime
    import math
    # Gom các shape theo group clock
    clock_groups = {}
    for shape in shapes:
        if "group" in shape and shape["group"].startswith("clock_"):
            group = shape["group"]
            if group not in clock_groups:
                clock_groups[group] = []
            clock_groups[group].append(shape)
    # Cập nhật vị trí các kim cho từng đồng hồ
    for group, group_shapes in clock_groups.items():
        # Tìm mặt đồng hồ để lấy bán kính
        clock_face = next((s for s in group_shapes if s["type"] == "Hinh Tron"), None)
        if clock_face:
            center_x, center_y, radius = clock_face["data"]
            now = datetime.datetime.now()
            hours, minutes, seconds = now.hour % 12, now.minute, now.second
            for shape in group_shapes:
                if "hand" in shape:
                    if shape["hand"] == "hour":
                        angle = math.radians(-(hours * 30 + minutes * 0.5) + 90)
                        length = radius * 0.5
                    elif shape["hand"] == "minute":
                        angle = math.radians(-minutes * 6 + 90)
                        length = radius * 0.7
                    elif shape["hand"] == "second":
                        angle = math.radians(-seconds * 6 + 90)
                        length = radius * 0.9
                    end_x = center_x + length * math.cos(angle)
                    end_y = center_y + length * math.sin(angle)
                    shape["data"] = ((center_x, center_y), (end_x, end_y))

def veXeTang(group, screen=None, draw_area=None, UNIT_SIZE=5, fill_color_map=None):
    """
    Vẽ group shape xe tăng. fill_color_map: dict {index: fill_color} hoặc None.
    """
    for idx, shape in enumerate(group):
        shape_type = shape["type"]
        style = shape.get("style", "Lien")
        fill_color = None
        if fill_color_map and idx in fill_color_map:
            fill_color = fill_color_map[idx]
        if shape_type == "Hinh Chu Nhat":
            HinhChuNhat(shape["data"], style, screen, draw_area, UNIT_SIZE, fill_color=fill_color)
        elif shape_type == "Hinh Tron":
            data = shape["data"]
            # Hình tròn xe tăng: (x, y, r) hoặc (x, y, r, ...) (có thể dư tham số)
            x, y, r = data[:3]
            VeCircle(x, y, r, style, screen, draw_area, UNIT_SIZE, fill_color=fill_color)
        elif shape_type == "HinhThang":
            # Sử dụng trực tiếp 4 điểm từ "data" thay vì tái tính toán
            HinhChuNhat(shape["data"], style, screen, draw_area, UNIT_SIZE, fill_color=fill_color)
        elif shape_type == "Ngoi Sao":
            data = shape["data"]
            # Ngôi sao: (x, y, r, angle) hoặc (x, y, r)
            if len(data) == 4:
                x, y, r, angle = data
            else:
                x, y, r = data
                angle = 0
            VeNgoiSao(x, y, r, angle, style, screen, draw_area, UNIT_SIZE)

def veDongHo(group, screen=None, draw_area=None, UNIT_SIZE=5, fill_color_map=None):
    """
    Vẽ group shape đồng hồ. fill_color_map: dict {index: fill_color} hoặc None.
    """
    for idx, shape in enumerate(group):
        shape_type = shape["type"]
        style = shape.get("style", "Lien")
        fill_color = None
        if fill_color_map and idx in fill_color_map:
            fill_color = fill_color_map[idx]
        if shape_type == "Hinh Tron":
            x, y, r = shape["data"]
            VeCircle(x, y, r, style, screen, draw_area, UNIT_SIZE, fill_color=fill_color)
        elif shape_type == "Doan Thang":
            (x0, y0), (x1, y1) = shape["data"]
            DoanThang(x0, y0, x1, y1, style, screen, draw_area, UNIT_SIZE)