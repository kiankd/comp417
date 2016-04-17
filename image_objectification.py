# coding=utf-8
from copy import deepcopy
from time import sleep

__author__ = 'Kian Kenyon-Dean'

import cv2
import numpy
import pyprind
from heapq import nsmallest



IMAGE_FILE = 'black_red_2d_objects.png'
SHAPE_AREA_CUTOFF_BOUNDARY = 220
COLOR_THRESHOLD_LIMIT = 25
NEW_SHAPE_SEARCH_DEPTH = 100

def euclidean_distance(arr1, arr2):
    """
    Calculate the euclidean distance between the closest points in the contour arrays.
    :param arr1: An N x 1 x 2 array
    :param arr2: An M x 1 x 2 array
    :return: float
    """
    closest_distances = []
    for c1 in arr1:
        closest, closest_dist = None, numpy.inf
        for c2 in arr2:
            d = numpy.sqrt((c1[0,0] - c2[0,0])**2 + (c1[0,1] - c2[0,1])**2) # sqrt (x1-x2)^2 + (y1-y2)^2
            if d < closest_dist:
                closest = c2
                closest_dist = d
            elif d > 750:
                return 999999

        closest_distances.append(closest_dist)

    return numpy.min(closest_distances)

def get_red_image_objects(image):
    lower_bound = numpy.array([0,0,COLOR_THRESHOLD_LIMIT])
    upper_bound = numpy.array([0,0,255])

    shape_mask = cv2.inRange(image, lower_bound, upper_bound)

    # This is the objectification step; thanks cv2! This is easy since we only have 2 colors and are in 2D.
    contours, _ = cv2.findContours(shape_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # We need to fix the objectification because some things are incomplete/are just dots.
    # Here we are finding the bad objects.
    contours_to_fix = {}
    for i,con in enumerate(contours):
        if 3.0 <= cv2.contourArea(con) <= SHAPE_AREA_CUTOFF_BOUNDARY:
            contours_to_fix[i] = con

    new_contours = {i:c for i,c in enumerate(contours) if not i in contours_to_fix.keys()}


    print 'Starting... (calculating Euclidean distances between contours)'
    # Here we are figuring out which objects the bad contours are supposed to be part of.
    for i,bad_con in contours_to_fix.iteritems():
        im_copy = deepcopy(image)
        best_new, best_dist, best_idx = None, numpy.inf, None
        for j in range(max(0,i-NEW_SHAPE_SEARCH_DEPTH), min(len(contours),i+NEW_SHAPE_SEARCH_DEPTH)):
            if not j in contours_to_fix.keys():
                d = euclidean_distance(bad_con, contours[j])
                if d < best_dist:
                    best_new = contours[j]
                    best_dist = d
                    best_idx = j
                cv2.drawContours(im_copy, [contours[j]], -1, (0, 250, 0), 2)

        new_contours[best_idx] = numpy.append(best_new, bad_con)
        cv2.drawContours(im_copy, [bad_con], -1, (255, 0, 0), 2)
        cv2.drawContours(im_copy, [best_new], -1, (255, 0, 0), 2)
        # cv2.drawContours(im_copy, [new_contours[best_idx]], -1, (255, 255, 255), 2)
        cv2.imshow("Image", im_copy)
        cv2.waitKey(0)

    return new_contours.values()

def display_contours(image, contours, comparison_function=None):
    print 'Press enter to display the contours over each object we have detected.'
    for c in contours:
        if not comparison_function or comparison_function(c):
            # print cv2.contourArea(c)
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
    display_contours(image, contours)

    print 'Done'
