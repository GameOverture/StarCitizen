"""'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                 BaLK HOTAS
              (Joystick Gremlin Profile/Scripts for Star Citizen)

                          2018 Jason "BaLK" Knobler
          (https://robertsspaceindustries.com/citizens/Game_Overture)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
import gremlin
import user
import scmap

throttle = gremlin.input_devices.JoystickDecorator(user.THR_Name,
                                                   user.THR_Id,
                                                   "Default")

isStrafeLeftRight = 0
isStrafeUpDown = 0
isStrafeFwdBck = 0

def setStrafeAxes(vjoy, joy):
	global isStrafeUpDown
	global isStrafeLeftRight
	global isStrafeFwdBck
	thrustAmt = 0 # A value 0..1
	if joy[user.THR_Name].button(user.THRSWITCH_FlapsDown).is_pressed:
		thrustAmt = joy[user.THR_Name].axis(user.THRAXIS_StrafeThrustAmt).value
		thrustAmt = (thrustAmt * -0.5) + 0.5 # Normalize axis to 0..1
		thrustAmt = max(0.05, thrustAmt) # Clamp lower bounds to 0.25
	else:
		thrustAmt = 1.0
	vjoy[1].axis(scmap.StrafeLeftRight).value = thrustAmt*isStrafeLeftRight
	vjoy[1].axis(scmap.StrafeUpDown).value = thrustAmt*isStrafeUpDown;
	vjoy[1].axis(scmap.StrafeForwardBack).value = thrustAmt*isStrafeFwdBck

@throttle.button(user.THRSWITCH_FlapsDown)
def onThrottleTHRSWITCH_FlapsDown(event, vjoy, joy):
	setStrafeAxes(vjoy, joy)

@throttle.axis(user.THRAXIS_StrafeThrustAmt)
def onThrottleAxis_Slider(event, vjoy, joy):
	setStrafeAxes(vjoy, joy)

@throttle.hat(user.THRHAT_StrafeUpDown)
def onThrottleHat_StrafeUpDown(event, vjoy, joy):
	global isStrafeUpDown
	isStrafeUpDown = event.value[1]
	setStrafeAxes(vjoy, joy)

@throttle.button(user.THRBTN_StrafeRight)
def onThrottleBtn_StrafeRight(event, vjoy, joy):
	global isStrafeLeftRight
	isStrafeLeftRight = 1 if event.is_pressed else 0
	setStrafeAxes(vjoy, joy)

@throttle.button(user.THRBTN_StrafeLeft)
def onThrottleBtn_StrafeLeft(event, vjoy, joy):
	global isStrafeLeftRight
	isStrafeLeftRight = -1 if event.is_pressed else 0
	setStrafeAxes(vjoy, joy)

@throttle.button(user.THRBTN_StrafeForward)
def onThrottleBtn_StrafeForward(event, vjoy, joy):
	global isStrafeFwdBck
	isStrafeFwdBck = 1 if event.is_pressed else 0
	setStrafeAxes(vjoy, joy)

@throttle.button(user.THRBTN_StrafeBackward)
def onThrottleBtn_StrafeBackward(event, vjoy, joy):
	global isStrafeFwdBck
	isStrafeFwdBck = -1 if event.is_pressed else 0
	setStrafeAxes(vjoy, joy)
