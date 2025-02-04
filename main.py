import json
from pathlib import Path
from router import Router



with open('intent.json', 'r') as file:
      data = json.load(file)


local_path = Path("C:/Users/theop/GNS3/projects/projetalinfini/project-files/dynamips")#
#local_path = Path("/mnt/c/users/pault/GNS3/projects/projetalinfini/project-files/dynamips")
directories = []
for d in local_path.iterdir():
      if d.is_dir():
            directories.append(d)




for d in directories:
      dir = d / "configs/"
      for item in dir.iterdir():
            if item.name.startswith("i") and item.name.endswith("_startup-config.cfg"):
                with open(item, 'r') as file:
                    content = file.read()
                    router = Router(
                          input=content,
                          extended_intent=data
                    )
                    print("printed on file ", file.name[-22:])
                with open(item, 'w') as file:
                    file.write(router.new_content)