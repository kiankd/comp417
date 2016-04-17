# coding=utf-8
__author__ = 'Kian Kenyon-Dean'

import cv2
from numpy import array
from heapq import nsmallest


IMAGE_FILE = 'black_red_2d_objects.png'
SHAPE_AREA_CUTOFF_BOUNDARY = 220
COLOR_THRESHOLD_LIMIT = 25

def get_red_image_objects(image):
    lower_bound = array([0,0,COLOR_THRESHOLD_LIMIT])
    upper_bound = array([0,0,255])

    shape_mask = cv2.inRange(image, lower_bound, upper_bound)

    # This is the objectification step; thanks cv2! This is easy since we only have 2 colors and are in 2D.
    contours, _ = cv2.findContours(shape_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def display_contours(image, contours, comparison_function=None):
    print 'Press enter to display the contours over each object we have detected.'
    for c in contours:
        if not comparison_function or comparison_function(c):
            print cv2.contourArea(c)
            cv2.drawContours(image, [c], -1, (0, 250, 0), 2)
            cv2.imshow("Image", image)
            cv2.waitKey(0)

def analyze_contours(contours):
    smallest = nsmallest(20, map(cv2.contourArea, contours))
    print smallest
    display_contours(image, contours, comparison_function=lambda c: cv2.contourArea(c) in smallest)

    # for c in contours:
    #     print contourArea(c)

if __name__ == '__main__':
    image = cv2.imread(IMAGE_FILE)

    contours = get_red_image_objects(image)
    # analyze_contours(contours)
    # display_contours(image, contours)

    print 'Done'
