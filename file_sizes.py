import os, sys, time, csv
from pathlib import Path

def size_conversion(byte_size):
    if(byte_size >= 1000000000000):
        byte_size /= 1000000000000
        return str(round(byte_size, 2)) + 'TB'
    elif(byte_size >= 1000000000):
        byte_size /= 1000000000
        return str(round(byte_size, 2)) + 'GB'
    elif(byte_size >= 1000000):
        byte_size /= 1000000
        return str(round(byte_size, 2)) + 'MB'
    elif(byte_size >= 1000):
        byte_size /= 1000
        return str(round(byte_size, 2)) + 'KB'
    elif(byte_size >= 0):
        return str(byte_size) + 'B'
    

def folder_walker(folder_path):
    directory_data_timeline = {}
    for element in p.iterdir():
        if(element.is_dir() and os.listdir(element)):
            new_p = Path(element)
            directory_data_timeline[str(Path(new_p))] = [0, 0, 0]
            for root, subdir, file in os.walk(new_p):
                for f in file:
                    filepath = Path(root) / Path(f)
                    if((int(time.time()) - 30*86400) < Path(filepath).stat().st_atime):
                        # between 0 - 30 days old
                        directory_data_timeline[str(new_p)][0] += Path(filepath).stat().st_size
                    elif((int(time.time()) - 60*86400) < Path(filepath).stat().st_atime):
                        # between 30 - 60 days old
                        directory_data_timeline[str(new_p)][1] += Path(filepath).stat().st_size
                    elif((int(time.time()) - 60*86400) > Path(filepath).stat().st_atime):
                        # older than 60 days old
                        directory_data_timeline[str(new_p)][2] += Path(filepath).stat().st_size
    return directory_data_timeline

if __name__ == '__main__':
    target_path = sys.argv[1]
    output_dictionary = {}
    if(Path(target_path).exists()):
        p = Path(target_path)
        output_dictionary = folder_walker(p)
        with open('file_output.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Directory Name', 'Files less than 30 days old', 'Files between 30 - 60 days old', 'Files older than 60 days'])
            for key, value in output_dictionary.items():
                main_list = [key]
                val_list = []
                for val in value:
                    val_list.append(size_conversion(val))
                main_list.extend(val_list)
                writer.writerow(main_list)
        csv_file.close()

    else:
        print("That path is not valid!")
    
    
        