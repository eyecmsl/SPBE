modules = ["python-3.11"]

[nix]
channel = "stable-24_05"
packages = ["SDL2", "SDL2_image", "SDL2_mixer", "SDL2_ttf", "espeak-ng", "fontconfig", "freetype", "libjpeg", "libpng", "pkg-config", "portmidi"]

[workflows]
runButton = "Project"

[[workflows.workflow]]
name = "Project"
mode = "parallel"
author = "agent"

[[workflows.workflow.tasks]]
task = "workflow.run"
args = "Spelling Bee Game"

[[workflows.workflow.tasks]]
task = "workflow.run"
args = "spelling_bee_game"

[[workflows.workflow]]
name = "Spelling Bee Game"
author = "agent"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "pip install pygame pyttsx3 && python main.py"

[[workflows.workflow]]
name = "spelling_bee_game"
author = "agent"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "pip install pygame pyttsx3 && python main.py"

[deployment]
run = ["sh", "-c", "pip install pygame pyttsx3 && python main.py"]
