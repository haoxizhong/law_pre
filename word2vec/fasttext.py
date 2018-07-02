import argparse
import os
import fasttext

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o')
parser.add_argument('--input', '-i')
args = parser.parse_args()

input_file_path = args.input
output_file_path = args.output

os.makedirs(output_file_path, exist_ok=True)

model = fasttext.skipgram(input_file_path,output_file_path)
