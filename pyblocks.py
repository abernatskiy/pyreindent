from pathlib import Path
from copy import copy
import re

def stripTrailingNewlines(line):
	if len(line)>0 and line[-1]=='\n':
		line = line[:-1]
	return line

def strinTrailingTabsAndSpaces(line):
	return re.sub(r'[\t ]*$', '', line)

def quoteStatus(origLine, curQuote, substituteWith='__stringLiteral__', replaceCommentsWith='__comment__'):
	'''Checks whether a line of Python code opens or closes a string literal and
	   provides the edited version of the string with all literal definitions
	   replaced by a placeholder. Optionally, also replaces comments (enabled
	   by default).

	   Parameters
	   ----------
	   origLine : str
	       Line of code to analyze.
	   curQuote : str or None
	       A literal of the currently open quote or None if no quotes are currently open.
	   substituteWith : str
	       Placeholder that the string literal will be replaced with. Must not contain any quotes or brackets.
	   replaceCommentsWith : str or None
	       String to replace comments with or None if no replacement is needed.

	   Returns
	   -------
	   line : str
	       The line of code with all string literal definitions replaced by the placeholder.
	   remainingQuote : str or None
	       Updated value of curQuote.
	       If there was no multiline literal open above according to curQuote and
	       the line contained a beginning of a multiline string literal, the
	       quote that was opened will be returned. If there was a multiline
	       literal open and the line closed it, None will be returned. If all
	       string literal definitions made on the line were closed or none
	       were made, None will be returned.
	'''
	possibleQuotes = ['"', "'"]
	outSubstrs = []
	line = copy(origLine)
	while len(line) > 0:
		#print(f'{curQuote} : {line}')
		if curQuote:
			before, sep, after = line.partition(curQuote)
			if sep == '' and after == '':
				line = ''
			else:
				line = after
				curQuote = None
			outSubstrs.append(substituteWith)
		else:
			#print(f'Looking for new quotes in line {line}')
			quoteTypes = ['"""', "'''", '"', "'"]
			quotePos = [ line.find(qt) for qt in quoteTypes ]
			closestQuotePos = min([ qp for qp in quotePos if qp>=0 ], default=-1)

			commentPos = line.find('#')
			if commentPos >=0 and (closestQuotePos == -1 or closestQuotePos > commentPos):
				if replaceCommentsWith:
					outSubstrs.append(line[:commentPos])
					outSubstrs.append(replaceCommentsWith)
				else:
					outSubstrs.append(line)
				line = ''
			elif closestQuotePos >= 0:
				quote = quoteTypes[quotePos.index(closestQuotePos)]
				before, sep, after = line.partition(quote)
				outSubstrs.append(before)
				if len(after) == 0:
					outSubstrs.append(substituteWith)
				curQuote = quote
				line = after
			else:
				outSubstrs.append(line)
				line = ''
			#print(f'After the search: line {line}, substrings {outSubstrs}')
	if curQuote and not (curQuote == '"""' or curQuote == "'''"):
		raise ValueError(f'Single quote {curQuote} not closed on line {origLine}')
	return ''.join(outSubstrs), curQuote

def bracesStatus(line, curBraces):
	braces = [ ('(', ')'), ('[', ']'), ('{', '}') ]
	curBrCounts = { obr: line.count(obr)-line.count(cbr) for obr, cbr in braces }
	if all([ val==0 for val in curBrCounts.values() ]):
		return curBraces
	else:
		updatedBrStatus = curBrCounts if curBraces is None else { obr: bc + curBrCounts[obr] for obr, bc in curBraces.items() }
		return None if all([val==0 for val in updatedBrStatus.values() ]) else updatedBrStatus

def lineWrapped(line):
	'''Assumes that any trailing spaces or tabs are taken care of'''
	return False if len(line)<1 else line[-1]=='\\'

def splitIntoBlocks(file):
	block = []
	curBraces = None
	curQuote = None
	for line in file:
#		print(f'{curBraces}, {curQuote}: {line}')
		line = stripTrailingNewlines(line)
		block.append(line)

		noslline, curQuote = quoteStatus(line, curQuote)
#		print(f'{curBraces}, {curQuote}: {noslline}')
		curBraces = bracesStatus(noslline, curBraces)
		if curQuote or curBraces:
			continue
		else:
			yield block
			block.clear()
	if curBraces:
		raise ValueError(f'Infinite block found: the code is syntactically incorrect (remaining braces {curBraces})')
	if curQuote:
		raise ValueError(f'Infinite block found: the code is syntactically incorrect (remaining quotes {curQuotes})')


sourceDir = Path('./generative-query-network-pytorch')

for pyfilename in sourceDir.rglob('*.py'):
	print(f'================ WORKING ON {pyfilename} ====================')
	with open(pyfilename, 'r') as pyfile:
		try:
			for block in splitIntoBlocks(pyfile):
				print('\n'.join(block))
				print('----------------')
		except ValueError as verr:
			raise ValueError(f'while processing file {pyfilename}:\n{verr}')
	print('\n\n\n')
#	break
