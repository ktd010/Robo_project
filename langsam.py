import cv2
import argparse
import numpy as np
from  PIL  import  Image

from lang_sam import LangSAM
from lang_sam.utils import draw_image


def shift_large_object(mask, mask_center_pt, curr_position, desired_position):
    img_width = mask.shape[1]

    if desired_position == 'left':
        difference_from_end = img_width - mask_center_pt
        if curr_position == 'right':
            shift_amount = -(mask_center_pt - difference_from_end)
        elif curr_position == 'center':
            shift_amount = -(difference_from_end // 2.5)

    elif desired_position == 'right':
        if curr_position == 'left':
            shift_amount = img_width - mask_center_pt
        elif curr_position == 'center':
            shift_amount = mask_center_pt + (mask_center_pt // 2.5)

    elif desired_position == 'center':
        if curr_position == 'right':
            shift_amount = -mask_center_pt // 12
        elif curr_position == 'left':
            shift_amount = mask_center_pt // 3.5

    return shift_amount    

def shift_medium_object(mask_center_pt, curr_position, desired_position):
        
    if desired_position == 'left':
        desired_distance_from_start = 500
        if curr_position == 'right' or 'center':
            shift_amount = -(mask_center_pt - desired_distance_from_start)

    elif desired_position == 'right':
        desired_distance_from_end = 1100
        if curr_position == 'left' or 'center':
            shift_amount = desired_distance_from_end - mask_center_pt

    elif desired_position == 'center':
        if curr_position == 'right':
            shift_amount = -mask_center_pt
        elif curr_position == 'left':
            shift_amount = mask_center_pt

    return shift_amount

def shift_small_object(mask_center_pt, curr_position, desired_position):
        
    if desired_position == 'left':
        desired_distance_from_start = 200
        if curr_position == 'right' or 'center':
            shift_amount = -(mask_center_pt - desired_distance_from_start)

    elif desired_position == 'right':
        desired_distance_from_end = 1400
        if curr_position == 'left' or 'center':
            shift_amount = desired_distance_from_end - mask_center_pt

    elif desired_position == 'center':
        if curr_position == 'right':
            shift_amount = -mask_center_pt
        elif curr_position == 'left':
            shift_amount = mask_center_pt

    return shift_amount

def get_shift_amount(mask, mask_center_pt, curr_position, desired_position):
    img_width = mask.shape[1]

    pts = np.where(mask == 255)[1]
    mask_width = max(pts) - min(pts)

    # TODO Still needs work. Shift amount calculations need improvement so that they perform
    # more dynamically. Currently just hardcoded values so that two images work
    if mask_width >= img_width // 2.5:
        shift_amount = shift_large_object(mask, mask_center_pt, curr_position, desired_position)
    elif img_width // 5 < mask_width < img_width // 2.5:
        shift_amount = shift_medium_object(mask_center_pt, curr_position, desired_position)
    elif mask_width <= img_width // 5:
        shift_amount = shift_small_object(mask_center_pt, curr_position, desired_position)

    return int(shift_amount)

def check_position_in_img(mask, center_pt):
    img_quadrants = list(range(mask.shape[1]))
    quadrant_len = len(img_quadrants) // 3


    # dividing image into three quadrants: left, center, and right. Center quadrant is much smaller than left and right.
    quad1 = img_quadrants[: int(quadrant_len * 1.2)]
    quad2 = img_quadrants[int(quadrant_len * 1.2): int(quadrant_len * 1.8)] 
    quad3 = img_quadrants[int(quadrant_len * 1.8): ]

    if center_pt in quad1:
        position = 'left'
    elif center_pt in quad2:
        position = 'center'
    else:
        position = 'right'

    return position

def get_mask_center_pt(mask):
    
    pts = np.where(mask == 255)[1]
    median = np.median(pts)

    return median

def shift_horizontally(mask, desired_position):
    mask = mask

    mask_center_pt = get_mask_center_pt(mask)
    curr_position = check_position_in_img(mask, mask_center_pt)
    
    if curr_position != desired_position:
        shift_amount = get_shift_amount(mask, mask_center_pt, curr_position, desired_position)
        shifted_mask = np.roll(mask, shift_amount, axis=1)
        return shifted_mask
    else:
        return mask
    
def shift_vertically(mask, direction):
    #TODO same logic as horizontal, just performed across axis=0
    pass

def get_angle(mask):
    '''
    TODO not robust to all cases. Currently just considering objects that are smaller vertically than horizontally as not upright.
    Does not cover cases of objects with larger widths which are upright.
    '''

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through each contour
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        angle = rect[2]

        if angle <= 45:
            return -angle
        else:
            return None

def rotate(mask, angle):

    center = tuple(np.array(mask.shape[::-1]) / 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_mask = cv2.warpAffine(mask, rotation_matrix, mask.shape[::-1], flags=cv2.INTER_NEAREST)

    return rotated_mask

def display_masks(mask):
    cv2.imshow('Final mesh', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run_segmentor(image_path, object_arrangement_response):
    model = LangSAM()
    image_pil = Image.open(image_path).convert("RGB")
    arrangement_dict = {'plate': 'center', 'fork': 'left', 'spoon': 'right', 'knife': 'right'}

    text_prompt = 'fork, spoon, knife, plate'
    # position = ['left', 'right', 'right', 'center']
    masks, boxes, labels, logits = model.predict(image_pil, text_prompt)
    # image_array = np.asarray(image_pil)
    # image = draw_image(image_array, masks, boxes, labels)
    bin_arr_list = []

    for mask, label in zip(masks,labels):
        arr = mask.cpu().numpy().astype(np.uint8)
        arr[arr == 1] = 255
        angle = get_angle(arr)
        if angle is not None:
            arr = rotate(arr, angle)
        arr = shift_horizontally(arr, arrangement_dict[label])
        bin_arr_list.append(arr)

    final_mask = sum(bin_arr_list)

    display_masks(final_mask)

    # display_img = Image.fromarray(image, mode="RGB")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default= 'assets/dining1.jpg')

    args = parser.parse_args()

    run_segmentor(args.image_path)



