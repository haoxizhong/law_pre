import argparse
import os
import fasttext

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o')
parser.add_argument('--input', '-i')
args = parser.parse_args()

input_file_path = args.input
output_file_path = args.output

model = fasttext.skipgram(input_file_path, os.path.join(output_file_path, "model"), dim=200, thread = 12)
