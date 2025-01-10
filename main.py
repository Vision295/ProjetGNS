import json
from pathlib import Path

local_path = Path("C:/Users/theop/GNS3/projects/testprojetGNS3/project-files/dynamips")

# List all directories in the given path


with open('intent.json', 'r') as file:
      date = json.load(file)


directories = [d for d in local_path.iterdir() if d.is_dir()]

for d in directories:
      dir = d / "configs/"
      print(dir)
      for item in dir.iterdir():
            if item.name.startswith("i") and item.name.endswith("_startup-config.cfg"):
              with open(item, 'r') as file:
                  content = file.read()
                  print(content)

