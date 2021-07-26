import argparse
import os
import sys
if __name__ == "__main__":

    args = sys.argv

    if len(args) <= 1:
        print("Directory is not specified")
    else:
        parser = argparse.ArgumentParser(description="Duplicate File Handler... \
             Enter root directory path")
        parser.add_argument("root_directory", default="", help="You should enter absolute root path")
        args = parser.parse_args()

        file_format = input("Enter file format:\n")

        files_list = []

        files_dict = dict()

        for root, dirs, files in os.walk(args.root_directory, topdown=True):
            for name in files:
                file_name, file_extension = os.path.splitext(os.path.join(root, name))
                if not file_format:
                    files_list.append(file_name + file_extension)
                elif file_extension == file_format:
                    files_list.append(file_name + file_extension)

        """Update dictionary with duplicate files"""
        for filepath in files_list:
            try:
                filesize = os.path.getsize(filepath)
                if filesize not in files_dict:
                    files_dict[filesize] = []
                    files_dict[filesize].append(filepath)
                else:
                    files_dict[filesize].append(filepath)
            except OSError:
                print("File does not exist or is inaccesible")

        print("\nSize sorting options:\n"
                                   "1. Descending\n"
                                   "2. Ascending\n\n")
        while True:
            sorting_option = input("Enter a sorting option:\n")
            rvrsd = False
            if sorting_option == "1" or sorting_option == "2":
                if sorting_option == "1":
                    rvrsd = True
                for file_bytes in sorted(files_dict.keys(), reverse=rvrsd):
                    print(file_bytes, "bytes")
                    for filepath in files_dict[file_bytes]:
                        print(filepath)
                    print("\n")
                break
            else:
                print("Wrong option")



