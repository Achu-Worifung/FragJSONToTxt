import json_repair
import os
import re

# get the name of all json files
def get_path():
    root = "./SongBooks"
    json_files = [] #store all json files 
    
    # Traverse the directory
    for foldername, subfolders, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".json"):
                # getting the file name
                json_files.append( filename)
    return json_files

def write_to_file(path, title, text):
    
    title = re.sub(r'[<>:"/\\|?*]', '_', title)  # removing invalid characters
    title = title.replace('\n', ' ').replace('\r', '')  # Remove newlines and carriage returns
    text = re.sub(r'<[^>]+>', '', text) #removing tags
    
    path = path.replace('.json', '')  # removing the .json extension from path (if present)
    
    # Ensure the directory exists
    os.makedirs(path, exist_ok=True)

    # Define the base file name with the .txt extension
    base_file_name = os.path.join(path, f"{title}.txt")
    
    # Check if the file exists and handle naming with a number suffix if needed
    if os.path.exists(base_file_name):
        for i in range(1, 100):
            new_file_name = os.path.join(path, f"{title}({i}).txt")
            if not os.path.exists(new_file_name):
                # Create and write to the new file with the numbered suffix
                with open(new_file_name, 'w', encoding='utf-8') as f:
                    f.write(text)
                break
    else:
        # File does not exist, create and write to it
        with open(base_file_name, 'w', encoding='utf-8') as f:
            f.write(text)
       

def read_json(path):
    file_path = "./SongBooks/" + path
    # Reading the JSON data file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Fixing and decoding the JSON data
    decoded_object = json_repair.loads(data)


    words_to_remove = ['Chorus:', 'Bridge:', 'Interlude','<b>','</b>' , 'Verse 1']
    for song in decoded_object['Songs']:
        

        # getting the song title
        song_title = song['Text']
        
        print(f'\n song title: {song_title}\n')
        
        song_lines = ''
        # iterating throgh the song verses

        
        for verse in song['Verses']:
            
            # ids to determine if different verse or not
            prev_id = 0
            
            if 'ID' in verse:
                # getting the id
                curr_id = verse['ID']
                
                if "Text" in verse: #check if text is not empty
                    currText = verse['Text']
                    currText = currText.rstrip() #removing trailing white spaces
                    # sanitizing the text(remove unwanted words)
                    for rmText in words_to_remove:
                        currText = currText.replace(rmText, '')
                    
                    
                    if curr_id != prev_id:
                    
                        print(f'\n{currText}')
                        song_lines = song_lines + f'\n\n{currText}'
                        prev_id = curr_id
                    else:
                        print(f'{currText}')
                        song_lines+= f'{currText}'
            else: #if no id is present
                if "Text" in verse:
                    currText = verse['Text']
                    for rmText in words_to_remove:
                        currText = currText.replace(rmText, '')
                    print(f'{currText}')
                    song_lines+= currText
        write_to_file(path,song_title, song_lines)
        
        
paths = get_path()
#converting json files to txt files
for path in paths:
    read_json(path)

print("Conversion completed")