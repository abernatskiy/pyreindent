#!/usr/bin/env python3

from pathlib import Path
import pyblocks
import shutil

def reindentFile(filePath, inTabSymbol, outTabSymbol, cleanTrailingTabsAndSpaces=False, backupSuffix=None):
	newBlocks = []
	with open(filePath, 'r') as pyfile:
		try:
			for block in pyblocks.splitIntoBlocks(pyfile, cleanTrailingTabsAndSpaces=cleanTrailingTabsAndSpaces):
				newBlocks.append(pyblocks.reindentBlock(block, inTabSymbol, outTabSymbol))
		except ValueError as verr:
			raise ValueError(f'while processing file {filePath}:\n{verr}')
	if backupSuffix:
		shutil.move(filePath, str(filePath) + backupSuffix)
	with open(filePath, 'w') as pyfile:
		for line in sum(newBlocks, []):
			pyfile.write(line + '\n')

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Freely switch between Python indentation styles')

	parser.add_argument('-o', '--output', type=str, default=None, metavar='output_file',
	                    help='Output file name. Default: overwrite the original file(s)')
	parser.add_argument('-b', '--backup-postfix', type=str, default='~', metavar='postfix',
	                    help='Back up unmodified input file(s) under their original name(s) with ' \
	                         'this postfix. Set to empty string to suppress backups. Default: ~')
	parser.add_argument('-r', '--recursive', action='store_true',
	                    help='Recursively find all .py files in the input path and convert them')
	parser.add_argument('-rt', '--remove-trailing', action='store_true',
	                    help='Remove any trailing tabs or spaces, leaving multiline string literals intact')

	parser.add_argument('input_path', type=str,
	                    help='Input path')

	req_grp = parser.add_argument_group(title='required flags')
	req_grp.add_argument('-f', '--from-tabs', choices=['hard', 'soft4', 'soft2'], required=True,
	                    help='Style of indentation to convert from')
	req_grp.add_argument('-t', '--to-tabs', choices=['hard', 'soft4', 'soft2'], required=True,
	                    help='Style of indentation to convert to')

	args = parser.parse_args()

#	sourceDir = Path('../gqn/generative-query-network-pytorch')
#
#	for pyfilename in sourceDir.rglob('*.py'):
#		print(f'================ WORKING ON {pyfilename} ====================')
#		reindentFile(pyfilename, '    ',  '\t', cleanTrailingTabsAndSpaces=True, backupSuffix='~')
#		break
