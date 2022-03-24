from itertools import count
import xml.etree.ElementTree as ET
import json

tree = ET.parse('dependency.xml')
root = tree.getroot()
dependences = {}
counter = 0


def convert_path_to_dot_style(path):
    # "$PROJECT_DIR$/src/main/java/org/java_websocket/AbstractWebSocket.java"
    split_path = path.split('/')[4:]
    return '.'.join(split_path)


for cls in root:
    abs_path = cls.attrib['path']
    if 'test' in abs_path or 'example' in abs_path or not abs_path.endswith('.java'):
        continue
    print("------------------------------")
    counter += 1
    print("file path: ", convert_path_to_dot_style(abs_path))

    abs_path_dot_style = convert_path_to_dot_style(abs_path)

    dependences[abs_path_dot_style] = []

    for dependency in cls:
        abs_path_of_dependency = dependency.attrib['path']
        if abs_path_of_dependency.startswith('$PROJECT_DIR$'):
            print("dependency path: ", convert_path_to_dot_style(
                abs_path_of_dependency))
            abs_path_of_dependency_dot_style = convert_path_to_dot_style(
                abs_path_of_dependency)
            dependences[abs_path_dot_style].append(
                abs_path_of_dependency_dot_style)

with open('json_data.json', 'w') as outfile:
    json.dump(dependences, outfile)

print(counter)
