# Import Module
from bs4 import BeautifulSoup
import os
import tinycss2
import re
from pprint import pprint
import cssutils


# class list set
class_list = set()

for page in os.listdir('../templates'):

    with open(os.path.join('../templates', page), 'r') as htmlfile:
        html_content = htmlfile.read()

    # parse html content
    soup = BeautifulSoup(html_content, 'html.parser')

    # get all tags
    tags = {tag.name for tag in soup.find_all()}

    # iterate all tags
    for tag in tags:

        # find all element of tag
        for i in soup.find_all(tag):

            # if tag has attribute of class
            if i.has_attr("class"):

                if len(i['class']) != 0:
                    class_list.add(" ".join(i['class']))


pprint(class_list)

# for stylesheet in os.listdir('../static/css'):
#
#     with open(os.path.join('../static/css', stylesheet), 'rb') as cssfile:
#         css_content = cssfile.read()
#         rules = tinycss2.parse_stylesheet_bytes(css_content, skip_whitespace=True, skip_comments=True)
#
#     rules = rules[0]  # returns list of rules (unpacks tuple)
#
#
#     for rule in rules:
#         try:
#             print(rule.prelude[0:2])
#         except:
#             pass

