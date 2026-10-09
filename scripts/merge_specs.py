import yaml
import glob
import os

def merge_specs():
    # The magic word is "recursive=True" and "**/"
    # This way the script searches in the main directory AND in all subfolders!
    # Sorted with '/' as separator so that Windows and Linux (CI) produce the same order
    files = sorted(glob.glob('**/spec_*.yaml', recursive=True), key=lambda p: p.replace(os.sep, '/'))
    merged_data = {}
    
    if not files:
        print("Warning: No files found with the pattern 'spec_*.yaml'!")
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                if data:
                    # Turns 'folder/spec_brushless_combo.yaml' -> 'Brushless Combo'
                    clean_name = os.path.basename(file).replace('spec_', '').replace('.yaml', '').replace('_', ' ').title()
                    
                    if 'spec' in data:
                        merged_data[clean_name] = data['spec']
                    else:
                        merged_data[clean_name] = data
                        
                    print(f"SUCCESS: {file} successfully added to '{clean_name}'.")
            except Exception as e:
                print(f"ERROR: Error reading {file}: {e}")
                
    with open('specs/full_spec.yaml', 'w', encoding='utf-8') as f:
        # sort_keys=False keeps the clean order of the blocks
        yaml.dump(merged_data, f, allow_unicode=True, sort_keys=False)
        
    print(f"SUCCESS: specs/full_spec.yaml generated successfully! ({len(files)} modules merged)")

if __name__ == '__main__':
    merge_specs()
