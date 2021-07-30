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
                if file_format == " " or not file_format:
                    files_list.append(file_name + file_extension)
                elif file_extension[1:] == file_format:
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
        duplicates_list = []  # list of tuples (hash, filepath, bytes) where index is the identifying number,
        # for the next stage

        BUF_SIZE = 65536
        line_number = 1

        while True:
            """List duplicate files"""
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
                                duplicates_list.append((hash_alg_digest, file_path, file_bytes))
                while True:
                    """Delete chosen duplicate files"""
                    delete_check = input("Delete files?")
                    if delete_check == "yes":
                        freed_space = 0
                        while True:
                            print("Duplicates list", duplicates_list)
                            files_to_delete = input("Enter files to delete (numbers, separated with space):")
                            print(files_to_delete)
                            if not files_to_delete:
                                print("Wrong format")
                                continue
                            try:
                                files_deleted = list(map(int, files_to_delete.split()))
                                for file_numb in files_deleted:
                                    if file_numb > len(duplicates_list):
                                        print("Wrong format")
                                        break
                                for file_numb in files_deleted:
                                    os.remove(duplicates_list[file_numb - 1][1])
                                    freed_space += duplicates_list[file_numb - 1][2]
                                print("Total freed up space:", freed_space, "bytes")
                                break
                            except (ValueError, TypeError):
                                print("Wrong format")
                    elif delete_check == "no":
                        break
                    else:
                        print("Wrong option")
                        continue
                    break
                break
            elif duplicates_check == "no":
                break
            else:
                print("Wrong option")
