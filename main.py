from platform import python_branch
import cv2
import mss
import pyautogui
import numpy as np
import time
import os
import pydirectinput

dirname = os.path.dirname(__file__)
animal_path = os.path.join(dirname, 'animals')

SCT = mss.mss()

def check_animal(animal):
    img = main_screen(height=650)
    result_animal = cv2.matchTemplate(img, animal, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc_animal = cv2.minMaxLoc(result_animal)
    #print(max_val)
    if max_val > .93:
        return max_loc_animal
    else:
        return None

def Put_Away(animal_name, animals, location):
    print(f"Checking for {animal_name}....")
    keep_testing = True
    while keep_testing:
        for animal in animals:
            animal_loc = check_animal(animal)
            if animal_loc is not None:
                pyautogui.moveTo(animal_loc[0] + left_start+20, animal_loc[1] + top_start+10) 
                pydirectinput.mouseDown()
                #pyautogui.mouseUp(location[0] + left_start, location[1] + top_start+10)
                # Try Drag instead?
                pydirectinput.moveTo(location[0] + left_start, location[1] + top_start+10, duration=.3) 
                pydirectinput.mouseUp()
                return True
            else:
                keep_testing = False
        # if animal_name == "Cow":
        #     print('test again......')
        #     for animal in animals:
        #         animal_loc = check_animal(animal)
        #         if animal_loc is not None:
        #             pyautogui.moveTo(animal_loc[0] + left_start+20, animal_loc[1] + top_start+10) 
        #             pydirectinput.mouseDown()
        #             #pyautogui.mouseUp(location[0] + left_start, location[1] + top_start+10)
        #             # Try Drag instead?
        #             pydirectinput.moveTo(location[0] + left_start, location[1] + top_start+10, duration=.025) 
        #             pydirectinput.mouseUp()
        #             return True
    return False

def main_screen(height=800):
    scr = SCT.grab({
                'left': left_start,
                'top': top_start,
                'width': 800,
                'height': height
            })
    img = np.array(scr)
    return cv2.cvtColor(img, cv2.IMREAD_COLOR)

def Try_Again():
    try_img = cv2.imread('tryagain.jpg', cv2.IMREAD_UNCHANGED)
    result_try = cv2.matchTemplate(main_screen(), try_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
    if max_val > .6:
        return max_loc
    else:
        return None

def tip_location():
    try_img = cv2.imread('Check.jpg', cv2.IMREAD_UNCHANGED)
    result_try = cv2.matchTemplate(main_screen(), try_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
    if max_val > .6:
        return max_loc
    else:
        return None

if __name__ == "__main__":
    while True:
        print("Starting in 2....")
        time.sleep(2)
        left_start = 550
        top_start = 190

        Try_loc = Try_Again()
        pyautogui.moveTo(Try_loc[0] + left_start + 10, Try_loc[1] + top_start + 10)
        time.sleep(.5)
        pydirectinput.mouseDown()
        time.sleep(.5)
        pydirectinput.mouseUp()
        time.sleep(2)

        Try_loc = tip_location()
        print(Try_loc)
        pyautogui.moveTo(Try_loc[0] + left_start + 10, Try_loc[1] + top_start + 10)
        time.sleep(.5)
        pydirectinput.mouseDown()
        time.sleep(.5)
        pydirectinput.mouseUp()
        time.sleep(.5)

        color = main_screen()

        pig_barn_img = cv2.imread('PigBarn.png', cv2.IMREAD_UNCHANGED)
        sheep_barn_img = cv2.imread('SheepBarn.png', cv2.IMREAD_UNCHANGED)
        cow_barn_img = cv2.imread('CowBarn.png', cv2.IMREAD_UNCHANGED)

        result_pig = cv2.matchTemplate(color, pig_barn_img, cv2.TM_CCOEFF_NORMED)
        result_sheep = cv2.matchTemplate(color, sheep_barn_img, cv2.TM_CCOEFF_NORMED)
        result_cow = cv2.matchTemplate(color, cow_barn_img, cv2.TM_CCOEFF_NORMED)

        _, _, _, max_loc_pig = cv2.minMaxLoc(result_pig)
        _, _, _, max_loc_sheep = cv2.minMaxLoc(result_sheep)
        _, _, _, max_loc_cow = cv2.minMaxLoc(result_cow)

        # Make pig barn close to sheep so it will accept either one.
        max_loc_pig = (max_loc_pig[0] + 50, max_loc_pig[1] + 100)
        max_loc_sheep = (max_loc_sheep[0] -50, max_loc_sheep[1] + 100)
        max_loc_cow = (max_loc_cow[0], max_loc_cow[1] + 100)

        # cv2.imshow("input", color)
        # cv2.imwrite("test.png", color)
        # cv2.waitKey(0)
    
        pigs = [
            cv2.imread(os.path.join(animal_path, 'Pig.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'PigRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'PigSpecialRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'PigSpecial.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'PigBlack.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'PigBlackRev.jpg'), cv2.IMREAD_UNCHANGED)
        ]

        sheeps = [
            cv2.imread(os.path.join(animal_path, 'Sheep.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'SheepRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'SheepSpecialRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'SheepSpecialRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'SheepSpecial2.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'SheepSpecialRev2.jpg'), cv2.IMREAD_UNCHANGED)
        ]

        cows = [
            cv2.imread(os.path.join(animal_path, 'Cow.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'CowRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'CowSpecial.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'CowSpecialRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'CowBlackRev.jpg'), cv2.IMREAD_UNCHANGED),
            cv2.imread(os.path.join(animal_path, 'CowBlackRev.jpg'), cv2.IMREAD_UNCHANGED)
        ]
        #wait = 4
        replay_shown = None
        while replay_shown is None:

            found = True
            # Check Cow
            while found == True:
                found = Put_Away("Cow", cows, max_loc_cow)

            found = True
            # Check Sheep
            while found == True:
                found = Put_Away("Sheep", sheeps, max_loc_sheep)


            found = True
            # Check Cow
            while found == True:
                found = Put_Away("Cow", cows, max_loc_cow)


            # Check Pig
            # Not worth enough to care about combo.
            found = True
            while found == True:
                found = Put_Away("Pig", pigs, max_loc_pig)

            found = True
            # Check Cow
            while found == True:
                found = Put_Away("Cow", cows, max_loc_cow)
            # Let animals build up a bit.
            #time.sleep(wait)
            #wait = wait * .5
            #print(wait)
            replay_shown = Try_Again()