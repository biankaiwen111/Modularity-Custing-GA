from xml.dom.minidom import Identified
import javalang
import os
import json


class DependencyParser:

    def __init__(self, project_path, self_package_path):
        self.project_path = project_path  # './projects/Java-WebSocket' version 1.4.1
        self.project_files = []
        self.self_package_path = self_package_path  # e.g. org.java_websocket
        self.dependences = {}

    def __str__(self):
        return f'path of the project: {self.project_path} \n number of classes: {len(self.project_files)} \n'

    def traverse_all_java_files(self):
        for subdir, dirs, files in os.walk(self.project_path):
            if 'test' in subdir:
                continue
            if 'example' in subdir:
                continue
            for file in files:
                if file.endswith('.java'):
                    abs_path = os.path.join(subdir, file)
                    self.project_files.append((abs_path, file))
                    print(abs_path)

    def parse(self):
        for java_file_path, filename in self.project_files:
            with open(java_file_path, 'r') as source_file:
                source_code = source_file.read()
                ast = javalang.parse.parse(source_code)
                package_name = ast.package.name
                unique_identified_name = package_name + '.' + filename
                print(unique_identified_name)
                for ipt in ast.imports:
                    if not ipt.path.startswith(self.self_package_path):
                        continue
                    else:
                        if unique_identified_name not in self.dependences:
                            self.dependences[unique_identified_name] = []
                            self.dependences[unique_identified_name].append(
                                ipt.path)
                        else:
                            self.dependences[unique_identified_name].append(
                                ipt.path)

    def export_dependences(self):
        with open('json_data.json', 'w') as outfile:
            json.dump(self.dependences, outfile)


if __name__ == "__main__":
    dependency_parser = DependencyParser(
        './projects/Java-WebSocket', 'org.java_websocket')
    dependency_parser.traverse_all_java_files()
    dependency_parser.parse()
    dependency_parser.export_dependences()
