def grayscale_to_angle(gray_val):
    assert (gray_val > 0) and (gray_val <= 0xFF), f"Value {gray_val} out of range (0-255)"
    return (gray_val / 0xFF) * 90 

def angle_to_grayscale(angle):
    assert (0 <= angle <= 90), f"Angle {angle} out of range (0-90)"
    return int((angle / 90) * 0xFF)

print(angle_to_grayscale(20))