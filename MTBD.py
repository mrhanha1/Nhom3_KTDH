import numpy as np
import math
import copy

def TinhTien2D(dx, dy):
    return np.array([[1, 0, dx],
                     [0, 1, dy],
                     [0, 0, 1]])

def DoiXung2D(truc):
    if truc == 'Ox':
        return np.array([[1, 0, 0],
                         [0, -1, 0],
                         [0, 0, 1]])
    elif truc == 'Oy':
        return np.array([[-1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])
    elif truc == 'O':
        return np.array([[-1, 0, 0],
                         [0, -1, 0],
                         [0, 0, 1]])

def TiLe2D(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])

def Quay2D(angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return np.array([[cos_a, -sin_a, 0],
                     [sin_a, cos_a, 0],
                     [0, 0, 1]])

def transform_point(point, matrix):
    point_hom = np.array([point[0], point[1], 1])
    result = matrix @ point_hom
    return (result[0], result[1])

def calculate_center(shape):
    shape_type = shape["type"]
    shape_data = shape["data"]
    if shape_type in ["Doan Thang", "Mui Ten"]:
        (x0, y0), (x1, y1) = shape_data
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
    elif shape_type in ["Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
        points = shape_data
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
    elif shape_type in ["Hinh Tron", "Xe Tang", "Dong Ho"]:
        cx, cy, _ = shape_data
    elif shape_type == "Hinh Elip":
        cx, cy, _, _, _ = shape_data
    else:
        cx, cy = 0, 0
    return cx, cy

def apply_transform(shape, transform_matrix, transform_type, input_boxes, MAX_RADIUS):
    shape_type = shape["type"]
    shape_data = shape["data"]
    new_shape = copy.deepcopy(shape)

    # Xử lý đặc biệt cho các hình thuộc nhóm "tank" với "Quay Tam" hoặc "Ty Le"
    if 'group' in shape and shape['group'].startswith('tank') and 'tank_center' in shape:
        tank_center = shape['tank_center']
        if transform_type == "Quay Tam":
            angle_value = float([box["value"] for box in input_boxes if box["label"] == "angle:"][0])
            R = Quay2D(angle_value)
            T_c = TinhTien2D(tank_center[0], tank_center[1])
            T_minus_c = TinhTien2D(-tank_center[0], -tank_center[1])
            transform_matrix = T_c @ R @ T_minus_c
        elif transform_type == "Ty Le":
            sx = float([box["value"] for box in input_boxes if box["label"] == "sx:"][0])
            sy = float([box["value"] for box in input_boxes if box["label"] == "sy:"][0])
            S = TiLe2D(sx, sy)
            T_c = TinhTien2D(tank_center[0], tank_center[1])
            T_minus_c = TinhTien2D(-tank_center[0], -tank_center[1])
            transform_matrix = T_c @ S @ T_minus_c

    if transform_type == "Custom":
        if shape_type in ["Doan Thang", "Mui Ten"]:
            (x0, y0), (x1, y1) = shape_data
            new_p0 = transform_point((x0, y0), transform_matrix)
            new_p1 = transform_point((x1, y1), transform_matrix)
            new_shape["data"] = (new_p0, new_p1)
        elif shape_type in ["Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
            points = shape_data
            new_points = [transform_point(p, transform_matrix) for p in points]
            new_shape["data"] = new_points
        elif shape_type in ["Hinh Tron", "Dong Ho"]:
            x, y, param = shape_data[:3]
            new_center = transform_point((x, y), transform_matrix)
            if len(shape_data) > 3:
                new_shape["data"] = (new_center[0], new_center[1], param) + tuple(shape_data[3:])
            else:
                new_shape["data"] = (new_center[0], new_center[1], param)
            if shape_type == "Dong Ho" and "hands" in new_shape:
                del new_shape["hands"]
        elif shape_type == "Hinh Elip":
            x, y, a, b, angle = shape_data
            new_center = transform_point((x, y), transform_matrix)
            new_shape["data"] = (new_center[0], new_center[1], a, b, angle)
        elif shape_type == "Ngoi Sao":
            if len(shape_data) == 4:
                x, y, r, angle = shape_data
            else:
                x, y, r = shape_data
                angle = 0
            new_center = transform_point((x, y), transform_matrix)
            new_shape["data"] = (new_center[0], new_center[1], r, angle)
        return new_shape

    if transform_type == "Quay Tam" and ('group' not in shape or not shape['group'].startswith('tank')):
        angle_value = float([box["value"] for box in input_boxes if box["label"] == "angle:"][0])
        R = Quay2D(angle_value)
        if shape_type in ["Doan Thang", "Mui Ten", "Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
            c = calculate_center(shape)
            T_c = TinhTien2D(c[0], c[1])
            T_minus_c = TinhTien2D(-c[0], -c[1])
            transform_matrix = T_c @ R @ T_minus_c
        elif shape_type == "Hinh Elip":
            x, y, a, b, angle = shape_data
            new_center = transform_point((x, y), transform_matrix)
            new_shape["data"] = (new_center[0], new_center[1], a, b, (angle + angle_value) % 360)
            return new_shape
        elif shape_type == "Ngoi Sao":
            if len(shape_data) == 4:
                x, y, r, angle = shape_data
            else:
                x, y, r = shape_data
                angle = 0
            new_center = transform_point((x, y), transform_matrix)
            new_angle = (angle + angle_value) % 360
            new_shape["data"] = (new_center[0], new_center[1], r, new_angle)
            return new_shape

    if shape_type in ["Doan Thang", "Mui Ten"]:
        (x0, y0), (x1, y1) = shape_data
        new_p0 = transform_point((x0, y0), transform_matrix)
        new_p1 = transform_point((x1, y1), transform_matrix)
        new_shape["data"] = (new_p0, new_p1)
    
    elif shape_type in ["Hinh Chu Nhat", "HinhThang", "HinhVuong"]:
        points = shape_data
        new_points = [transform_point(p, transform_matrix) for p in points]
        new_shape["data"] = new_points
    
    elif shape_type in ["Hinh Tron", "Xe Tang", "Dong Ho"]:
        x, y, r = shape_data
        new_center = transform_point((x, y), transform_matrix)
        new_r = r
        if transform_type == "Ty Le" and 'group' in shape and shape['group'].startswith('tank'):
            sx = float([box["value"] for box in input_boxes if box["label"] == "sx:"][0])
            sy = float([box["value"] for box in input_boxes if box["label"] == "sy:"][0])
            scale = (sx + sy) / 2  # Tỷ lệ trung bình để giữ hình dạng
            new_r = r * scale
        new_shape["data"] = (new_center[0], new_center[1], new_r)
        if shape_type == "Dong Ho" and "hands" in new_shape:
            del new_shape["hands"]
    
    elif shape_type == "Hinh Elip":
        x, y, a, b, angle = shape_data
        new_center = transform_point((x, y), transform_matrix)
        if transform_type in ["Quay O", "Quay Tam"]:
            angle_value = float([box["value"] for box in input_boxes if box["label"] == "angle:"][0])
            new_angle = (angle + angle_value) % 360
        else:
            new_angle = angle
        if transform_type == "Ty Le":
            sx = float([box["value"] for box in input_boxes if box["label"] == "sx:"][0])
            sy = float([box["value"] for box in input_boxes if box["label"] == "sy:"][0])
            new_a = a * sx
            new_b = b * sy
            new_shape["data"] = (new_center[0], new_center[1], new_a, new_b, new_angle)
        else:
            new_shape["data"] = (new_center[0], new_center[1], a, b, new_angle)
    
    elif shape_type == "Ngoi Sao":
        if len(shape_data) == 4:
            x, y, r, angle = shape_data
        else:
            x, y, r = shape_data
            angle = 0
        new_center = transform_point((x, y), transform_matrix)
        new_r = r
        if transform_type == "Ty Le" and 'group' in shape and shape['group'].startswith('tank'):
            sx = float([box["value"] for box in input_boxes if box["label"] == "sx:"][0])
            sy = float([box["value"] for box in input_boxes if box["label"] == "sy:"][0])
            scale = (sx + sy) / 2  # Tỷ lệ trung bình để giữ hình dạng
            new_r = r * scale
        new_shape["data"] = (new_center[0], new_center[1], new_r, angle)
    
    elif shape_type == "Hinh hop CN":
        x, y, z, l, w, h = shape_data
        new_origin = transform_point((x, y), transform_matrix)
        new_shape["data"] = (new_origin[0], new_origin[1], z, l, w, h)
    
    elif shape_type == "Hinh Cau":
        x, y, z, r = shape_data
        new_origin = transform_point((x, y), transform_matrix)
        new_shape["data"] = (new_origin[0], new_origin[1], z, r)
    
    elif shape_type == "Den J97":
        x, y, z, l, w = shape_data
        new_origin = transform_point((x, y), transform_matrix)
        new_shape["data"] = (new_origin[0], new_origin[1], z, l, w)
    
    return new_shape