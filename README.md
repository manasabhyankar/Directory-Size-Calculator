# Directory-Size-Calculator
A simple utility script that walks a directory tree and calculates the sizes of files within subdirectories and assesses their age.

**Sample usage:**

`D:\python>python file_sizes.py C:\Eclipse D:\output\output.csv`

## Notes:

1. Make sure Python is added to your PATH. Start with "python", add the name of the .py (*file_sizes.py*) file, then add the target directory (in this case I used "C:\Eclipse" from my local disk).

2. Additionally, you will need to specify a destination directory for the .csv file output. I used *D:\output\output.csv* for this example.

## TODO:**

1. Separate **csv** output stream to its own function for readability.
2. Clean up print statements scattered through code.
3. Potentially add support for multiple target_path inputs.
4. Change time calculation for *file_helper*.
5. At some point, release Linux variant.
