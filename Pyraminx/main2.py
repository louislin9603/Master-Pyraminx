#test3
from tkinter import *
import time, ast
from tkinter import messagebox

start_time=time.time()
print("Program Loading... Please Wait...")

total_time=time.time() - start_time
print("Done!  Program Loaded in %s seconds." % str(total_time))

CP_TEXT = False	#if True:  will print working visuals and other text in the Command Prompt.  This may cause slower solve times.

HEIGHT = 500
WIDTH = 800
POINTS = [(32,108,1),(64,108,-1),(96,108,1),(32,162,-1),(64,162,1),(96,162,-1),(224,108,1),(256,108,-1),(288,108,1),(224,162,-1),(256,162,1),(288,162,-1),(416,108,1),(448,108,-1),(480,108,1),(416,162,-1),(448,162,1),(480,162,-1),(224,216,1),(256,216,-1),(288,216,1),(224,270,-1),(256,270,1),(288,270,-1)]
CORNERPOINTS = [(0,162,1),(64,54,1),(128,162,1),(192,162,1),(256,54,1),(320,162,1),(384,162,1),(448,54,1),(512,162,1),(192,216,-1),(256,324,-1),(320,216,-1)]

TvalueArray=['gray','red','blue','green','yellow','black']
Telements = [None]*24
Celements = [None]*12



class GUI:
	def __init__(self, master):
		self.master = master
		master.title("Pyraminx Solver")
		
		self.canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg='white')
		self.canvas.pack()
		
		for i in range(0,len(Telements)):
			Telements[i] = self.canvas.create_polygon(self.getTri(POINTS[i][0]+112,POINTS[i][1]+38,POINTS[i][2]),  fill=TvalueArray[0],outline = 'black', width = 4.0)

		for i in range(0,12):
			Celements[i] = self.canvas.create_polygon(self.getTri(CORNERPOINTS[i][0]+112,CORNERPOINTS[i][1]+38,CORNERPOINTS[i][2]),  fill=TvalueArray[0],outline = 'black', width = 4.0)

		self.label = Label(master, text="Idicate color at purple cursor using values: 'r', 'g', 'b', and 'y'")
		self.label.pack()
		
		self.textBox=Text(master, height=1, width=40)
		self.textBox.bind("<KeyRelease>", self.keydown)
		self.textBox.bind("<Return>", lambda event: self.runSolver(self.retrieve_input()))
		self.textBox.focus()
		self.textBox.pack()
		
		self.buttonCommit=Button(master, height=1, width=10, text="Solve", command=lambda: self.runSolver(self.retrieve_input()))
		self.buttonCommit.pack()
		
		self.buttonInstructions=Button(master, height=1, width=10, text="Instructions", command=lambda: self.getInstructions())
		self.buttonInstructions.pack()

		self.close_button = Button(master, height=1, width=10, text="Close", command=master.quit)
		self.close_button.pack()
		
	def getInstructions(self):
		output = ""
		output += "How To Use:\n\n"
		output += "The program displays an unfolded Pyraminx puzzle.  "
		output += "To enter the puzzle into the program, follow the purple triangle and enter 'r','b','y', or 'g' in the indicated space.  "
		output += "If you're familiar with the solution of the Pyraminx then you know that the corner pieces stay out of the way and can be solved with a simple turn.  Therefore, double-layer-turns will play the main role in the solution and so the solver will not require you enter the colors of those pieces.\n\n"
		output += "How Solving Works:\n\n"
		output += "After entering your scrambled puzzle, you can press 'Solve' and the program will display a pop-up window.  "
		output += "Steps will be in the form:  'Turn RGB side clockwise'.  "
		output += "In this example, it means to turn the Red, Green, and Blue corner two layers deep in the clockwise direction.  The final move of any solve will be to orient the trivial corner pieces.\n\n"
		messagebox.showinfo(title = "Welcome to Rob's Pyraminx Solver!!", message = output)

	def keydown(self, e):
		self.recolorize()
	
	def getTri(self,x,y,orient): 
		if(orient == 1):
			return [x, y+50, x+58, y+50, x+29, y]
		elif(orient == -1):
			return [x, y, x+58, y, x+29, y+50]
		
	def retrieve_input(self):
		inputValue=self.textBox.get("1.0","end-1c").strip()
		return inputValue.upper()
	
	def getColorNum(self, input):
		if (input.lower() == 'r'):
			return 1
		elif (input.lower() == 'b'):
			return 2
		elif (input.lower() == 'g'):
			return 3
		elif (input.lower() == 'y'):
			return 4
		else:
			return 5
			
	def recolorize(self):
		colorCode=self.textBox.get("1.0","end-1c")
		colorList = list(colorCode)[:24]
		for i in range(0,len(colorList)):
			self.canvas.itemconfigure(Telements[i], fill=TvalueArray[self.getColorNum(colorList[i])])
		for j in range(len(colorList), 24):
			self.canvas.itemconfigure(Telements[j], fill=TvalueArray[0])
		for k in range(0,24):
			if (k == len(colorList)):
				self.canvas.itemconfigure(Telements[k], outline = 'purple', width = 5.0)
			else:
				self.canvas.itemconfigure(Telements[k], outline = 'black', width = 4.0)
	
	def runSolver(self, cubeCode):
		if (not self.checkLegal(cubeCode)):
			messagebox.showinfo(title ="Error!", message = "Not a Legal Cube!\nPlease check your input.")
			
		else:
			start_time=time.time()
			moveList = "x x x x x x x x x x x".split()
			isSolved=False
			
			trySolved = self.tryMoveList(cubeCode,moveList)
			if (self.checkSolved(trySolved)):
				if(CP_TEXT):
					print("Already Solved!")
				isSolved=True
			else:
				tryCount = 0
				if(CP_TEXT):
					print("Calculating...")
				for tryMe in solveDictionary:
					tryCount += 1
					if(CP_TEXT):
						print("Testing solution %s / 933120 :  %s" % (str(tryCount), str(tryMe)))
					trySolved = self.tryMoveList(cubeCode,tryMe)
					if(self.checkSolved(trySolved)):
						isSolved=True
						moveList = tryMe
						if(CP_TEXT):
							print("Solution Found!\n")
						break
			total_time=time.time() - start_time
			print("Calculation time: %s seconds." % str(total_time))
			
			if(isSolved):
				topStr=trySolved[13]+trySolved[7]+trySolved[1]
				leftStr=trySolved[5]+trySolved[9]+trySolved[18]
				rightStr=trySolved[11]+trySolved[15]+trySolved[20]
				backStr=trySolved[3]+trySolved[22]+trySolved[17]

				self.displayDirections(moveList,topStr,leftStr,rightStr,backStr)
			else:
				if(CP_TEXT):
					print("No solution found!")
				messagebox.showinfo(title ="Error", message = "This puzzle seems to be impossible...\nPlease check your input.")
			
		return 'break'
		
	def checkLegal(self, cubeCode):
		legal=False
		if(cubeCode.count('R') == 6 and cubeCode.count('G') == 6 and cubeCode.count('B') == 6 and cubeCode.count('Y') == 6 and len(cubeCode)== 24):
			legal=True
		return legal
		
	def tryMoveList(self, unsolvedCube, moves):
		CA=list(unsolvedCube)
		for step in reversed(moves):	#do moves in reverse
			if (step == 'U'):  #if u2, do u translation
				CA[0],CA[1],CA[2],CA[6],CA[7],CA[8],CA[12],CA[13],CA[14] = CA[6],CA[7],CA[8],CA[12],CA[13],CA[14],CA[0],CA[1],CA[2]
				continue
			elif (step == 'u'):  #if u, do u2 translation;  and so on...
				CA[6],CA[7],CA[8],CA[12],CA[13],CA[14],CA[0],CA[1],CA[2] = CA[0],CA[1],CA[2],CA[6],CA[7],CA[8],CA[12],CA[13],CA[14]
				continue
			elif (step == 'L'):
				CA[6],CA[9],CA[10],CA[19],CA[18],CA[21],CA[4],CA[5],CA[2] = CA[4],CA[5],CA[2],CA[6],CA[9],CA[10],CA[19],CA[18],CA[21]
				continue
			elif (step == 'l'):
				CA[4],CA[5],CA[2],CA[6],CA[9],CA[10],CA[19],CA[18],CA[21] = CA[6],CA[9],CA[10],CA[19],CA[18],CA[21],CA[4],CA[5],CA[2]
				continue
			elif (step == 'R'):
				CA[10],CA[11],CA[8],CA[12],CA[15],CA[16],CA[23],CA[20],CA[19] = CA[23],CA[20],CA[19],CA[10],CA[11],CA[8],CA[12],CA[15],CA[16]
				continue
			elif (step == 'r'):
				CA[23],CA[20],CA[19],CA[10],CA[11],CA[8],CA[12],CA[15],CA[16] = CA[10],CA[11],CA[8],CA[12],CA[15],CA[16],CA[23],CA[20],CA[19]
				continue
			elif (step == 'B'):
				CA[0],CA[3],CA[4],CA[21],CA[22],CA[23],CA[16],CA[17],CA[14] = CA[16],CA[17],CA[14],CA[0],CA[3],CA[4],CA[21],CA[22],CA[23]
				continue
			elif (step == 'b'):
				CA[16],CA[17],CA[14],CA[0],CA[3],CA[4],CA[21],CA[22],CA[23] = CA[0],CA[3],CA[4],CA[21],CA[22],CA[23],CA[16],CA[17],CA[14]
				continue

		return CA
		
	def checkSolved(self, input):
		solved = False
		
		if(input[1] == input[2]  and input[3] == input[4]  and input[5] == input[0]  and input[1] == input[3]  and input[3] == input[5]):
			if(input[7] == input[8]  and input[9] == input[10]  and input[11] == input[6]  and input[7] == input[9]  and input[9] == input[11]):
				if(input[13] == input[14]  and input[15] == input[16]  and input[17] == input[12]  and input[13] == input[15]  and input[15] == input[17]):
					if(input[19] == input[20]  and input[21] == input[22]  and input[23] == input[18]  and input[19] == input[21]  and input[21] == input[23]):
						solved = True
						
		return solved

	def displayDirections(self, mList, top, left, right, back):
		messagebox.showinfo(title = "Solution Found", message = "Press 'OK' to begin Step-by-step instructions")
		stepNum = 1
		for step in reversed(mList):
			if (step == 'U'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side clockwise\n" % top)
				stepNum += 1				
			elif (step == 'u'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side counter-clockwise\n" % top)
				stepNum += 1				
			elif (step == 'L'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side clockwise\n" % left)
				stepNum += 1				
			elif (step == 'l'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side counter-clockwise\n" % left)
				stepNum += 1				
			elif (step == 'R'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side clockwise\n" % right)
				stepNum += 1				
			elif (step == 'r'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side counter-clockwise\n" % right)
				stepNum += 1				
			elif (step == 'B'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side clockwise\n" % back)
				stepNum += 1				
			elif (step == 'b'):
				messagebox.showinfo(title ="Step " + str(stepNum), message = "> turn %s side counter-clockwise\n" % back)
				stepNum += 1				
		messagebox.showinfo(title ="Step " + str(stepNum), message = "> fix any unsolved corner tips")

	
root = Tk()
root.resizable(0,0)
my_gui = GUI(root)
my_gui.recolorize()
root.mainloop()

print("Program Closed.")