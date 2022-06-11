import toml
from pprint import pprint

with open('static/content/work_experience.toml', 'r') as tfile:
    d = toml.load(tfile)

pprint(d)