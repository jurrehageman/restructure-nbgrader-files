#!/usr/bin/env python3
"""
Name: structure_files.py
Purpose: restructure file/path stucture for NB grader.
Author: Jurre Hageman
Created: 2020-01-24
Updated: NA
"""

# Imports
import os
import shutil
import sys
import argparse
import itertools


def args():
    "parses command line arguments"
    parser = argparse.ArgumentParser(description="restructures files")
    parser.add_argument("in_dir", help="the path to the directory with the input")
    parser.add_argument("test_name", help="the name of the test")
    parser.add_argument("jupyter_name", help="the name of the jupyter notebook (without file-extension)")
    args = parser.parse_args()
    return args


def peek_generator_object(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)


def write_files(src, dst):
    dstfolder = os.path.dirname(dst)
    if not os.path.exists(dstfolder):
        os.makedirs(dstfolder)
        shutil.copy(src, dst)


def recreate_dir_structure(in_dir, test_name, jupyter_name):
    students = []
    dst_file_name = jupyter_name + '.ipynb'
    subfolders = os.walk(in_dir)
    has_content = peek_generator_object(subfolders)
    if not has_content:
        print("Dir does not exist or no subfolders found")
        return
    for subfolder in subfolders:
        st_num = subfolder[0].split('_')[-1]
        submission = subfolder[0]
        print("Processing submission:", submission)
        if st_num in students:
            print("Double submission detected for student: {}. Folder {} skipped.".format(st_num, submission))
            continue
        else:
            students.append(st_num)
        files = subfolder[-1]
        non_hidden_files = [i for i in files if not i.startswith(".")]
        if len(non_hidden_files) > 1:
            print("Multiple files detected for submission: {}. Folder {} skipped.".format(submission, submission))
            continue
        else:
            if files[0].endswith('.ipynb'):
                file_name = files[0]
            else:
                print("Other filetype ({}) found for submission: {}. Folder {} skipped.".format(files[0], submission, submission))
                continue
        src = os.path.join(submission, file_name)
        dst = os.path.join('submitted', st_num, test_name, dst_file_name)
        write_files(src, dst)


def main():
    comm_args = args()
    in_dir = comm_args.in_dir
    test_name = comm_args.test_name
    jupyter_name = comm_args.jupyter_name
    recreate_dir_structure(in_dir, test_name, jupyter_name)
    print("Done...")
    return 0


if __name__ == "__main__":
    sys.exit(main())