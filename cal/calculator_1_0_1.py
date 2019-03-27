from tkinter import Tk,Frame,StringVar,Label,Button
import math
from decimal import Decimal,getcontext

"""
using class to build the app, 
for maintaince and update purpose

"""

class calculator:

	# all the basic initilizations
	# number buttons
	# operators
	# key bind
	def __init__(self,master):

		########## variable used  ##############
		global numberQue
		# the displayed number is a string!!
		numberQue = '0'

		global display_number
		display_number = StringVar()
		display_number.set('0')

		#store the number and operations
		global numberPool,sign_Pool,acPress
		acPress = 1
		numberPool,sign_Pool = [],[]
		#control the length
		getcontext().prec = 12


		########################## GUI setup ####################

		master.title("Calculator")
		master.resizable(width=False,height=False)
		#gui geometry
		#width x height + 'x' offset + 'y' offset 
		master.geometry("378x315")

		########################## display section ####################

		self.display_frame = Frame(master)
		self.display_frame.config(width=374,height=50)
		self.display_frame.grid(row= 0,column= 0,columnspan= 4)
		# the frame is not shrink with the label
		self.display_frame.pack_propagate(False) 
		# display configurations
		self.display = Label(self.display_frame,textvariable = display_number)
		self.display.configure(anchor= 'e',font=("Helvetica", 40),padx=10)
		self.display.pack(fill='both')
		
		#
		# ################## Buttons setup  ##################
		#

		# AC button
		# pos/neg button
		# percent button
		# decimal button

		self.ac_button = self.buttons(master,'AC',1,0,self.acButton)
		self.neg_button = self.buttons(master,'+/-',1,1,self.negative)
		self.percent_button = self.buttons(master,'%',1,2,self.percentButton)
		self.deci_button = self.buttons(master,'.',5,2,self.decimalButton)

		# operations buttons initialized
		#	
		# divide button
		# multiple button	
		# minus button
		# plus button
		# equal button
		#

		self.divide_button = self.buttons(master,'/',1,3,lambda:self.operations("/"))
		self.mul_button = self.buttons(master,'X',2,3,lambda:self.operations("X"))
		self.minus_button = self.buttons(master,'-',3,3,lambda:self.operations("-"))
		self.plus_button = self.buttons(master,'+',4,3,lambda:self.operations("+"))
		self.equal_button = self.buttons(master,'=',5,3,self.equal)

		# numbers setup
		self.number_7 = self.buttons(master,'7',2,0,lambda: self.numberButton(7))
		self.number_8 = self.buttons(master,'8',2,1,lambda: self.numberButton(8))
		self.number_9 = self.buttons(master,'9',2,2,lambda: self.numberButton(9))

		self.number_4 = self.buttons(master,'4',3,0,lambda: self.numberButton(4))
		self.number_5 = self.buttons(master,'5',3,1,lambda: self.numberButton(5))
		self.number_6 = self.buttons(master,'6',3,2,lambda: self.numberButton(6))

		self.number_1 = self.buttons(master,'1',4,0,lambda: self.numberButton(1))
		self.number_2 = self.buttons(master,'2',4,1,lambda: self.numberButton(2))
		self.number_3 = self.buttons(master,'3',4,2,lambda: self.numberButton(3))

		self.number_0 = self.buttons(master,'0',5,0,lambda: self.numberButton(0),Width= 20,Columnspan= 2)


		################ key bind  ################

		# numbers bind
		for i in range(0,10):
			self.numberInput(master,i)
	
		# operators bind
		operatorlist = ['+','-','*','/','%'] 
		for i in operatorlist:
			self.operatorInput(master,i)

		# equal operator bind
		master.bind('<Return>',self.equal)
		master.bind('=',self.equal)

		# percent button bind
		master.bind('%',self.percentButton)

		# decimal button bind
		master.bind('.',self.decimalButton)

		# delete key bind
		# delete key to remove last number
		master.bind('<BackSpace>',self.deleteKey)



	# button configures (GUI)
	def buttons(self,master,buttonName,givenRow,givenColumn,action,Width = 10,Columnspan = 1):
		button = Button(master,text= buttonName)
		button.configure(width= Width,height= 3,command= action)
		button.grid(row= givenRow,column= givenColumn,columnspan= Columnspan)
		return button

	

	# debug info
	# print out all the actives
	# waht is the operators,
	# what is the numbers in the queue
	# what is numbers on display
	def debugInfo(self,_event=None):
		global numberPool,numberQue,sign_Pool,display_number
		print(
			'numberPool:',numberPool,
			'\nnumberQue:',numberQue,
			'\nsign_pool:',sign_Pool,
			'\ndisplaynumber:',display_number
			)
	





	############### Operation methods #################

	### Numbers initi #######
	def numberButton(self,number,_event=None):
		global numberQue,display_number,numberPool,sign_Pool
		number = str(number)

		# change the text "AC" to text "C"
		if numberPool or numberQue:
			self.ac_button.configure(text="C")

		# make sure there is no extra number
		if numberPool and not sign_Pool:
			numberPool.pop()

		# avoid the over float
		if len(numberQue) < 15:
			if not numberQue or numberQue == '0':
				numberQue = number
			else:
				numberQue += number
			display_number.set(numberQue)
		
		self.debugInfo()
	
	####### AC button #######
	def acButton(self):
		global numberQue,display_number,numberPool,sign_Pool,acPress
		
		# add more features on the ac button
		# when doing calculation, it changes to 'C'
		# clear the content
		if self.ac_button['text'] == 'C' and acPress > 0:
			numberQue = '0'
			display_number.set(numberQue)
			acPress -= 1
		
		# if there is no more calculation, reset
		else:
			#reset everything 
			acPress = 1
			self.ac_button.configure(text='AC')
			numberQue = '0'
			numberPool = []
			sign_Pool = []
			display_number.set('0')

		self.debugInfo()

	####### Equal button #######
	def equal(self,_event=None):
		global numberQue,display_number,numberPool,sign_Pool
		
		# if there is a following number
		# if there is a operator
		if numberQue and sign_Pool:
			numberPool.append(Decimal(numberQue))
		
		if not sign_Pool:
			pass

		else:
			if '+' in sign_Pool:
				if numberQue:
				# if there is a following number
					numberQue = numberPool[0] + numberPool[1]		
				# if there is not a following number
				else:
					numberQue = numberPool[0] + numberPool[0]

			elif '-' in sign_Pool:
				if numberQue:
				# if there is a following number
					numberQue = numberPool[0] - numberPool[1]		
				# if there is not a following number
				else:
					numberQue = numberPool[0] - numberPool[0]
			
			elif 'X' in sign_Pool  or '*' in sign_Pool:
				if numberQue:
				# if there is a following number
					numberQue = numberPool[0] * numberPool[1]		
				# if there is not a following number
				else:
					numberQue = numberPool[0] * numberPool[0]
			
			elif '/' in sign_Pool:
				if numberQue:
				# if there is a following number
					try:
						numberQue = numberPool[0] / numberPool[1]	
					except:
						pass

				# if there is not a following number
				else:
					try:
						numberQue = numberPool[0] / numberPool[0]
					except:
						pass
			


			numberPool = []
			try:
				if len(str(numberQue)) < 15: # length control
					if Decimal(numberQue) == int(numberQue):
						display_number.set(str(int(numberQue)))
					else:
						display_number.set(str(numberQue))
					numberPool.append(Decimal(numberQue))

				else:
					display_number.set('E')
					numberPool.append(Decimal('0'))
				numberQue=''
			except:
				display_number.set('NOT VALID')
				numberQue= '0'

			sign_Pool = []		


		self.debugInfo()
	
	####### operations   #######
	def operations(self,operators,_event=None):
		global numberQue,display_number,numberPool,sign_Pool
		
		'''
		if numberQue not empty:
			append the numberQue into numberPool
	
		check the operators
		
		'''
		if numberQue:
			numberPool.append(Decimal(numberQue))
		else:
			# debug duplicate operators
			if sign_Pool:
				sign_Pool.pop()
		
		if sign_Pool:
			self.equal()

		#if operators not in sign_Pool:
		sign_Pool.append(operators)
		#reset the numberQue
		numberQue = ''
		self.debugInfo()

	# key input for number
	def numberInput(self,master,number):
		master.bind(number,lambda _event:self.numberButton(number))
	#
	#
	#
	# key input for operators
	def operatorInput(self,master,operators):
		master.bind(operators,lambda _event:self.operations(operators))
	#
	#
	#


	####### Percent button #######
	def percentButton(self,_event=None):
		global numberPool,numberQue
		if numberPool:
			numberQue = numberPool.pop()
			numberQue = str(numberQue)

		numberQue = Decimal(numberQue) / 100
		display_number.set(numberQue)
		
		numberQue = str(numberQue)
		self.debugInfo()

	####### Decimal button #######
	def decimalButton(self,_event=None):
		global numberPool,numberQue

		if not numberQue:
			numberQue += '0.'

		elif '.' not in numberQue:
			numberQue += '.'
		display_number.set(numberQue)

	####### Delete key #######
	def deleteKey(self,_event):
		global numberQue
		if numberQue and numberQue != '0':
			numberQue = numberQue.replace(numberQue[-1],'',1)
			if not numberQue:
				numberQue = '0'
			display_number.set(numberQue)
		else:
			self.acButton()
		self.debugInfo()

	####### Nagtive key #######
	# no bind for this key
	# avoid confusion with minus
	def negative(self):
		global numberQue,numberPool
		if numberPool and not numberQue:
			numberQue = numberPool.pop()
		if numberQue != '0':
			numberQue = Decimal(numberQue) * -1
			numberQue = str(numberQue)
		display_number.set(numberQue)
		self.debugInfo()





if __name__ == "__main__":
	gui = Tk()
	cal = calculator(gui)
	gui.mainloop()
