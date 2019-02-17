import time

class Line:
	verbose=-1
	rude=-1 #Will simply return empty string if an error occurs
	def __init__(self, line, sChar='<', eChar='>'):
		self.sChar=sChar
		self.eChar=eChar
		self.originalLine=line
		self.line=line.strip('\n\t ')

	def __str__(self):
		return(self.line)

	def stripLine(self):
	#Error tag: S
		"""
		Removes all tags from a line.
		Nested tags and multi-line tags will also be removed.
		"""
		line=self.line
		x=line.find(self.sChar)
		y=line.find(self.eChar)

		while True:
			#time.sleep(1)
			v('Top again!')
			preStrip=self.line #Save the line before stripping
			line=preStrip.strip('\n\t ')

			if x>=0:
				line=line[:x]+line[y+1:]
				self.line=line.strip('\n\t ')
				count=0
			elif x*y==1:
				break
			else:
				v(self.error(loc='-'))

			x=self.line.find(self.sChar)
			y=self.line.find(self.eChar)

			#Check for break
			v('Line: {}'.format(self.line))
			v('x: {}\ty: {}'.format(x, y))
			if y<x or y==-1 and x>=0 or x==-1 and y>=0:
				if Line.rude==1:
					self.line=''
					break

				line=self.line #Before all checking
				v(self.warning('Break Found!'))

				#if checkNestedTag failed (both result and given line are the same)
				#then try checking for an open tag
				result=self.checkNestedTag(preStrip)
				if result==preStrip:
					result=self.checkOpenTag(preStrip)
					v('{}\t<-- Check result\n{}\t<-- Line before check'.format(result, line))
				else:
					v('{}\t<-- Check result\n{}\t<-- Line before check'.format(result, line))
				#Checks if both nested and multi check worked.
				#If so, continue stripping
				v('Checking for similarity...')
				v('{}\t<-- Check result\n{}\t<-- Line before check'.format(result, line))
				if result!=line:
					v(self.warning('Changing line to result!'))
					self.line=result.strip('\n\t ')
					v("NewLine: {}".format(self.line))
					#Refind x and y
					x=self.line.find(self.sChar)
					y=self.line.find(self.eChar)
					v("New x&y: {}, {}".format(x, y))
					count=0

				#If all checks failed, return line as blank
				elif result==line:
					v("Breaking!")
					v(self.error())
					self.line=''
					break

				#If we get to this point, it means the checks were a success,
				#so keep stripping
				else:
					v("Continuing!")
					continue
				v("Uhhh... {}".format(result==line))

		return(self.line)

	def checkNestedTag(self, line):
		#Error tag: N
		"""
		Checks for nested tags (ex: <!-- <> -->) and tries to remove them.
		Returns the line after the nested tag is removed
		"""
		x=line.find('<')
		y=line.find('>')
		yOut=line[y+1:].find('>')
		xOut=line[y+1:].find('<') #if y==-1, xOut==x
		v("\tNested!\n\tLine: {}".format(line))
		v("\tx: {}\ty: {}\txOut: {}\tyOut: {}".format(x, y, xOut, yOut))

		#If any closing tag is found, after the first found, without an open tag
		#then move y to outter closing tag, then strip the tag
		if yOut>=0:
			v(self.warning('Found yOut!', 'N'))
			y+=yOut+1
			result=line[:x]+line[y+1:]

		#If no yOut is found, assume open tag (multi-line)
		elif yOut==-1:
			v(self.warning('Could not find an embedded tag (probably open tag)!', 'N'))
			result=line

		if result==line:
			v(self.error('No Changes Made!', 'N'))

		v('\tResult:\t{}\n\tOrig:\t{}'.format(result, line))
		return(result)

	def checkOpenTag(self, line):
		pre=line #Saves line before checking

		#Check open
		x=line.find('<')
		y=line.find('>')
		if y<x or y>=0 and x==-1:
			result=line[y+1:]

		#Check close
		x=line.rfind('<')
		y=line.rfind('>')
		if y<x or y==-1:
			result=line[:x]

		v("RESULT: {}".format(result))
		return(result)

	def getLine(self):
		"""Gets the line"""
		return(self.line)

	def setLine(self, newLine):
		"""Sets the line"""
		self.line=newLine.strip('\n\t ')
		self.originalLine=self.line

	def setSChar(self, newS):
		self.sChar=newS

	def setEChar(self, newE):
		self.eChar=newE

	def toggleRude(self):
		"""If rude is on, will simply delete invalid lines (lines with open tags)"""
		self.rude*=-1

	def toggleVerbose():
		"""If verbose is on, wil print extra debug messages"""
		Line.verbose*=-1
		print("Verbose: {}".format(Line.verbose==1))

	def error(self, message='Unknown Error!', loc='S'):
		return('\033[31m[|X]({})\033[0m Error: {}'.format(loc, message))

	def warning(self, message='Unknown Warning!', loc='S'):
		return('\033[93m[|X]({})\033[0m Warning: {}'.format(loc, message))

def v(*args, **kwargs):
	if Line.verbose==1:
		print(*args, **kwargs)

def main():
	x=Line("Hello<")
	Line.toggleVerbose()
	x.stripLine()

if __name__=='__main__':
	main()
