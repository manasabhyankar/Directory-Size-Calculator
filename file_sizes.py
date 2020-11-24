import os, sys, time, csv
from pathlib import Path
from multiprocessing import Process, Queue

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
    
def file_helper(element, q):
    new_p = Path(element)
    d = {}
    d[str(Path(new_p))] = [0, 0, 0]
    for root, subdir, file in os.walk(new_p):
        for f in file:
            filepath = Path(root) / Path(f)
            if((int(time.time()) - 30*86400) < Path(filepath).stat().st_atime):
                # between 0 - 30 days old
                d[str(new_p)][0] += Path(filepath).stat().st_size
            elif((int(time.time()) - 60*86400) < Path(filepath).stat().st_atime):
                # between 30 - 60 days old
                d[str(new_p)][1] += Path(filepath).stat().st_size
            elif((int(time.time()) - 60*86400) > Path(filepath).stat().st_atime):
                # older than 60 days old
                d[str(new_p)][2] += Path(filepath).stat().st_size
    q.put(d)

def folder_walker(folder_path):
    directory_data_timeline = {}
    main_path = Path(folder_path)
    q = Queue()
    jobs = []
    for element in main_path.iterdir():
        p = Process(target=file_helper, args=(element, q))
        if(element.is_dir() and os.listdir(element)):
            jobs.append(p)
            p.start()
    for proc in jobs:
        ret = q.get()
        directory_data_timeline.update(ret)
    for proc in jobs:
        proc.join()
    return directory_data_timeline

if __name__ == '__main__':
    if(len(sys.argv) <= 2):
        print("You are missing 1 or more arguments. Expecting a target and destination path.")
        quit()
    
    target_path = sys.argv[1]
    destination_path = sys.argv[2]
    output_dictionary = {}

    # If the destination path doesn't exist, make it.
    if(not Path(destination_path).parent.exists()):
        Path(destination_path).parent.mkdir()
    # If the supplied target path doesn't exist, quit the program and alert the user.
    if(not Path(target_path).exists()):
        print("That target path is not valid!")
        quit()
    # If we reach here, then the target SHOULD exist and the script will be valid to run.
    print("Target Path: " + target_path)
    print("Destination Path: " + destination_path)
    p = Path(target_path)
    output_dictionary = folder_walker(p)
    
    with open(destination_path, 'w') as csv_file:
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
    print(destination_path.split('\\')[2] + " was created at " + destination_path)