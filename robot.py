# coding=utf-8
from copy import deepcopy
from spacy import English
from warnings import warn
import image_objectification as imob

__author__ = 'kian'

# Globals.
UNKNOWN_OBJECT_STRING = 'NA'
PARSER = English()

class Objectified:
    def __init__(self, name, contours):
        self.name = name
        self.contours = contours
        self.spacy_tokenization = PARSER(self.name)

    def __repr__(self):
        return "Objectified: name = %s"%self.name

    def similarity(self, objectified):
        if self.name == objectified.name:
            return 1.0

        score = self.spacy_tokenization.similarity(objectified.spacy_tokenization)
        if score == 0.0:
            warn("One of the strings (%s or %s) does not have a word embedding!"%(self.name, objectified.name))

        return score

class Robot:
    def __init__(self):
        self.world_image = imob.load_image()
        self.world_representation = []

        contours = imob.load_contours()
        annotations = imob.load_object_annotations()
        assert len(contours) == len(annotations)

        for i in range(len(contours)):
            if annotations[i] != UNKNOWN_OBJECT_STRING:
                self.world_representation.append( Objectified(unicode(annotations[i]), contours[i]) )


    def display_objectified_world(self, save=False):
        image = deepcopy(self.world_image)

        for ob in self.world_representation:
            print ob.name
            imob.cv2.drawContours(image, [ob.contours], -1, (0, 250, 0), 2)

            if not save:
                imob.cv2.imshow("Image", image)
                imob.cv2.waitKey(0)
        if save:
            imob.cv2.imwrite('annotated_objectified_world.png', image)

    def display_similarity_scores(self):
        for i in range(len(self.world_representation)-1):
            o1 = self.world_representation[i]
            o2 = self.world_representation[i+1]

            print o1.name,'<-->', o2.name
            print o1.similarity(o2),'\n'

if __name__ == '__main__':
    r = Robot()
    r.display_similarity_scores()

