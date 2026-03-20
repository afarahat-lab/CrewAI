import importlib
import os

selection = 0

def clear_console():
	import os
	import platform

	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

clear_console()

def load_libraries() -> list[str]:
	# List all folder that has name "*_lib" and return the name without the suffix. Exclude "crew_lib" and "utils_lib"
	libs = []
	for folder in os.listdir("."):
		if folder.endswith("_lib") and folder not in ["crew_lib", "utils_lib"]:
			libs.append(folder[:-4])  # Remove the "_lib" suffix
			
	# In a real implementation, this could dynamically discover libraries in a directory
	return libs

libs = load_libraries()


print("Select a library to run:")

for i, lib in enumerate(libs, 1):
    print(f"{i}. {lib}")

while True:
    try:
        selection = int(input("Enter the number of the library: "))
        if 1 <= selection <= len(libs):
            break
        else:
            print(f"Please enter a number between 1 and {len(libs)}.")
    except ValueError:
        print("Invalid input. Please enter a number.")

target = libs[selection - 1]

# Warning control
import warnings

warnings.filterwarnings("ignore")

import dotenv

dotenv.load_dotenv()  # Load environment variables from .env file

from crew_lib import build_llm_from_selection


def load_run_crew(target_name: str):
    module_name = f"{target_name}_lib"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            f"Could not import '{module_name}'. Check TARGET_LIBRARY and project structure."
        ) from exc

    create_crew = getattr(module, "run_crew", None)
    if create_crew is None:
        raise AttributeError(f"Module '{module_name}' does not expose 'run_crew'.")
    return create_crew


run_crew = load_run_crew(target)

selected_llm = build_llm_from_selection()

print(f"Running crew for target: {target} using LLM: {selected_llm.__class__.__name__}")

result = run_crew(llm=selected_llm, verbose=True)

# from IPython.display import Markdown
# markdownResult = Markdown(result.raw)

from textwrap import dedent
from rich.console import Console
from rich.markdown import Markdown

raw = dedent(result.raw).strip()

console = Console()
console.print(Markdown(raw))
