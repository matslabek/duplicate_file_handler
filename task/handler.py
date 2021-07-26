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
        for root, dirs, files in os.walk(args.root_directory, topdown=True):
            for name in files:
                print(os.path.join(root, name))




