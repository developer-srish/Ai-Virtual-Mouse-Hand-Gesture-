import cv2, mediapipe as mp, pyautogui, math
import time
import builtins


def print(*args, delay=0.06, end="\n"):
    text = " ".join(str(arg) for arg in args)
    for char in text:
        builtins.print(char, end="", flush=True)
        time.sleep(delay)
    builtins.print(end=end, flush=True)

print("[+]Starting Virtual Mouse...")


print('[+] Made by Srish Ghosh')
print('[+] GitHub: developer-srish')
print('[+] All rights reserved to Srish Ghosh')
print('[+] 10 seconds more to start the program...')

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils
sw, sh = pyautogui.size()

R, s = 100, 5
mx = my = 0
state = [0, 0, 0]

while True:
    _, f = cap.read()
    f = cv2.flip(f, 1)
    h, w = f.shape[:2]
    cv2.rectangle(f, (R, R), (w - R, h - R), (255, 0, 255), 2)

    r = hands.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))

    if r.multi_hand_landmarks:
        hand = r.multi_hand_landmarks[0]
        draw.draw_landmarks(f, hand, mp.solutions.hands.HAND_CONNECTIONS)
        lm = hand.landmark

        p = [(int(lm[i].x * w), int(lm[i].y * h)) for i in (4, 8, 12, 16)]
        (tx, ty), (ix, iy), (mx2, my2), (rx, ry) = p

        x = max(0, min(sw, (ix - R) * sw / (w - 2 * R)))
        y = max(0, min(sh, (iy - R) * sh / (h - 2 * R)))

        mx += (x - mx) / s
        my += (y - my) / s
        pyautogui.moveTo(mx, my)

        for i, (pt, act) in enumerate([
            ((ix, iy), pyautogui.click),
            ((mx2, my2), pyautogui.rightClick),
            ((rx, ry), pyautogui.doubleClick)
        ]):
            if math.hypot(pt[0] - tx, pt[1] - ty) < 30:
                if not state[i]:
                    act()
                    state[i] = 1
            else:
                state[i] = 0

        if iy < R:
            pyautogui.scroll(50)
        elif iy > h - R:
            pyautogui.scroll(-50)

    cv2.imshow("Virtual Mouse", f)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()