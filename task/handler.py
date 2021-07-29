import argparse
import os
import sys
import hashlib

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

        files_bytes = []  # list of sorted file bytes
        rvrsd = False

        while True:
            sorting_option = input("Enter a sorting option:\n")
            if sorting_option == "1" or sorting_option == "2":
                if sorting_option == "1":
                    rvrsd = True
                for file_bytes in sorted(files_dict.keys(), reverse=rvrsd):
                    files_bytes.append(file_bytes)
                    print(file_bytes, "bytes")
                    for filepath in files_dict[file_bytes]:
                        print(filepath)
                    print("\n")
                break
            else:
                print("Wrong option")

        hashes_dict = {}    #has structure of: {bytes: { hash: [filepath1, filepath2... ] } }
        duplicates_list = []  # list of tuples (hash, filepath) where index is the identifying number,
        # for the next stage

        BUF_SIZE = 65536
        line_number = 1

        while True:
            duplicates_check = input("Check for duplicates?\n")
            if duplicates_check == "yes":
                for file_bytes in files_bytes:
                    hashes_dict[file_bytes] = {}
                    print("\n", file_bytes, "bytes")
                    for filepath in files_dict[file_bytes]:
                        hash_alg = hashlib.md5()
                        with open(filepath, "rb") as file:
                            while True:
                                data = file.read(BUF_SIZE)
                                if not data:
                                    break
                                hash_alg.update(data)
                        hash_digest = hash_alg.hexdigest()
                        if hash_digest not in hashes_dict[file_bytes]:
                            hashes_dict[file_bytes][hash_digest] = []
                        hashes_dict[file_bytes][hash_digest].append(filepath)
                    for hash_alg_digest in sorted(hashes_dict[file_bytes].keys(), reverse=rvrsd):
                        if len(hashes_dict[file_bytes][hash_alg_digest]) > 1:
                            print("Hash:", hash_alg_digest)
                            for file_path in hashes_dict[file_bytes][hash_alg_digest]:
                                print(str(line_number) + ".", file_path)
                                line_number += 1
                                duplicates_list.append((hash_alg_digest, file_path))
                break
            elif duplicates_check == "no":
                break
            else:
                print("Wrong option")
