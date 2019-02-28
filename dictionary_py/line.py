import time

class Line:
	verbose=-1
	rude=-1 #Will simply return empty string if an error occurs
	def __init__(self, line, sChar='<', eChar='>'):
		self.sChar=sChar
		self.eChar=eChar
		self.originalLine=line
		self.line=line.strip()
		self.count=0
		self.inTag=False

	def __str__(self):
		return(self.line.strip())

	def stripLine(self):
	#Error tag: S
		"""
		Removes all tags from a line.
		Nested tags and multi-line tags will also be removed.
		"""
		line=self.line
		x=line.find(self.sChar)
		y=line.find(self.eChar)
		v('sChar={}\teChar={}'.format(self.sChar, self.eChar))

		while True:
			#time.sleep(1)
			self.count+=1

			#Prevent infinite looping, break if count==5
			if self.count>=10:
				v('Someting went wrong! Returning a null line')
				self.line=''
				self.count=0
				break

			v('Top again!')
			v('Count: {}'.format(self.count))
			preStrip=self.line #Save the line before stripping
			line=preStrip.strip('\n\t ')

			if self.inTag:
				v(self.warning("In a Tag!"))
				v("\t{}".format(line))
				x=self.line.find(self.sChar)
				y=self.line.find(self.eChar)
				v("\tx: {}\ty: {}".format(x, y))

				#If a closing bracket is found, continue outside of a tag
				if y<x or y>=0 and x==-1:
					self.inTag=False
					line=line[y+1:]
					v(self.warning("Leaving tag!", 'S'))
					continue

				#If not brackets are found, or you can't find a closing bracket,
				#return a blank line
				else:
					self.line=''
					self.count=0
					break

			if x>=0:
				line=line[:x]+line[y+1:]
				self.line=line.strip('\n\t ')
				self.count=0
			elif x*y==1:
				self.count=0
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
					self.count=0
					break

				line=self.line #Before all checking
				v(self.warning('Break Found!'))

				#if checkNestedTag failed (both result and given line are the same)
				#then try checking for an open tag
				result, res=self.checkNestedTag(preStrip)
				if result==preStrip:
					result, returnType=self.checkOpenTag(line)
					#Essentially if not tags are left, return the result
					if result.find(self.sChar)*result.find(self.eChar)==1:
						v(self.warning("Premature returning of result!", "S"))
						self.line=result
						self.count=0
						if returnType=='C':
							self.inTag=False
						elif returnType=='O':
							self.inTag=True
						break

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
					self.count=0


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
					self.count=0
					continue
				v("Uhhh... {}".format(result==line))

		return(self.line.strip())

	def checkNestedTag(self, line):
		returnType='N'
		#Error tag: N
		"""
		Checks for nested tags (ex: <!-- <> -->) and tries to remove them.
		Returns the line after the nested tag is removed
		"""
		x=line.find(self.sChar)
		y=line.find(self.eChar)
		yOut=line.find(self.eChar, y+1)
		xOut=line.find(self.sChar, y+1) #if y==-1, xOut==x
		v("\tNested!\n\tLine: {}".format(line))
		v("\tx: {}\ty: {}\txOut: {}\tyOut: {}".format(x, y, xOut, yOut))

		#If any closing tag is found, after the first found, without an open tag
		#then move y to outter closing tag, then strip the tag
		#if yOut>=0 and x<y or yOut>=0 and xOut>yOut or yOut>=0 and xOut==-1:
		if not x<y<xOut<yOut and (yOut>=0 and x<y or yOut>=0 and (xOut>yOut or xOut==-1)):
			v(self.warning('Found yOut!', 'N'))
			y=yOut+1
			result=line[:x]+line[y:]
			returnType='Y'

		#If no yOut is found, assume open tag (multi-line)
		else:
			v(self.warning('Could not find an embedded tag (probably open tag)!', 'N'))
			result=line
			returnType='N'

		if result==line:
			v(self.error('No Changes Made!', 'N'))

		v('\tResult:\t{}\n\tOrig:\t{}'.format(result, line))
		return([result, returnType])

	def checkOpenTag(self, line):
		"""
		Checks for open ended tags '<', '>', etc... and removes them
		Returns a list with the fixed line and the type of tag found:
			-N = No changes made
			-O = Open tag found
			-C = Close tag found
		"""
		#Error tag: O
		pre=line #Saves line before checking
		result=line
		returnType='N'
		v(self.warning('Checking for open tag...', 'O'))
		v("\t{}".format(line))

		#Check open
		x=line.rfind(self.sChar)
		y=line.rfind(self.eChar)
		v("\txR: {}\tyR: {}".format(x, y))
		if x>=0 and y==-1 or x>y and y!=-1:
			v("\t{}".format(self.warning("Found opening tag!", "O")))
			result=line[:x]
			returnType='O'
			v(self.warning("RESULT: {}".format(result), 'O'))
			v(self.warning("ORIGINAL: {}".format(pre), 'O'))
			return([result, returnType])
		#Check close
		x=line.find(self.sChar)
		y=line.find(self.eChar)
		v("\tx: {}\ty: {}".format(x, y))
		if y>=0 and x==-1 or y>=0 and y<x:
			v("\t{}".format(self.warning("Found closing tag!", "O")))
			result=line[y+1:]
			self.inTag=False
			returnType='C'
			v(self.warning("RESULT: {}".format(result), 'O'))
			v(self.warning("ORIGINAL: {}".format(pre), 'O'))
			return([result, returnType])


		v(self.warning("RESULT: {}".format(result), 'O'))
		v(self.warning("ORIGINAL: {}".format(pre), 'O'))
		return([result, returnType])

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

	def getSChar(self):
		return(self.sChar)

	def getEChar(self):
		return(self.eChar)

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
