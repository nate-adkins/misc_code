import os
from PIL import Image
import pyheif

folder_path = '.'

if not os.path.isdir(folder_path):
    print(f"The folder path {folder_path} does not exist.")
else:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.lower().endswith(('.jpg', '.jpeg', '.heic', '.bmp', '.gif', '.tiff')):
            try:
                if filename.lower().endswith('.heic'):
                    # Open HEIC file using pyheif
                    heif_file = pyheif.read(file_path)
                    img = Image.frombytes(
                        heif_file.mode, 
                        heif_file.size, 
                        heif_file.data
                    )
                else:
                    img = Image.open(file_path)
                
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(folder_path, f'{base_name}.png')
                
                img.save(output_path, 'PNG')
                print(f'Converted {filename} to {base_name}.png')

                os.remove(file_path)
                print(f'Deleted {filename}')

            except Exception as e:
                print(f"Error processing {filename}: {e}")
