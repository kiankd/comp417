# coding=utf-8
__author__ = 'kian'
print 'Loading parser into main memory...'

from spacy.en import English
PARSER = English()

class Grounder:
    def __init__(self):
        self.parsed_doc = None

    def parse_command_to_sdc(self, command):
        self.parsed_doc = PARSER(unicode(command))

        print

    def navigate_parse_tree(self, verbose=True):
        labels = []
        max_length = 23

        for token in self.parsed_doc:
            labels.append(token.dep_)

            if verbose:
                token_string = '\"%s\", %s'%(str(token), token.dep_)

                print token_string,
                print ' '*(max_length-len(token_string))+'-->',

                for child in token.children:
                    s = '\"%s\"'%(str(child))
                    print s + ' ,',
                print


        # while token.head is not token:
        #     labels.append(token.dep)
        #     token = token.head
        print labels


if __name__ == '__main__':
    g = Grounder()
    g.parse_command_to_sdc("Go to the helmet.")
    g.navigate_parse_tree()

    g.parse_command_to_sdc("Put the helmet on the table.")
    g.navigate_parse_tree()

    g.parse_command_to_sdc("Grab the helmet near the table.")
    g.navigate_parse_tree()

    g.parse_command_to_sdc("Travel to the alarm clock in the corner.")
    g.navigate_parse_tree()

