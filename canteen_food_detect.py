import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('C:/Users/niunue/OneDrive/Tài liệu/CT_AI/best_value_canteen_food_4.pt')

def load_image(name):
    return cv2.imread(f'C:/Users/niunue/OneDrive/Tài liệu/CT_AI/UI/{name}', cv2.IMREAD_UNCHANGED)

def crop_alpha_region(image):
    if image.shape[2] < 4:
        return image, (0, 0, image.shape[1], image.shape[0])
    alpha = image[:, :, 3]
    coords = cv2.findNonZero(alpha)
    if coords is None:
        return image, (0, 0, image.shape[1], image.shape[0])
    x, y, w, h = cv2.boundingRect(coords)
    cropped = image[y:y+h, x:x+w]
    return cropped, (x, y, w, h)

def overlay_image_alpha(background, overlay, x, y):
    h, w = overlay.shape[:2]
    if overlay.shape[2] < 4:
        return background
    bh, bw = background.shape[:2]
    if x + w > bw:
        w = bw - x
        overlay = overlay[:, :w]
    if y + h > bh:
        h = bh - y
        overlay = overlay[:h, :]
    if w <= 0 or h <= 0:
        return background
    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha * overlay[:, :, c] +
            (1 - alpha) * background[y:y+h, x:x+w, c]
        )
    return background

def is_inside(x, y, btn_x, btn_y, btn_w, btn_h):
    return btn_x <= x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h

tmprices = {
    'rice': 3000,
    'braised meat': 15000, 
    'braised pork with eggs': 18000,
    'braised fish': 15000,
    'stir-fried water spinach': 3000, 
    'fried chicken': 18000,
    'fried eggs': 3000,
    'tofu with tomato sauce': 12000, 
    'greens soup': 5000, 
    'sour soup': 5000, 

}
calories = {
    'rice': 200,
    'braised meat': 250, 
    'braised pork with eggs': 300,
    'braised fish': 220,
    'stir-fried water spinach': 80, 
    'fried chicken': 350,
    'fried eggs': 100,
    'tofu with tomato sauce': 150, 
    'greens soup': 40, 
    'sour soup': 50,
}

camera_width = 480
camera_height = 360
camera_x_offset = 20
camera_y_offset = 20

screen = 'start'
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
detected_items = {}
paused_frame = None

images = {
    'start': load_image('1.png'),
    'capture': load_image('2.png'),
    'payment': load_image('3.png'),
    'thankyou': load_image('4.png'),
}

button_files = {
    'start_1': 'start_1.png',
    'exit_1': 'exit_1.png',
    'capture_2': 'capture_2.png',
    'return_2': 'return_2.png',
    'cancel_2': 'cancel_2.png',
    'pay_2': 'pay_2.png',
    'cash_3': 'cash_3.png',
    'qr_3': 'qr_3.png',
    'home_4': 'home_4.png',
    'return_4': 'return_4.png',
    'exit_4': 'exit_4.png'

}

btn_pos = {
    'start_1': (279, 336),
    'exit_1': (279, 432),
    'capture_2': (26, 419),
    'pay_2': (262, 510),
    'cancel_2': (262, 419),
    'return_2': (26, 510),
    'cash_3': (60, 155),
    'qr_3': (450, 155),
    'home_4': (292, 300),
    'return_4': (292, 396),
    'exit_4': (292, 491)
}

buttons = {}
for key, filename in button_files.items():
    img = load_image(filename)
    cropped, (cx, cy, w, h) = crop_alpha_region(img)
    buttons[key] = {'image': cropped, 'pos': btn_pos[key], 'size': (w, h)}

click_x, click_y = -1, -1
def mouse_callback(event, x, y, flags, param):
    global click_x, click_y
    if event == cv2.EVENT_LBUTTONDOWN:
        click_x, click_y = x, y

cv2.namedWindow('App')
cv2.setMouseCallback('App', mouse_callback)

while True:
    click = (click_x, click_y)
    click_x, click_y = -1, -1

    if screen == 'start':
        frame = images['start'].copy()
        for key in ['start_1', 'exit_1']:
            overlay_image_alpha(frame, buttons[key]['image'], *buttons[key]['pos'])
        if is_inside(*click, *buttons['start_1']['pos'], *buttons['start_1']['size']):
            screen = 'detect'
            paused_frame = None
        elif is_inside(*click, *buttons['exit_1']['pos'], *buttons['exit_1']['size']):
            break

    elif screen == 'detect':
        base_frame = images['capture'].copy()
        if base_frame.shape[2] == 4:
            base_frame = cv2.cvtColor(base_frame, cv2.COLOR_BGRA2BGR)
        if paused_frame is not None:
            camera_view = paused_frame.copy()
        else:
            ret, frame = cap.read()
            if not ret:
                continue
            camera_view = cv2.resize(frame, (camera_width, camera_height))
            results = model(camera_view)[0]
            detected_items = {}
            for box in results.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                detected_items[label] = detected_items.get(label, 0) + 1
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                cv2.rectangle(camera_view, tuple(xyxy[:2]), tuple(xyxy[2:]), (0,255,0), 2)
                cv2.putText(camera_view, label, tuple(xyxy[:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        base_frame[camera_y_offset:camera_y_offset+camera_height,
                   camera_x_offset:camera_x_offset+camera_width] = camera_view

        for key in ['capture_2', 'pay_2', 'cancel_2', 'return_2']:
            overlay_image_alpha(base_frame, buttons[key]['image'], *buttons[key]['pos'])


        y0 = 90
        line_height = 25
        max_text_length = 40 

        for label, count in detected_items.items():
            price = tmprices.get(label, 0) * count
            calo = calories.get(label, 0) * count
            text1 = f"{label} x{count}: {price} VND"
            text2 = f"Calories: {calo} cal"

            if len(text1) > max_text_length:
                words = text1.split()
                mid = len(words) // 2
                text1a = ' '.join(words[:mid])
                text1b = ' '.join(words[mid:])
                cv2.putText(base_frame, text1a, (530, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                y0 += line_height
                cv2.putText(base_frame, text1b, (530, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                y0 += line_height
            else:
                cv2.putText(base_frame, text1, (530, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                y0 += line_height

            cv2.putText(base_frame, text2, (530, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 80, 80), 1)
            y0 += line_height + 5

        if is_inside(*click, *buttons['capture_2']['pos'], *buttons['capture_2']['size']):
            paused_frame = camera_view.copy()
        elif is_inside(*click, *buttons['pay_2']['pos'], *buttons['pay_2']['size']):
            screen = 'payment'
        elif is_inside(*click, *buttons['cancel_2']['pos'], *buttons['cancel_2']['size']):
            paused_frame = None
        elif is_inside(*click, *buttons['return_2']['pos'], *buttons['return_2']['size']):
            screen = 'start'
            paused_frame = None

        frame = base_frame



    elif screen == 'payment':
        frame = images['payment'].copy()
        for key in ['cash_3', 'qr_3']:
            overlay_image_alpha(frame, buttons[key]['image'], *buttons[key]['pos'])
        if is_inside(*click, *buttons['cash_3']['pos'], *buttons['cash_3']['size']):
            screen = 'cash'
            paused_frame = None
        elif is_inside(*click, *buttons['qr_3']['pos'], *buttons['qr_3']['size']):
            screen = 'qr'
            paused_frame = None

    elif screen in ['cash', 'qr', 'thankyou']:
        frame = images['thankyou'].copy()
        for key in ['home_4', 'return_4', 'exit_4']:
            overlay_image_alpha(frame, buttons[key]['image'], *buttons[key]['pos'])
        if is_inside(*click, *buttons['home_4']['pos'], *buttons['home_4']['size']):
            screen = 'start'
            paused_frame = None
        elif is_inside(*click, *buttons['return_4']['pos'], *buttons['return_4']['size']):
            screen = 'detect'
            paused_frame = None
        elif is_inside(*click, *buttons['exit_4']['pos'], *buttons['exit_4']['size']):
            break

    cv2.imshow('App', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

