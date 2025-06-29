import pygame
import math
import copy
import numpy as np
import file_2D
import file_3D
import MTBD

"""---------------------------------PHẦN SETTING---------------------------------"""
W, H = 1280, 720
UNIT_SIZE = 5
GRAY = (200, 200, 200)
MAX_RADIUS = 200

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

draw_area = pygame.Rect(0, -50, 800, 800)
current_mode = 'Che do 2D'
selected_draw_mode = None
selected_line_style = "Cham"
selected_transform = None
font = pygame.font.SysFont('arial', 20)
rotation_circle_active = False
rotation_angle = 0
rotation_angles = [0, 0, 0]
zoom_level = 1.0
camera_offset = [0, 0]
selected_shape_indices = []
ui_rect = pygame.Rect(810, 0, 425, 720)
ui_scroll_offset = 0
ui_content_height = 960
shape_list_max_rows = 4
tank2_start_x = -50
ui_regions = {
    "input_area_rect": None,
    "shape_list_rect_adj": None,
    "info_rect_adj": None
}
animation_active = False
animation_step = 0

"""---------------------------------PHẦN UI---------------------------------"""
buttons = [
    {"rect": pygame.Rect(820, 20, 100, 35), "text": "Che do 2D", "section": "mode"},
    {"rect": pygame.Rect(930, 20, 100, 35), "text": "Che do 3D", "section": "mode"},
    {"rect": pygame.Rect(820, 80, 95, 30), "text": "Doan Thang", "section": "2d"},
    {"rect": pygame.Rect(925, 80, 95, 30), "text": "Mui Ten", "section": "2d"},
    {"rect": pygame.Rect(1030, 80, 95, 30), "text": "Hinh Tron", "section": "2d"},
    {"rect": pygame.Rect(820, 115, 95, 30), "text": "Hinh Elip", "section": "2d"},
    {"rect": pygame.Rect(925, 115, 95, 30), "text": "Hinh Chu Nhat", "section": "2d"},
    {"rect": pygame.Rect(1030, 115, 95, 30), "text": "Xe Tang", "section": "2d"},
    {"rect": pygame.Rect(820, 150, 95, 30), "text": "Dong Ho", "section": "2d"},
    {"rect": pygame.Rect(925, 150, 95, 30), "text": "HinhThang", "section": "2d"},
    {"rect": pygame.Rect(1030, 150, 95, 30), "text": "HinhVuong", "section": "2d"},
    {"rect": pygame.Rect(820, 240, 95, 30), "text": "Hinh hop CN", "section": "3d"},
    {"rect": pygame.Rect(925, 240, 95, 30), "text": "Hinh Cau", "section": "3d"},
    {"rect": pygame.Rect(1030, 240, 95, 30), "text": "Den J97", "section": "3d"},
    {"rect": pygame.Rect(820, 295, 95, 30), "text": "Net Lien", "section": "line"},
    {"rect": pygame.Rect(925, 295, 95, 30), "text": "Net Dut", "section": "line"},
    {"rect": pygame.Rect(1030, 295, 95, 30), "text": "Net Cham", "section": "line"},
    {"rect": pygame.Rect(820, 390, 95, 30), "text": "Tinh Tien", "section": "transform"},
    {"rect": pygame.Rect(925, 390, 95, 30), "text": "Doi Xung Ox", "section": "transform"},
    {"rect": pygame.Rect(1030, 390, 95, 30), "text": "Doi Xung Oy", "section": "transform"},
    {"rect": pygame.Rect(820, 425, 95, 30), "text": "Doi Xung O", "section": "transform"},
    {"rect": pygame.Rect(925, 425, 95, 30), "text": "Ty Le", "section": "transform"},
    {"rect": pygame.Rect(1030, 425, 95, 30), "text": "Quay O", "section": "transform"},
    {"rect": pygame.Rect(820, 460, 95, 30), "text": "Quay Tam", "section": "transform"},
    {"rect": pygame.Rect(820, 520, 95, 35), "text": "Xoa Du Lieu", "section": "control"},
    {"rect": pygame.Rect(925, 520, 95, 35), "text": "Ap Dung", "section": "control"},
    {"rect": pygame.Rect(1030, 520, 95, 35), "text": "Reset", "section": "control"},
    {"rect": pygame.Rect(820, 580, 95, 35), "text": "Anim Xe Tang", "section": "animation"},
]

input_boxes = [
    {"label": "X0:", "value": "", "active": False},
    {"label": "Y0:", "value": "", "active": False},
    {"label": "X1:", "value": "", "active": False},
    {"label": "Y1:", "value": "", "active": False},
    {"label": "X:", "value": "", "active": False},
    {"label": "Y:", "value": "", "active": False},
    {"label": "R:", "value": "", "active": False},
    {"label": "S:", "value": "", "active": False},
    {"label": "a:", "value": "", "active": False},
    {"label": "b:", "value":"", "active": False},
    {"label": "X3D:", "value": "", "active": False},
    {"label": "Y3D:", "value": "", "active": False},
    {"label": "Z3D:", "value": "", "active": False},
    {"label": "L:", "value": "", "active": False},
    {"label": "W:", "value": "", "active": False},
    {"label": "H:", "value": "", "active": False},
    {"label": "R3D:", "value": "", "active": False},
    {"label": "dx:", "value": "", "active": False},
    {"label": "dy:", "value": "", "active": False},
    {"label": "sx:", "value": "", "active": False},
    {"label": "sy:", "value": "", "active": False},
    {"label": "angle:", "value": "", "active": False},
    {"label": "Top:", "value": "", "active": False},
    {"label": "Bot:", "value": "", "active": False},
]

def get_square_points(x0, y0, x1, y1):
    side = min(abs(x1 - x0), abs(y1 - y0))
    xA = x0
    yA = y0
    if x1 < x0:
        xA -= side
    if y1 < y0:
        yA -= side
    return [
        (xA, yA),
        (xA + side, yA),
        (xA + side, yA + side),
        (xA, yA + side)
    ]

def get_trapezoid_points(x0, y0, x1, y1):
    width = abs(x1 - x0)
    height = abs(y1 - y0)
    bottom_base = width
    top_base = width * 0.6
    offset = (bottom_base - top_base) / 2
    if y1 >= y0:
        return [
            (x0, y0),
            (x0 + bottom_base, y0),
            (x0 + offset + top_base, y0 + height),
            (x0 + offset, y0 + height)
        ]
    else:
        return [
            (x0 + offset, y0),
            (x0 + offset + top_base, y0),
            (x0 + bottom_base, y0 - height),
            (x0, y0 - height)
        ]

def calculate_group_center(selected_shapes):
    if selected_shapes and all('group' in s for s in selected_shapes):
        group_name = selected_shapes[0].get('group', None)
        if group_name and str(group_name).startswith('tank'):
            for s in selected_shapes:
                if 'tank_center' in s:
                    return s["tank_center"]
    total_weight = 0
    sum_x = 0
    sum_y = 0
    for shape in selected_shapes:
        t = shape["type"]
        data = shape["data"]
        if t in ["Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
            points = data
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            n = len(points)
            area = 0
            cx = 0
            cy = 0
            for i in range(n):
                j = (i + 1) % n
                cross = xs[i]*ys[j] - xs[j]*ys[i]
                area += cross
                cx += (xs[i] + xs[j]) * cross
                cy += (ys[i] + ys[j]) * cross
            area = abs(area) / 2
            if area != 0:
                cx = cx / (6 * area)
                cy = cy / (6 * area)
            else:
                cx = sum(xs) / n
                cy = sum(ys) / n
            weight = area
        elif t in ["Hinh Tron", "Ngoi Sao"]:
            if len(data) == 4:
                cx, cy, r, *_ = data
            else:
                cx, cy, r = data
            weight = math.pi * r * r
        elif t == "Hinh Elip":
            cx, cy, a, b, *_ = data
            weight = math.pi * a * b
        elif t in ["Doan Thang", "Mui Ten"]:
            (x0, y0), (x1, y1) = data
            cx = (x0 + x1) / 2
            cy = (y0 + y1) / 2
            weight = math.hypot(x1 - x0, y1 - y0)
        elif t in ["Xe Tang", "Dong Ho"]:
            cx, cy = data[:2]
            weight = 1
        else:
            cx, cy = data[:2]
            weight = 1
        sum_x += cx * weight
        sum_y += cy * weight
        total_weight += weight
    if total_weight > 0:
        return sum_x / total_weight, sum_y / total_weight
    return 0, 0

def format_shape_data(shape, detailed=False):
    shape_type = shape["type"]
    if detailed:
        data = shape["data"]
        if shape_type in ["Doan Thang", "Mui Ten"]:
            (x0, y0), (x1, y1) = data
            return f"{shape_type}: P0({x0:.0f}, {y0:.0f}), P1({x1:.0f}, {y1:.0f})"
        elif shape_type in ["Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
            points = data
            return f"{shape_type}: P0({points[0][0]:.0f}, {points[0][1]:.0f}), P2({points[2][0]:.0f}, {points[2][1]:.0f})"
        elif shape_type == "Hinh Tron":
            x, y, r = data
            return f"{shape_type}: O({x:.0f}, {y:.0f}), R={r:.0f}"
        elif shape_type == "Hinh Elip":
            x, y, a, b, angle = data
            return f"{shape_type}: O({x:.0f}, {y:.0f}), a={a:.0f}, b={b:.0f}, angle={angle:.0f}"
        elif shape_type == "Xe Tang":
            x, y, s = data
            return f"{shape_type}: O({x:.0f}, {y:.0f}), S={s:.0f}"
        elif shape_type == "Dong Ho":
            x, y, r = data
            return f"{shape_type}: O({x:.0f}, {y:.0f}), R={r:.0f}"
        elif shape_type == "Hinh hop CN":
            x, y, z, l, w, h = data
            return f"{shape_type}: A({x:.0f}, {y:.0f}, {z:.0f}), L={l:.0f}, W={w:.0f}, H={h:.0f}"
        elif shape_type == "Hinh Cau":
            x, y, z, r = data
            return f"{shape_type}: O({x:.0f}, {y:.0f}, {z:.0f}), R={r:.0f}"
        elif shape_type == "Den J97":
            x, y, z, l, w = data
            return f"{shape_type}: ({x:.0f}, {y:.0f}, {z:.0f}), L={l:.0f}, W={w:.0f}"
        return shape_type
    return shape_type

def get_active_labels():
    active_labels = []
    if selected_draw_mode in ["Doan Thang", "Mui Ten", "Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
        active_labels = ["X0:", "Y0:", "X1:", "Y1:"]
    elif selected_draw_mode in ["Hinh Tron", "Dong Ho"]:
        active_labels = ["X:", "Y:", "R:"]
    elif selected_draw_mode == "Hinh Elip":
        active_labels = ["X:", "Y:", "a:", "b:"]
    elif selected_draw_mode == "Xe Tang":
        active_labels = ["X:", "Y:", "S:"]
    elif selected_draw_mode in ["Hinh hop CN", "Hinh Cau", "Den J97"]:
        active_labels = ["X3D:", "Y3D:", "Z3D:"]
        if selected_draw_mode == "Hinh hop CN":
            active_labels.extend(["L:", "W:", "H:"])
        elif selected_draw_mode == "Hinh Cau":
            active_labels.append("R3D:")
        elif selected_draw_mode == "Den J97":
            active_labels.extend(["L:", "W:"])
    elif selected_transform == "Tinh Tien":
        active_labels = ["dx:", "dy:"]
    elif selected_transform == "Ty Le":
        active_labels = ["sx:", "sy:"]
    elif selected_transform in ["Quay O", "Quay Tam"]:
        active_labels = ["angle:"]
    return active_labels

def get_input_box_positions(input_area_rect):
    active_labels = get_active_labels()
    input_box_positions = []
    for i, label in enumerate(active_labels):
        col = i % 4
        row = i // 4
        box_x = input_area_rect.x + 5 + col * 90
        box_y = input_area_rect.y + 10 + row * 35
        box_rect = pygame.Rect(box_x, box_y, 80, 25)
        input_box_positions.append((label, box_rect))
    return input_box_positions

def draw_UI(screen, font):
    global ui_regions
    pygame.draw.rect(screen, (240, 240, 245), ui_rect, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), ui_rect, 1, border_radius=8)

    title_font = pygame.font.SysFont('arial', 20, bold=True)
    section_font = pygame.font.SysFont('arial', 16, True)

    section_x = 830
    section_w = 370
    section_pad_x = 10
    section_pad_y = 8
    btn_w = 95
    btn_h = 30
    btn_gap = 10

    current_y = 20 - ui_scroll_offset

    pygame.draw.line(screen, (70, 130, 180), (section_x, current_y), (section_x + section_w, current_y), 2)
    section_text = section_font.render("Mode", True, (70, 130, 180))
    screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
    current_y += 28
    x_btn = section_x + section_pad_x
    for button in buttons:
        if button["section"] == "mode":
            button_rect = pygame.Rect(x_btn, current_y, btn_w, btn_h)
            is_selected = button["text"] == current_mode
            color = (100, 149, 237) if is_selected else (230, 230, 230)
            text_color = (255, 255, 255) if is_selected else (50, 50, 50)
            pygame.draw.rect(screen, color, button_rect, border_radius=6)
            pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
            text = font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            button["rect"] = button_rect.copy()
            x_btn += btn_w + btn_gap
    current_y += btn_h + 10

    if current_mode == 'Che do 2D':
        pygame.draw.line(screen, (34, 139, 34), (section_x, current_y), (section_x + section_w, current_y), 2)
        section_text = section_font.render("2D Draw", True, (34, 139, 34))
        screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
        current_y += 28
        x_btn = section_x + section_pad_x
        row_y = current_y
        count = 0
        for button in buttons:
            if button["section"] == "2d":
                button_rect = pygame.Rect(x_btn, row_y, btn_w, btn_h)
                is_selected = button["text"] == selected_draw_mode
                color = (100, 200, 100) if is_selected else (230, 230, 230)
                text_color = (255, 255, 255) if is_selected else (50, 50, 50)
                pygame.draw.rect(screen, color, button_rect, border_radius=6)
                pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
                text = font.render(button["text"], True, text_color)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)
                button["rect"] = button_rect.copy()
                x_btn += btn_w + btn_gap
                count += 1
                if count % 3 == 0:
                    x_btn = section_x + section_pad_x
                    row_y += btn_h + btn_gap
        current_y = row_y + btn_h + 10

    elif current_mode == 'Che do 3D':
        pygame.draw.line(screen, (220, 20, 60), (section_x, current_y), (section_x + section_w, current_y), 2)
        section_text = section_font.render("3D Draw", True, (220, 20, 60))
        screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
        current_y += 28
        x_btn = section_x + section_pad_x
        row_y = current_y
        count = 0
        for button in buttons:
            if button["section"] == "3d":
                button_rect = pygame.Rect(x_btn, row_y, btn_w, btn_h)
                is_selected = button["text"] == selected_draw_mode
                color = (220, 20, 60) if is_selected else (230, 230, 230)
                text_color = (255, 255, 255) if is_selected else (50, 50, 50)
                pygame.draw.rect(screen, color, button_rect, border_radius=6)
                pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
                text = font.render(button["text"], True, text_color)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)
                button["rect"] = button_rect.copy()
                x_btn += btn_w + btn_gap
                count += 1
                if count % 3 == 0:
                    x_btn = section_x + section_pad_x
                    row_y += btn_h + btn_gap
        current_y = row_y + btn_h + 10

    if current_mode == 'Che do 2D':
        pygame.draw.line(screen, (255, 140, 0), (section_x, current_y), (section_x + section_w, current_y), 2)
        section_text = section_font.render("Line Style", True, (255, 140, 0))
        screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
        current_y += 28
        x_btn = section_x + section_pad_x
        for button in buttons:
            if button["section"] == "line":
                button_rect = pygame.Rect(x_btn, current_y, btn_w, btn_h)
                is_selected = selected_line_style == button["text"].split()[1]
                color = (255, 140, 0) if is_selected else (230, 230, 230)
                text_color = (255, 255, 255) if is_selected else (50, 50, 50)
                pygame.draw.rect(screen, color, button_rect, border_radius=6)
                pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
                text = font.render(button["text"], True, text_color)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)
                button["rect"] = button_rect.copy()
                x_btn += btn_w + btn_gap
        current_y += btn_h + 10

    pygame.draw.line(screen, (138, 43, 226), (section_x, current_y), (section_x + section_w, current_y), 2)
    section_text = section_font.render("Transform", True, (138, 43, 226))
    screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
    current_y += 28
    x_btn = section_x + section_pad_x
    row_y = current_y
    count = 0
    for button in buttons:
        if button["section"] == "transform":
            button_rect = pygame.Rect(x_btn, row_y, btn_w, btn_h)
            is_selected = selected_transform == button["text"]
            color = (138, 43, 226) if is_selected else (230, 230, 230)
            text_color = (255, 255, 255) if is_selected else (50, 50, 50)
            pygame.draw.rect(screen, color, button_rect, border_radius=6)
            pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
            text = font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            button["rect"] = button_rect.copy()
            x_btn += btn_w + btn_gap
            count += 1
            if count % 3 == 0:
                x_btn = section_x + section_pad_x
                row_y += btn_h + btn_gap
    current_y = row_y + btn_h + 5

    pygame.draw.line(screen, (105, 105, 105), (section_x, current_y), (section_x + section_w, current_y), 2)
    section_text = section_font.render("Input", True, (105, 105, 105))
    screen.blit(section_text, (section_x + section_pad_x, current_y + 5))
    current_y += 28
    input_area_rect = pygame.Rect(section_x + section_pad_x, current_y, section_w - 2 * section_pad_x, 90)
    ui_regions["input_area_rect"] = input_area_rect.copy()
    pygame.draw.rect(screen, (245, 245, 250), input_area_rect, border_radius=6)
    pygame.draw.rect(screen, (200, 200, 200), input_area_rect, 1, border_radius=6)
    input_box_positions = get_input_box_positions(input_area_rect)
    for label, box_rect in input_box_positions:
        box = next((b for b in input_boxes if b["label"] == label), None)
        if not box:
            continue
        box_color = (200, 255, 200) if box["active"] else (255, 255, 255)
        border_color = (100, 200, 100) if box["active"] else (200, 200, 200)
        pygame.draw.rect(screen, box_color, box_rect, border_radius=4)
        pygame.draw.rect(screen, border_color, box_rect, 1, border_radius=4)
        display_text = box["value"] if box["value"] else label.strip(":")
        text_color = (100, 100, 100) if not box["value"] else (30, 30, 30)
        value_surface = font.render(display_text, True, text_color)
        max_width = box_rect.width - 10
        if value_surface.get_width() > max_width:
            while font.size(display_text + "...")[0] > max_width and len(display_text) > 1:
                display_text = display_text[:-1]
            display_text += "..."
            value_surface = font.render(display_text, True, text_color)
        screen.blit(value_surface, (box_rect.x + 5, box_rect.y + 3))

    rotation_circle_radius = 40
    if selected_transform in ["Quay O", "Quay Tam"]:
        circle_center = (input_area_rect.x + input_area_rect.width // 2, input_area_rect.y + input_area_rect.height // 2)
        pygame.draw.circle(screen, (245, 245, 245), circle_center, rotation_circle_radius + 8)
        pygame.draw.circle(screen, (180, 180, 180), circle_center, rotation_circle_radius + 2)
        angle_rad = math.radians(rotation_angle)
        pointer_x = circle_center[0] + (rotation_circle_radius - 5) * math.cos(angle_rad)
        pointer_y = circle_center[1] - (rotation_circle_radius - 5) * math.sin(angle_rad)
        pygame.draw.line(screen, (255, 69, 0), circle_center, (pointer_x, pointer_y), 3)
        pygame.draw.circle(screen, (255, 69, 0), circle_center, 4)

    current_y += input_area_rect.height + section_pad_y

    pygame.draw.line(screen, (178, 34, 34), (section_x, current_y), (section_x + section_w, current_y), 2)
    section_text = section_font.render("Control", True, (178, 34, 34))
    screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
    current_y += 28
    x_btn = section_x + section_pad_x
    for button in buttons:
        if button["section"] == "control":
            button_rect = pygame.Rect(x_btn, current_y, btn_w, btn_h)
            color = (178, 34, 34) if False else (230, 230, 230)
            text_color = (255, 255, 255) if False else (50, 50, 50)
            pygame.draw.rect(screen, color, button_rect, border_radius=6)
            pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
            text = font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            button["rect"] = button_rect.copy()
            x_btn += btn_w + btn_gap
    current_y += btn_h + section_pad_y

    pygame.draw.line(screen, (70, 130, 180), (section_x, current_y), (section_x + section_w, current_y), 2)
    section_text = section_font.render("Animation", True, (70, 130, 180))
    screen.blit(section_text, (section_x + section_pad_x, current_y + 2))
    current_y += 28
    x_btn = section_x + section_pad_x
    for button in buttons:
        if button["section"] == "animation":
            button_rect = pygame.Rect(x_btn, current_y, btn_w, btn_h)
            color = (70, 130, 180) if False else (230, 230, 230)
            text_color = (255, 255, 255) if False else (50, 50, 50)
            pygame.draw.rect(screen, color, button_rect, border_radius=6)
            pygame.draw.rect(screen, (180, 180, 180), button_rect, 1, border_radius=6)
            text = font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            button["rect"] = button_rect.copy()
            x_btn += btn_w + btn_gap
    current_y += btn_h + section_pad_y

    info_rect_adj = pygame.Rect(section_x, current_y, section_w, 100)
    ui_regions["info_rect_adj"] = info_rect_adj.copy()
    pygame.draw.rect(screen, (245, 245, 250), info_rect_adj, border_radius=6)
    pygame.draw.rect(screen, (218, 165, 32), info_rect_adj, 1, border_radius=6)
    info_title = section_font.render("Shape Info", True, (218, 165, 32))
    screen.blit(info_title, (info_rect_adj.x + 10, info_rect_adj.y + 5))
    if current_mode == 'Che do 2D':
        info_text = f"Style: {selected_line_style}"
        if selected_shape_indices and 0 <= selected_shape_indices[0] < len(shapes):
            shape = shapes[selected_shape_indices[0]]
            info_text = f"{format_shape_data(shape, detailed=True)}, {info_text}"
    else:
        info_text = f"Angles: X={rotation_angles[0]:.0f}, Y={rotation_angles[1]:.0f}, Z={rotation_angles[2]:.0f}, Zoom: {zoom_level:.0f}x"
        if selected_shape_indices and 0 <= selected_shape_indices[0] < len(shapes):
            shape = shapes[selected_shape_indices[0]]
            info_text = f"{format_shape_data(shape, detailed=True)}, {info_text}"
    info_surface = font.render(info_text, True, (50, 50, 50))
    max_width = section_w - 20
    if info_surface.get_width() > max_width:
        display_text = info_text
        while font.size(display_text + "...")[0] > max_width and len(display_text) > 1:
            display_text = display_text[:-1]
        display_text += "..."
        info_surface = font.render(display_text, True, (50, 50, 50))
    screen.blit(info_surface, (info_rect_adj.x + 10, info_rect_adj.y + 30))

    current_y += info_rect_adj.height + section_pad_y

    shape_list_rect_adj = pygame.Rect(section_x, current_y, section_w, 120)
    ui_regions["shape_list_rect_adj"] = shape_list_rect_adj.copy()
    pygame.draw.rect(screen, (245, 245, 250), shape_list_rect_adj, border_radius=6)
    pygame.draw.rect(screen, (123, 104, 238), shape_list_rect_adj, 1, border_radius=6)
    list_title = section_font.render("Shape List", True, (123, 104, 238))
    screen.blit(list_title, (shape_list_rect_adj.x + 10, shape_list_rect_adj.y + 5))

    clip_surface = pygame.Surface((shape_list_rect_adj.width - 20, shape_list_rect_adj.height - 30))
    clip_surface.fill((245, 245, 250))
    row_height = 25
    list_start_y = 0
    visible_shapes = shapes[shape_list_scroll_offset:shape_list_scroll_offset + shape_list_max_rows]
    for i, shape in enumerate(visible_shapes):
        row_y = list_start_y + i * row_height
        row_rect = pygame.Rect(5, row_y, section_w - 20, row_height - 3)
        if (i + shape_list_scroll_offset) in selected_shape_indices:
            pygame.draw.rect(clip_surface, (200, 220, 255), row_rect, border_radius=4)
        elif i % 2 == 0:
            pygame.draw.rect(clip_surface, (250, 250, 255), row_rect, border_radius=4)
        shape_text = f"{i + shape_list_scroll_offset + 1}. {format_shape_data(shape, detailed=False)}"
        shape_surface = font.render(shape_text, True, (50, 50, 50))
        max_width = section_w - 40
        if shape_surface.get_width() > max_width:
            display_text = shape_text
            while font.size(display_text + "...")[0] > max_width and len(display_text) > 1:
                display_text = display_text[:-1]
            display_text += "..."
            shape_surface = font.render(display_text, True, (50, 50, 50))
        clip_surface.blit(shape_surface, (row_rect.x + 5, row_rect.y + 3))
    screen.blit(clip_surface, (shape_list_rect_adj.x + 10, shape_list_rect_adj.y + 30))

    if len(shapes) > shape_list_max_rows:
        scroll_bar_height = max(20, shape_list_rect_adj.height * shape_list_max_rows / len(shapes))
        scroll_ratio = shape_list_scroll_offset / max(1, len(shapes) - shape_list_max_rows)
        scroll_bar_y = shape_list_rect_adj.y + 30 + scroll_ratio * (shape_list_rect_adj.height - 30 - scroll_bar_height)
        pygame.draw.rect(screen, (200, 200, 200),
                         (shape_list_rect_adj.right - 15, scroll_bar_y, 10, scroll_bar_height),
                         border_radius=5)

def set_mode(mode):
    global current_mode, selected_draw_mode, selected_transform, rotation_circle_active, selected_shape_indices
    if mode in ['Che do 2D', 'Che do 3D']:
        current_mode = mode
        selected_draw_mode = None
        selected_transform = None
        rotation_circle_active = False
        selected_shape_indices = []
        for box in input_boxes:
            box["value"] = ""
    else:
        print("Che do khong hop le! Chon '2D' hoac '3D'")
        return
    print(f" trasfer sang {mode}")

def handle_zoom(action):
    global zoom_level
    if action == "in":
        zoom_level *= 1.1
    elif action == "out":
        zoom_level *= 0.9
    zoom_level = max(0.1, min(5.0, zoom_level))
    print(f"Zoom level: {zoom_level:.0f}x")

shapes = []
drawing_shape = False
start_point = None
end_point = None
last_end_point = None
shape_params = {}
shape_list_scroll_offset = 0
doors = []

def start_tank_animation():
    global shapes, animation_active, animation_step, doors
    shapes = []
    offset_x = -10
    frame_points = [(40 + offset_x, -20), (75 + offset_x, -20), (75 + offset_x, 20), (40 + offset_x, 20)]
    shapes.append({"type": "Hinh Chu Nhat", "data": frame_points, "style": "Lien", "name": "khung_cong", "initial_data": copy.deepcopy(frame_points)})
    door_height = 30
    door_width_small = 4
    door_width_large = 8
    y_top = -door_height // 2
    y_bot = door_height // 2
    doors = [
        {"name": "cong trai", "center_x": 48 + offset_x, "width": door_width_small},
        {"name": "cong phai", "center_x": 67 + offset_x, "width": door_width_small},
        {"name": "cong giua trai", "center_x": 56 + offset_x, "width": door_width_large},
        {"name": "cong giua phai", "center_x": 61 + offset_x, "width": door_width_large},
    ]
    for door in doors:
        w = door["width"]
        cx = door["center_x"]
        points = [
            (cx - w/2, y_top),
            (cx + w/2, y_top),
            (cx + w/2, y_bot),
            (cx - w/2, y_bot)
        ]
        shapes.append({
            "type": "Hinh Chu Nhat",
            "data": points,
            "style": "Lien",
            "name": door["name"],
            "initial_data": copy.deepcopy(points)
        })
    tank1_start_x = -40
    tank2_start_x = -50
    tank1_center = (tank1_start_x, 0)
    tank2_center = (tank2_start_x, 0)
    tank1_shapes = file_2D.create_tank(tank1_center[0], tank1_center[1], 14, "Lien", group="tank1")
    tank2_shapes = file_2D.create_tank(tank2_center[0], tank2_center[1], 14, "Lien", group="tank2")
    for s in tank1_shapes:
        s['tank_center'] = tank1_center
    for s in tank2_shapes:
        s['tank_center'] = tank2_center
    shapes.extend(tank1_shapes)
    shapes.extend(tank2_shapes)
    animation_active = True
    animation_step = 0

def update_animation():
    global shapes, animation_step
    step = animation_step

    # Define animation parameters
    tank1_start_x = -40
    tank1_target_x = doors[0]["center_x"]
    tank1_move_steps = 100  # Steps for tank1 to reach the door
    door_open_steps = 50    # Steps for door to open
    tank2_start_step = 50   # Step when tank2 starts moving
    tank2_target_x = (doors[2]["center_x"] + doors[3]["center_x"]) / 2
    tank2_move_steps = 100  # Steps for tank2 to reach its target

    # Tank1 movement
    tank1_shapes = [s for s in shapes if s.get("group") == "tank1"]
    if tank1_shapes:
        if step <= tank1_move_steps:
            t = step / tank1_move_steps
            x = tank1_start_x + (tank1_target_x - tank1_start_x) * t
        else:
            x = tank1_target_x
        dx = x - tank1_shapes[0]['tank_center'][0]
        transform_matrix = MTBD.TinhTien2D(dx, 0)
        new_tank_center = (x, tank1_shapes[0]['tank_center'][1])
        for shape in tank1_shapes:
            new_shape = MTBD.apply_transform(shape, transform_matrix, "Custom", input_boxes, MAX_RADIUS)
            shape["data"] = new_shape["data"]
            shape["tank_center"] = new_tank_center

    # Door opening for tank1 (left door)
    if step >= tank1_move_steps:
        door_open_t = min((step - tank1_move_steps) / door_open_steps, 1.0)
        door = doors[0]  # Left door
        door_shape = next((s for s in shapes if s.get("name") == door["name"]), None)
        if door_shape:
            dx = -50 * door_open_t
            dy = 0
            angle = 90 * door_open_t
            sx = sy = 1 - 0.5 * door_open_t
            c = (door["center_x"], 0)
            T_c = MTBD.TinhTien2D(c[0], c[1])
            T_minus_c = MTBD.TinhTien2D(-c[0], -c[1])
            R = MTBD.Quay2D(angle)
            S = MTBD.TiLe2D(sx, sy)
            T_dx_dy = MTBD.TinhTien2D(dx, dy)
            R_center = T_c @ R @ T_minus_c
            S_center = T_c @ S @ T_minus_c
            M = T_dx_dy @ R_center @ S_center
            initial_points = door_shape["initial_data"]
            new_points = [MTBD.transform_point(p, M) for p in initial_points]
            door_shape["data"] = new_points

    # Tank2 movement
    tank2_shapes = [s for s in shapes if s.get("group") == "tank2"]
    if tank2_shapes and step >= tank2_start_step:
        move_step = step - tank2_start_step
        if move_step <= tank2_move_steps:
            t = move_step / tank2_move_steps
            x = tank2_start_x + (tank2_target_x - tank2_start_x) * t
        else:
            x = tank2_target_x
        dx = x - tank2_shapes[0]['tank_center'][0]
        transform_matrix = MTBD.TinhTien2D(dx, 0)
        new_tank_center = (x, tank2_shapes[0]['tank_center'][1])
        for shape in tank2_shapes:
            new_shape = MTBD.apply_transform(shape, transform_matrix, "Custom", input_boxes, MAX_RADIUS)
            shape["data"] = new_shape["data"]
            shape["tank_center"] = new_tank_center

    # Door opening for tank2 (middle doors)
    if step >= tank1_move_steps + tank2_start_step:
        door_open_t = min((step - (tank1_move_steps + tank2_start_step)) / door_open_steps, 1.0)
        for door in doors[2:4]:  # Middle left and right doors
            door_shape = next((s for s in shapes if s.get("name") == door["name"]), None)
            if door_shape:
                sign = -1 if door["name"] == "cong giua trai" else 1
                dx = 50 * door_open_t * sign
                dy = 0
                angle = 90 * door_open_t * sign
                sx = sy = 1 - 0.5 * door_open_t
                c = (door["center_x"], 0)
                T_c = MTBD.TinhTien2D(c[0], c[1])
                T_minus_c = MTBD.TinhTien2D(-c[0], -c[1])
                R = MTBD.Quay2D(angle)
                S = MTBD.TiLe2D(sx, sy)
                T_dx_dy = MTBD.TinhTien2D(dx, dy)
                R_center = T_c @ R @ T_minus_c
                S_center = T_c @ S @ T_minus_c
                M = T_dx_dy @ R_center @ S_center
                initial_points = door_shape["initial_data"]
                new_points = [MTBD.transform_point(p, M) for p in initial_points]
                door_shape["data"] = new_points

def draw_coordinates_info(screen, font, shapes):
    info_text = [f"Shapes: {len(shapes)}"]
    tank_groups = {}
    for idx, s in enumerate(shapes):
        group = s.get("group", "")
        if group and group.startswith("tank"):
            if group not in tank_groups:
                tank_groups[group] = []
            tank_groups[group].append(s)
    for group_name, group_shapes in tank_groups.items():
        if group_shapes:
            center_x = group_shapes[0].get("tank_center", (0, 0))[0]
            center_y = group_shapes[0].get("tank_center", (0, 0))[1]
            info_text.append(f"{group_name}: ({center_x:.0f}, {center_y:.0f})")
    for s in shapes:
        if s["type"] == "Hinh Tron":
            x, y, r = s["data"]
            info_text.append(f"  Hinh tron: ({x:.0f}, {y:.0f}), R={r:.0f}")
        elif s["type"] == "Hinh Elip":
            x, y, a, b, angle = s["data"]
            info_text.append(f"  Hinh elip: ({x:.0f}, {y:.0f}), a={a:.0f}, b={b:.0f}, angle={angle:.0f}")
        elif s["type"] == "Doan Thang":
            (x0, y0), (x1, y1) = s["data"]
            info_text.append(f"  Doan thang: ({x0:.0f}, {y0:.0f}) -> ({x1:.0f}, {y1:.0f})")
        elif s["type"] == "Mui Ten":
            (x0, y0), (x1, y1) = s["data"]
            info_text.append(f"  Mui ten: ({x0:.0f}, {y0:.0f}) -> ({x1:.0f}, {y1:.0f})")
        elif s["type"] == "Hinh Chu Nhat":
            points = s["data"]
            info_text.append(f"  Hinh CN: {[(round(px,1), round(py,1)) for px,py in points]}")
        elif s["type"] == "Ngoi Sao":
            x, y, r, *_ = s["data"]
            info_text.append(f"  Ngoi sao: ({x:.0f}, {y:.0f}), R={r:.1f}")
    for shape in shapes:
        if shape.get("name") in ["cong trai", "cong phai", "cong giua trai", "cong giua phai"]:
            points = shape["data"]
            if isinstance(points, list) and len(points) == 4:
                cx = (points[0][0] + points[2][0]) / 2
                cy = (points[0][1] + points[2][1]) / 2
                info_text.append(f"{shape['name']}: ({cx:.0f}, {cy:.0f})")
    for shape in shapes:
        if shape["type"] == "Dong Ho" and "hands" in shape:
            hands = shape["hands"]
            info_text.append(f"Hour Hand: ({hands['hour_hand'][0]:.0f}, {hands['hour_hand'][1]:.0f})")
            info_text.append(f"Minute Hand: ({hands['minute_hand'][0]:.0f}, {hands['minute_hand'][1]:.0f})")
            info_text.append(f"Second Hand: ({hands['second_hand'][0]:.0f}, {hands['second_hand'][1]:.0f})")
    y_offset = 0
    for text in info_text:
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (draw_area.x + 10, draw_area.y + 50 + y_offset * 20))  # Adjusted y-position
        y_offset += 1

def update_scene():
    global last_end_point
    file_2D.update_clock_hands_in_shapes(shapes)
    if current_mode == 'Che do 2D':
        file_2D.draw_grid(screen, UNIT_SIZE, draw_area)
        file_2D.draw_axes_2d(screen, draw_area)
        tank_groups = {}
        for idx, shape in enumerate(shapes):
            group = shape.get("group", "")
            if group and group.startswith("tank"):
                if group not in tank_groups:
                    tank_groups[group] = []
                tank_groups[group].append((idx, shape))
        colored_indices = set()
        for group, group_shapes in tank_groups.items():
            group_shapes = sorted(group_shapes, key=lambda x: x[0])
            color_order = [
                (110, 70, 30),
                (120, 120, 120),
                (120, 120, 120),
                (120, 120, 120),
                (120, 120, 120),
                (0, 128, 0),
                (0, 128, 0),
                (200, 0, 0),
                (255, 215, 0),
            ]
            for i, (idx, shape) in enumerate(group_shapes):
                fill_color = color_order[i] if i < len(color_order) else None
                colored_indices.add(idx)
        for idx, shape in enumerate(shapes):
            if idx in colored_indices:
                continue
            fill_color = None
            group = shape.get("group", "")
            if group and group.startswith("clock"):
                if shape["type"] == "Hinh Tron":
                    fill_color = (180, 240, 240)
            if shape["type"] == "Doan Thang":
                (x0, y0), (x1, y1) = shape["data"]
                file_2D.DoanThang(x0, y0, x1, y1, shape["style"], screen, draw_area, UNIT_SIZE)
            elif shape["type"] == "Mui Ten":
                (x0, y0), (x1, y1) = shape["data"]
                file_2D.MuiTen(x0, y0, x1, y1, shape["style"], screen, draw_area, UNIT_SIZE)
            elif shape["type"] == "Hinh Chu Nhat":
                file_2D.HinhChuNhat(shape["data"], shape["style"], screen, draw_area, UNIT_SIZE, fill_color=fill_color)
            elif shape["type"] == "Hinh Tron":
                center_x, center_y, R = shape["data"]
                file_2D.VeCircle(center_x, center_y, R, shape["style"], screen, draw_area, UNIT_SIZE, fill_color=fill_color)
            elif shape["type"] == "Ngoi Sao":
                data = shape["data"]
                if len(data) == 4:
                    center_x, center_y, R, angle = data
                else:
                    center_x, center_y, R = data
                    angle = 0
                file_2D.VeNgoiSao(center_x, center_y, R, angle, shape["style"], screen, draw_area, UNIT_SIZE)
            elif shape["type"] == "Hinh Elip":
                center_x, center_y, a, b, angle = shape["data"]
                reflect_mode = shape.get("reflect_mode", None)
                file_2D.VeEllipse(center_x, center_y, a, b, angle, shape["style"], screen, draw_area, UNIT_SIZE, reflect_mode=reflect_mode, fill_color=fill_color)
            elif shape["type"] == "Dong Ho":
                center_x, center_y, radius = shape["data"]
                file_2D.DongHo(center_x, center_y, radius, shape["style"], screen, draw_area, UNIT_SIZE, show_coords=True, font=font)
            elif shape["type"] == "HinhThang":
                file_2D.HinhChuNhat(shape["data"], shape["style"], screen, draw_area, UNIT_SIZE, fill_color=fill_color)
            elif shape["type"] == "HinhVuong":
                file_2D.HinhChuNhat(shape["data"], shape["style"], screen, draw_area, UNIT_SIZE, fill_color=fill_color)
        if drawing_shape and start_point and end_point:
            if not last_end_point or (round(end_point[0], 2), round(end_point[1], 2)) != (round(last_end_point[0], 2), round(last_end_point[1], 2)):
                start_x, start_y = file_2D.convert_pos((start_point[0], start_point[1]), draw_area, UNIT_SIZE)
                end_x, end_y = file_2D.convert_pos((end_point[0], end_point[1]), draw_area, UNIT_SIZE)
                if selected_draw_mode == "Doan Thang":
                    file_2D.DoanThang(start_x, start_y, end_x, end_y, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Mui Ten":
                    file_2D.MuiTen(start_x, start_y, end_x, end_y, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Hinh Chu Nhat":
                    x0 = min(start_x, end_x)
                    y0 = min(start_y, end_y)
                    x1 = max(start_x, end_x)
                    y1 = max(start_y, end_y)
                    points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                    file_2D.HinhChuNhat(points, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Hinh Tron":
                    R = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                    if R > 0:
                        file_2D.VeCircle(start_x, start_y, R, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Hinh Elip":
                    a = min(abs(end_x - start_x), MAX_RADIUS)
                    b = min(abs(end_y - start_y), MAX_RADIUS)
                    if a > 0 and b > 0:
                        file_2D.VeEllipse(start_x, start_y, a, b, 0, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Dong Ho":
                    R = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                    if R > 0:
                        file_2D.DongHo(start_x, start_y, R, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Xe Tang":
                    size = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                    if size > 0:
                        group = f"tank_preview"
                        temp_tank_shapes = file_2D.create_tank(start_x, start_y, size, selected_line_style, group)
                        for s in temp_tank_shapes:
                            s['tank_center'] = (start_x, start_y)
                        file_2D.veXeTang(temp_tank_shapes, screen=screen, draw_area=draw_area, UNIT_SIZE=UNIT_SIZE)
                elif selected_draw_mode == "HinhThang":
                    points = get_trapezoid_points(start_x, start_y, end_x, end_y)
                    file_2D.HinhChuNhat(points, selected_line_style, screen, draw_area, UNIT_SIZE)
                last_end_point = end_point
        for group, group_shapes in tank_groups.items():
            group_shapes = [s for _, s in sorted(group_shapes, key=lambda x: x[0])]
            fill_color_map = {
                0: (110, 70, 30),
                1: (120, 120, 120),
                2: (120, 120, 120),
                3: (120, 120, 120),
                4: (120, 120, 120),
                5: (0, 128, 0),
                6: (0, 128, 0),
                7: (200, 0, 0),
                8: (255, 215, 0),
            }
            file_2D.veXeTang(group_shapes, screen=screen, draw_area=draw_area, UNIT_SIZE=UNIT_SIZE, fill_color_map=fill_color_map)
        if drawing_shape and start_point and end_point:
            if not last_end_point or (round(end_point[0], 2), round(end_point[1], 2)) != (round(last_end_point[0], 2), round(last_end_point[1], 2)):
                start_x, start_y = file_2D.convert_pos((start_point[0], start_point[1]), draw_area, UNIT_SIZE)
                end_x, end_y = file_2D.convert_pos((end_point[0], end_point[1]), draw_area, UNIT_SIZE)
                if selected_draw_mode == "Doan Thang":
                    file_2D.DoanThang(start_x, start_y, end_x, end_y, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Mui Ten":
                    file_2D.MuiTen(start_x, start_y, end_x, end_y, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Hinh Chu Nhat":
                    x0 = min(start_x, end_x)
                    y0 = min(start_y, end_y)
                    x1 = max(start_x, end_x)
                    y1 = max(start_y, end_y)
                    points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                    file_2D.HinhChuNhat(points, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Hinh Tron":
                    R = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                    if R > 0:
                        file_2D.VeCircle(start_x, start_y, R, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Hinh Elip":
                    a = min(abs(end_x - start_x), MAX_RADIUS)
                    b = min(abs(end_y - start_y), MAX_RADIUS)
                    if a > 0 and b > 0:
                        file_2D.VeEllipse(start_x, start_y, a, b, 0, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "Dong Ho":
                    R = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                    if R > 0:
                        file_2D.DongHo(start_x, start_y, R, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "HinhThang":
                    points = get_trapezoid_points(start_x, start_y, end_x, end_y)
                    file_2D.HinhChuNhat(points, selected_line_style, screen, draw_area, UNIT_SIZE)
                elif selected_draw_mode == "HinhVuong":
                    points = get_square_points(start_x, start_y, end_x, end_y)
                    file_2D.HinhChuNhat(points, selected_line_style, screen, draw_area, UNIT_SIZE)
                last_end_point = end_point
    elif current_mode == 'Che do 3D':
        file_3D.draw_3d_axes(screen, UNIT_SIZE, draw_area, axis_length=100)
        for shape in shapes:
            if shape["type"] == "Hinh hop CN":
                x, y, z, length, width, height = shape["data"]
                file_3D.draw_3d_cuboid_rotated(screen, (x, y, z), length, width, height, rotation_angles,
                                               UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
            elif shape["type"] == "Hinh Cau":
                x, y, z, radius = shape["data"]
                file_3D.draw_3d_sphere_rotated(screen, (x, y, z), radius, rotation_angles,
                                               UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
            elif shape["type"] == "Den J97":
                x, y, z, height, width = shape["data"]
                file_3D.draw_3d_streetlight(screen, (x, y, z), height, width, rotation_angles,
                                            UNIT_SIZE=UNIT_SIZE, draw_area=draw_area, zoom_level=zoom_level, camera_offset=camera_offset)
    draw_coordinates_info(screen, font, shapes)

running = True
while running:
    screen.fill((255, 255, 255))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if draw_area.collidepoint(mouse_pos) and selected_draw_mode in ["Doan Thang", "Mui Ten", "Hinh Chu Nhat", "Hinh Tron", "Hinh Elip", "Xe Tang", "Dong Ho", "HinhThang", "HinhVuong"]:
                start_point = mouse_pos
                end_point = start_point
                drawing_shape = True
                print(f"Diem bat dau: {start_point}")
            elif ui_regions["shape_list_rect_adj"] and ui_regions["shape_list_rect_adj"].collidepoint(mouse_pos):
                row_height = 25
                rel_y = mouse_pos[1] - (ui_regions["shape_list_rect_adj"].y + 30)
                if rel_y >= 0:
                    index = shape_list_scroll_offset + int(rel_y // row_height)
                    if 0 <= index < len(shapes):
                        shape = shapes[index]
                        if "group" in shape:
                            group = shape["group"]
                            selected_shape_indices = [i for i, s in enumerate(shapes) if s.get("group") == group]
                        else:
                            selected_shape_indices = [index]
                        print(f"Chon hinh: {selected_shape_indices}")
            elif selected_transform in ["Quay O", "Quay Tam"] and ui_regions["input_area_rect"]:
                circle_center = (ui_regions["input_area_rect"].x + ui_regions["input_area_rect"].width // 2, ui_regions["input_area_rect"].y + ui_regions["input_area_rect"].height // 2)
                rotation_circle_radius = 40
                dx = mouse_pos[0] - circle_center[0]
                dy = mouse_pos[1] - circle_center[1]
                if (dx**2 + dy**2)**0.5 <= rotation_circle_radius + 10:
                    rotation_circle_active = True
            active_labels = get_active_labels()
            if ui_regions["input_area_rect"]:
                input_box_positions = get_input_box_positions(ui_regions["input_area_rect"])
                for label, box_rect in input_box_positions:
                    if box_rect.collidepoint(mouse_pos) and label in active_labels:
                        for box in input_boxes:
                            box["active"] = (box["label"] == label)
            allowed_sections = ["mode", "transform", "control", "animation"]
            if current_mode == 'Che do 2D':
                allowed_sections.extend(["2d", "line"])
            elif current_mode == 'Che do 3D':
                allowed_sections.append("3d")
            for button in buttons:
                if button["section"] in allowed_sections and button["rect"].collidepoint(mouse_pos):
                    if button["text"] in ['Che do 2D', 'Che do 3D']:
                        set_mode(button["text"])
                    elif button["text"] in [
                        "Doan Thang", "Mui Ten", "Hinh Tron", "Hinh Elip", "Hinh Chu Nhat", "Xe Tang", "Dong Ho", "HinhThang", "HinhVuong",
                        "Hinh hop CN", "Hinh Cau", "Den J97"
                    ]:
                        selected_draw_mode = button["text"]
                        selected_transform = None
                        for box in input_boxes:
                            box["value"] = ""
                        print(f"Chon che do ve: {selected_draw_mode}")
                    elif button["text"] in ["Net Lien", "Net Dut", "Net Cham"]:
                        selected_line_style = button["text"].split()[1]
                        print(f"Chon kieu net: {selected_line_style}")
                    elif button["text"] in ["Tinh Tien", "Doi Xung Ox", "Doi Xung Oy", "Doi Xung O", "Ty Le", "Quay O", "Quay Tam"]:
                        selected_transform = button["text"]
                        selected_draw_mode = None
                        for box in input_boxes:
                            box["value"] = ""
                        print(f"Chon phep bien doi: {selected_transform}")
                    elif button["text"] == "Xoa Du Lieu":
                        shapes.clear()
                        shape_params.clear()
                        drawing_shape = False
                        start_point = None
                        end_point = None
                        last_end_point = None
                        rotation_angles = [0, 0, 0]
                        zoom_level = 1.0
                        camera_offset = [0, 0]
                        selected_shape_indices = []
                        shape_list_scroll_offset = 0
                        for box in input_boxes:
                            box["value"] = ""
                    elif button["text"] == "Ap Dung":
                        try:
                            if selected_draw_mode in ["Doan Thang", "Mui Ten"]:
                                x0 = [box["value"] for box in input_boxes if box["label"] == "X0:"][0]
                                y0 = [box["value"] for box in input_boxes if box["label"] == "Y0:"][0]
                                x1 = [box["value"] for box in input_boxes if box["label"] == "X1:"][0]
                                y1 = [box["value"] for box in input_boxes if box["label"] == "Y1:"][0]
                                if x0 and y0 and x1 and y1:
                                    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
                                    shapes.append({
                                        "type": selected_draw_mode,
                                        "data": ((x0, y0), (x1, y1)),
                                        "style": selected_line_style,
                                        "initial_data": copy.deepcopy(((x0, y0), (x1, y1)))
                                    })
                                    selected_shape_indices = [len(shapes) - 1]
                            elif selected_draw_mode in ["Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
                                x0 = [box["value"] for box in input_boxes if box["label"] == "X0:"][0]
                                y0 = [box["value"] for box in input_boxes if box["label"] == "Y0:"][0]
                                x1 = [box["value"] for box in input_boxes if box["label"] == "X1:"][0]
                                y1 = [box["value"] for box in input_boxes if box["label"] == "Y1:"][0]
                                if x0 and y0 and x1 and y1:
                                    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
                                    if selected_draw_mode == "Hinh Chu Nhat":
                                        points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                                    elif selected_draw_mode == "HinhThang":
                                        points = get_trapezoid_points(x0, y0, x1, y1)
                                    elif selected_draw_mode == "HinhVuong":
                                        points = get_square_points(x0, y0, x1, y1)
                                    shapes.append({
                                        "type": selected_draw_mode,
                                        "data": points,
                                        "style": selected_line_style,
                                        "initial_data": copy.deepcopy(points)
                                    })
                                    selected_shape_indices = [len(shapes) - 1]
                            elif selected_draw_mode in ["Hinh Tron", "Dong Ho"]:
                                x = [box["value"] for box in input_boxes if box["label"] == "X:"][0]
                                y = [box["value"] for box in input_boxes if box["label"] == "Y:"][0]
                                r = [box["value"] for box in input_boxes if box["label"] == "R:"][0]
                                if r:
                                    x = float(x) if x else 0
                                    y = float(y) if y else 0
                                    r = float(r)
                                    if r > 0:
                                        if selected_draw_mode == "Dong Ho":
                                            group = f"clock_{len(shapes)}"
                                            clock_shapes = file_2D.create_clock(x, y, r, selected_line_style, group)
                                            shapes.extend(clock_shapes)
                                            selected_shape_indices = list(range(len(shapes) - len(clock_shapes), len(shapes)))
                                        else:
                                            shapes.append({
                                                "type": selected_draw_mode,
                                                "data": (x, y, r),
                                                "style": selected_line_style,
                                                "initial_data": copy.deepcopy((x, y, r))
                                            })
                                            selected_shape_indices = [len(shapes) - 1]
                            elif selected_draw_mode == "Xe Tang":
                                x = [box["value"] for box in input_boxes if box["label"] == "X:"][0]
                                y = [box["value"] for box in input_boxes if box["label"] == "Y:"][0]
                                s = [box["value"] for box in input_boxes if box["label"] == "S:"][0]
                                if s:
                                    x = float(x) if x else 0
                                    y = float(y) if y else 0
                                    s = float(s)
                                    if s > 0:
                                        group = f"tank_{len(shapes)}"
                                        tank_shapes = file_2D.create_tank(x, y, s, selected_line_style, group)
                                        for s in tank_shapes:
                                            s['tank_center'] = (x, y)
                                        shapes.extend(tank_shapes)
                                        selected_shape_indices = list(range(len(shapes) - len(tank_shapes), len(shapes)))
                            elif selected_draw_mode == "Hinh Elip":
                                x = [box["value"] for box in input_boxes if box["label"] == "X:"][0]
                                y = [box["value"] for box in input_boxes if box["label"] == "Y:"][0]
                                a = [box["value"] for box in input_boxes if box["label"] == "a:"][0]
                                b = [box["value"] for box in input_boxes if box["label"] == "b:"][0]
                                if a and b:
                                    x = float(x) if x else 0
                                    y = float(y) if y else 0
                                    a, b = float(a), float(b)
                                    if a > 0 and b > 0:
                                        shapes.append({
                                            "type": selected_draw_mode,
                                            "data": (x, y, a, b, 0),
                                            "style": selected_line_style,
                                            "initial_data": copy.deepcopy((x, y, a, b, 0))
                                        })
                                        selected_shape_indices = [len(shapes) - 1]
                            elif selected_draw_mode == "Hinh hop CN":
                                x = [box["value"] for box in input_boxes if box["label"] == "X3D:"][0]
                                y = [box["value"] for box in input_boxes if box["label"] == "Y3D:"][0]
                                z = [box["value"] for box in input_boxes if box["label"] == "Z3D:"][0]
                                l = [box["value"] for box in input_boxes if box["label"] == "L:"][0]
                                w = [box["value"] for box in input_boxes if box["label"] == "W:"][0]
                                h = [box["value"] for box in input_boxes if box["label"] == "H:"][0]
                                if x and y and z and l and w and h:
                                    x, y, z, l, w, h = float(x), float(y), float(z), float(l), float(w), float(h)
                                    if l > 0 and w > 0 and h > 0:
                                        shapes.append({
                                            "type": selected_draw_mode,
                                            "data": (x, y, z, l, w, h),
                                            "style": selected_line_style,
                                            "initial_data": copy.deepcopy((x, y, z, l, w, h))
                                        })
                                        selected_shape_indices = [len(shapes) - 1]
                            elif selected_draw_mode == "Hinh Cau":
                                x = [box["value"] for box in input_boxes if box["label"] == "X3D:"][0]
                                y = [box["value"] for box in input_boxes if box["label"] == "Y3D:"][0]
                                z = [box["value"] for box in input_boxes if box["label"] == "Z3D:"][0]
                                r = [box["value"] for box in input_boxes if box["label"] == "R3D:"][0]
                                if x and y and z and r:
                                    x, y, z, r = float(x), float(y), float(z), float(r)
                                    if r > 0:
                                        shapes.append({
                                            "type": selected_draw_mode,
                                            "data": (x, y, z, r),
                                            "style": selected_line_style,
                                            "initial_data": copy.deepcopy((x, y, z, r))
                                        })
                                        selected_shape_indices = [len(shapes) - 1]
                            elif selected_draw_mode == "Den J97":
                                x = [box["value"] for box in input_boxes if box["label"] == "X3D:"][0]
                                y = [box["value"] for box in input_boxes if box["label"] == "Y3D:"][0]
                                z = [box["value"] for box in input_boxes if box["label"] == "Z3D:"][0]
                                l = [box["value"] for box in input_boxes if box["label"] == "L:"][0]
                                w = [box["value"] for box in input_boxes if box["label"] == "W:"][0]
                                if x and y and z and l and w:
                                    x, y, z, l, w = float(x), float(y), float(z), float(l), float(w)
                                    if l > 0 and w > 0:
                                        shapes.append({
                                            "type": selected_draw_mode,
                                            "data": (x, y, z, l, w),
                                            "style": selected_line_style,
                                            "initial_data": copy.deepcopy((x, y, z, l, w))
                                        })
                                        selected_shape_indices = [len(shapes) - 1]
                            def get_selected_groups():
                                group_map = {}
                                for idx in selected_shape_indices:
                                    shape = shapes[idx]
                                    group = shape.get("group")
                                    if group:
                                        if group not in group_map:
                                            group_map[group] = []
                                        group_map[group].append(idx)
                                return group_map

                            def get_all_indices_for_groups(group_map):
                                all_indices = set()
                                for group in group_map:
                                    all_indices.update(i for i, s in enumerate(shapes) if s.get("group") == group)
                                return list(sorted(all_indices))

                            group_map = get_selected_groups()
                            if group_map:
                                indices_to_transform = get_all_indices_for_groups(group_map)
                            else:
                                indices_to_transform = selected_shape_indices[:]

                            def update_tank_center(indices):
                                if not indices:
                                    return
                                group = shapes[indices[0]].get("group")
                                if group and str(group).startswith("tank"):
                                    tank_center = None
                                    for idx in indices:
                                        if 'tank_center' in shapes[idx]:
                                            tank_center = shapes[idx]['tank_center']
                                            break
                                    if tank_center:
                                        for idx in indices:
                                            shapes[idx]["tank_center"] = tank_center

                            if selected_transform == "Tinh Tien" and indices_to_transform:
                                dx = [box["value"] for box in input_boxes if box["label"] == "dx:"][0]
                                dy = [box["value"] for box in input_boxes if box["label"] == "dy:"][0]
                                if dx and dy:
                                    dx, dy = float(dx), float(dy)
                                    transform_matrix = MTBD.TinhTien2D(dx, dy)
                                    for idx in indices_to_transform:
                                        new_shape = MTBD.apply_transform(shapes[idx], transform_matrix, "Custom", input_boxes, MAX_RADIUS)
                                        if new_shape:
                                            shapes[idx] = new_shape
                                    update_tank_center(indices_to_transform)
                            elif selected_transform in ["Doi Xung Ox", "Doi Xung Oy", "Doi Xung O"] and indices_to_transform:
                                truc = "Ox" if selected_transform == "Doi Xung Ox" else "Oy" if selected_transform == "Doi Xung Oy" else "O"
                                for idx in indices_to_transform:
                                    shape = shapes[idx]
                                    if shape["type"] == "Hinh Elip":
                                        from file_2D import ellipse_reflect
                                        cx, cy, a, b, angle = shape["data"]
                                        new_cx, new_cy, a, b, new_angle = ellipse_reflect(cx, cy, a, b, angle, truc)
                                        shape["data"] = (new_cx, new_cy, a, b, new_angle)
                                        shape["reflect_mode"] = None
                                    else:
                                        transform_matrix = MTBD.DoiXung2D(truc)
                                        new_shape = MTBD.apply_transform(shape, transform_matrix, "Custom", input_boxes, MAX_RADIUS)
                                        if new_shape:
                                            shapes[idx] = new_shape
                                update_tank_center(indices_to_transform)
                            elif selected_transform == "Ty Le" and indices_to_transform:
                                sx = [box["value"] for box in input_boxes if box["label"] == "sx:"][0]
                                sy = [box["value"] for box in input_boxes if box["label"] == "sy:"][0]
                                if sx and sy:
                                    sx, sy = float(sx), float(sy)
                                    tank_center = None
                                    group = shapes[indices_to_transform[0]].get("group", None)
                                    if group and str(group).startswith("tank"):
                                        tank_center = shapes[indices_to_transform[0]].get("tank_center", None)
                                    if tank_center:
                                        cx, cy = tank_center
                                        T_c = MTBD.TinhTien2D(cx, cy)
                                        T_minus_c = MTBD.TinhTien2D(-cx, -cy)
                                        S = MTBD.TiLe2D(sx, sy)
                                        transform_matrix = T_c @ S @ T_minus_c
                                    else:
                                        transform_matrix = MTBD.TiLe2D(sx, sy)
                                    for idx in indices_to_transform:
                                        new_shape = MTBD.apply_transform(shapes[idx], transform_matrix, "Custom", input_boxes, MAX_RADIUS)
                                        if new_shape:
                                            shapes[idx] = new_shape
                                    update_tank_center(indices_to_transform)
                            elif selected_transform == "Quay O" and indices_to_transform:
                                angle = [box["value"] for box in input_boxes if box["label"] == "angle:"][0]
                                if angle:
                                    angle = float(angle)
                                    transform_matrix = MTBD.Quay2D(angle)
                                    for idx in indices_to_transform:
                                        new_shape = MTBD.apply_transform(shapes[idx], transform_matrix, "Custom", input_boxes, MAX_RADIUS)
                                        if new_shape:
                                            shapes[idx] = new_shape
                                    update_tank_center(indices_to_transform)
                            elif selected_transform == "Quay Tam" and selected_shape_indices:
                                angle = [box["value"] for box in input_boxes if box["label"] == "angle:"][0]
                                if angle:
                                    angle = float(angle)
                                    selected_shapes = [shapes[idx] for idx in selected_shape_indices]
                                    group_names = set([shape.get("group", None) for shape in selected_shapes])
                                    if len(group_names) == 1 and list(group_names)[0] and str(list(group_names)[0]).startswith("tank"):
                                        group_name = list(group_names)[0]
                                        group_indices = [i for i, s in enumerate(shapes) if s.get("group", None) == group_name]
                                        group_shapes = [shapes[i] for i in group_indices]
                                        tank_center = None
                                        for s in group_shapes:
                                            if 'tank_center' in s:
                                                tank_center = s['tank_center']
                                                break
                                        if tank_center is None:
                                            tank_center = calculate_group_center(group_shapes)
                                        R = MTBD.Quay2D(angle)
                                        T_c = MTBD.TinhTien2D(tank_center[0], tank_center[1])
                                        T_minus_c = MTBD.TinhTien2D(-tank_center[0], -tank_center[1])
                                        transform_matrix = T_c @ R @ T_minus_c
                                        new_tank_center = MTBD.transform_point(tank_center, transform_matrix)
                                        for idx in group_indices:
                                            new_shape = MTBD.apply_transform(shapes[idx], transform_matrix, "Custom", input_boxes, MAX_RADIUS)
                                            if new_shape:
                                                shapes[idx] = new_shape
                                                shapes[idx]["tank_center"] = new_tank_center
                                    else:
                                        group_center = calculate_group_center(selected_shapes)
                                        R = MTBD.Quay2D(angle)
                                        T_c = MTBD.TinhTien2D(group_center[0], group_center[1])
                                        T_minus_c = MTBD.TinhTien2D(-group_center[0], -group_center[1])
                                        transform_matrix = T_c @ R @ T_minus_c
                                        for idx in selected_shape_indices:
                                            new_shape = MTBD.apply_transform(shapes[idx], transform_matrix, "Custom", input_boxes, MAX_RADIUS)
                                            if new_shape:
                                                shapes[idx] = new_shape
                        except ValueError:
                            print("Vui long nhap du lieu hop le!")
                        except Exception as e:
                            print(f"Loi khi ap dung: {e}")
                    elif button["text"] == "Reset":
                        if current_mode == 'Che do 2D':
                            groups_to_reset = set()
                            for idx in selected_shape_indices:
                                if 0 <= idx < len(shapes):
                                    shape = shapes[idx]
                                    if "group" in shape:
                                        groups_to_reset.add(shape["group"])
                                    else:
                                        if "initial_data" in shape:
                                            shapes[idx]["data"] = copy.deepcopy(shape["initial_data"])
                                            if "hands" in shape:
                                                del shapes[idx]["hands"]
                            for group in groups_to_reset:
                                for shape in shapes:
                                    if shape.get("group") == group and "initial_data" in shape:
                                        shape["data"] = copy.deepcopy(shape["initial_data"])
                                        if "hands" in shape:
                                            del shape["hands"]
                            print(f"Reset cac hinh va nhom: {selected_shape_indices}, {groups_to_reset}")
                        elif current_mode == 'Che do 3D':
                            rotation_angles = [0, 0, 0]
                            zoom_level = 1.0
                            camera_offset = [0, 0]
                            for shape in shapes:
                                if "initial_data" in shape:
                                    shape["data"] = copy.deepcopy(shape["initial_data"])
                            print("Reset 3D view va shapes")
                        for box in input_boxes:
                            box["value"] = ""
                    elif button["text"] == "Anim Xe Tang":
                        start_tank_animation()
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing_shape and start_point and end_point:
                start_x, start_y = file_2D.convert_pos(start_point, draw_area, UNIT_SIZE)
                end_x, end_y = file_2D.convert_pos(end_point, draw_area, UNIT_SIZE)
                try:
                    if selected_draw_mode == "Doan Thang":
                        shapes.append({
                            "type": selected_draw_mode,
                            "data": ((start_x, start_y), (end_x, end_y)),
                            "style": selected_line_style,
                            "initial_data": copy.deepcopy(((start_x, start_y), (end_x, end_y)))
                        })
                    elif selected_draw_mode == "Mui Ten":
                        shapes.append({
                            "type": selected_draw_mode,
                            "data": ((start_x, start_y), (end_x, end_y)),
                            "style": selected_line_style,
                            "initial_data": copy.deepcopy(((start_x, start_y), (end_x, end_y)))
                        })
                    elif selected_draw_mode == "Hinh Chu Nhat":
                        x0 = min(start_x, end_x)
                        y0 = min(start_y, end_y)
                        x1 = max(start_x, end_x)
                        y1 = max(start_y, end_y)
                        points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                        shapes.append({
                            "type": selected_draw_mode,
                            "data": points,
                            "style": selected_line_style,
                            "initial_data": copy.deepcopy(points)
                        })
                    elif selected_draw_mode == "Hinh Tron":
                        R = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                        if R > 0:
                            shapes.append({
                                "type": selected_draw_mode,
                                "data": (start_x, start_y, R),
                                "style": selected_line_style,
                                "initial_data": copy.deepcopy((start_x, start_y, R))
                            })
                    elif selected_draw_mode == "Hinh Elip":
                        a = min(abs(end_x - start_x), MAX_RADIUS)
                        b = min(abs(end_y - start_y), MAX_RADIUS)
                        if a > 0 and b > 0:
                            shapes.append({
                                "type": selected_draw_mode,
                                "data": (start_x, start_y, a, b, 0),
                                "style": selected_line_style,
                                "initial_data": copy.deepcopy((start_x, start_y, a, b, 0))
                            })
                    elif selected_draw_mode == "Xe Tang":
                        size = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                        if size > 0:
                            group = f"tank_{len(shapes)}"
                            tank_shapes = file_2D.create_tank(start_x, start_y, size, selected_line_style, group)
                            for s in tank_shapes:
                                s['tank_center'] = (start_x, start_y)
                            shapes.extend(tank_shapes)
                            selected_shape_indices = list(range(len(shapes) - len(tank_shapes), len(shapes)))
                    elif selected_draw_mode == "Dong Ho":
                        R = min(round(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5), MAX_RADIUS)
                        if R > 0:
                            group = f"clock_{len(shapes)}"
                            clock_shapes = file_2D.create_clock(start_x, start_y, R, selected_line_style, group)
                            shapes.extend(clock_shapes)
                            selected_shape_indices = list(range(len(shapes) - len(clock_shapes), len(shapes)))
                    elif selected_draw_mode == "HinhThang":
                        points = get_trapezoid_points(start_x, start_y, end_x, end_y)
                        shapes.append({
                            "type": selected_draw_mode,
                            "data": points,
                            "style": selected_line_style,
                            "initial_data": copy.deepcopy(points)
                        })
                    elif selected_draw_mode == "HinhVuong":
                        points = get_square_points(start_x, start_y, end_x, end_y)
                        shapes.append({
                            "type": selected_draw_mode,
                            "data": points,
                            "style": selected_line_style,
                            "initial_data": copy.deepcopy(points)
                        })
                    selected_shape_indices = [len(shapes) - 1]
                except Exception as e:
                    print(f"Loi khi them hinh: {e}")
                drawing_shape = False
                start_point = None
                end_point = None
                last_end_point = None
            rotation_circle_active = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing_shape and start_point:
                end_point = event.pos
            if rotation_circle_active:
                circle_center = (ui_regions["input_area_rect"].x + ui_regions["input_area_rect"].width // 2,
                                 ui_regions["input_area_rect"].y + ui_regions["input_area_rect"].height // 2)
                dx = event.pos[0] - circle_center[0]
                dy = event.pos[1] - circle_center[1]
                if dx != 0 or dy != 0:
                    rotation_angle = math.degrees(math.atan2(-dy, dx)) % 360
                    for box in input_boxes:
                        if box["label"] == "angle:":
                            box["value"] = f"{rotation_angle:.1f}"
        elif event.type == pygame.MOUSEWHEEL:
            if draw_area.collidepoint(pygame.mouse.get_pos()):
                if current_mode == 'Che do 3D':
                    handle_zoom("in" if event.y > 0 else "out")
                elif ui_regions["shape_list_rect_adj"] and ui_regions["shape_list_rect_adj"].collidepoint(pygame.mouse.get_pos()):
                    max_scroll = max(0, len(shapes) - shape_list_max_rows)
                    shape_list_scroll_offset -= event.y
                    shape_list_scroll_offset = max(0, min(shape_list_scroll_offset, max_scroll))
            else:
                max_scroll = max(0, ui_content_height - ui_rect.height)
                ui_scroll_offset -= event.y * 20
                ui_scroll_offset = max(0, min(ui_scroll_offset, max_scroll))
        elif event.type == pygame.KEYDOWN:
            active_box = next((box for box in input_boxes if box["active"]), None)
            if active_box:
                if event.key == pygame.K_BACKSPACE:
                    active_box["value"] = active_box["value"][:-1]
                elif event.key == pygame.K_RETURN:
                    active_box["active"] = False
                elif event.unicode.isprintable():
                    active_box["value"] += event.unicode
            if current_mode == 'Che do 3D':
                if event.key == pygame.K_LEFT:
                    rotation_angles[1] = (rotation_angles[1] - 5) % 360
                elif event.key == pygame.K_RIGHT:
                    rotation_angles[1] = (rotation_angles[1] + 5) % 360
                elif event.key == pygame.K_UP:
                    rotation_angles[0] = (rotation_angles[0] - 5) % 360
                elif event.key == pygame.K_DOWN:
                    rotation_angles[0] = (rotation_angles[0] + 5) % 360
                elif event.key == pygame.K_a:
                    camera_offset[0] -= 10 / zoom_level
                elif event.key == pygame.K_d:
                    camera_offset[0] += 10 / zoom_level
                elif event.key == pygame.K_w:
                    camera_offset[1] -= 10 / zoom_level
                elif event.key == pygame.K_s:
                    camera_offset[1] += 10 / zoom_level
        elif event.type == pygame.QUIT:
            running = False
    if animation_active:
        animation_step += 1
        update_animation()
    
    update_scene()
    draw_UI(screen, font)
    pygame.display.flip()
pygame.quit()