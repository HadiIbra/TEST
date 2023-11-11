import subprocess
import pyautogui
import os
import time
import ctypes
from sys import platform
import msvcrt

# define global vars
PROCESS_PER_MONITOR_DPI_AWARE = 2.0

class ChangeResolution:
    
    def __init__(self, numOfStandardResolutionEntrie, defaultScale, batScriptDir):
        self.dicOfResolution = {
            0: [1920, 1200],    # WUXGA
            1: [1920, 1080],    # Full HD  → Standard!!
            2: [1680, 1050],
            3: [1600, 1200],
            4: [1600, 1024],
            5: [1600, 900],     # HD+
            6: [1440, 900],
            7: [1360, 768],
            8: [1280, 1024],
            9: [1280, 960],
            10: [1280, 800],
            11: [1280, 768],
            12: [1152, 864],     # HD
            13: [1024, 768]
        }
        
        self.batScriptDir = batScriptDir
        self.numOfStandardResolutionEntrie = numOfStandardResolutionEntrie 
        possibleScaleList = [100, 125, 150, 175]
        
        if defaultScale in possibleScaleList:
            self.defaultScale = defaultScale
        else:
            raise ValueError('USER-ERROR: ur wished is not included in the pre-defined "possibleScaleList" please adjust the code or change the defaultScale')
            
        self.stepSize = 25
        pass

    def checkcurrentScalePercent(self) -> [bool, int]: 
        user32 = ctypes.windll.user32
        scaleFactor = user32.GetDpiForSystem() / 96.0  # 96 is the default DPI
        scalePercent = int(scaleFactor * 100)
        
        print(f"Current Screen scale: {scalePercent}%")
        if not scalePercent == self.defaultScale:
            return [False, scalePercent]
        else:
            return [True, scalePercent]
        
    def changeScale(self, numOfButtonAction : int, moveDirection : str):        
        
        # The following code is just to ask user if the windows setting window is closed or not... but we don't need this anymore because i integrated the closing option in the bash Script
        # print("Please make sure that the the Windows of the windows settings is closed!!... if it's closed press ENTER to continue")
        # while True:
        #     key = msvcrt.getch().decode('utf-8')
        #     if key == '\r':  # Check for Enter key (carriage return)
        #         print("You pressed Enter!. Monitor Scale will be now changed....")
                
        #         # Call the Bash script and pass the variables as arguments
        #         if platform == "linux" or platform == "linux2":                   # TODO: need to be discussed later!!! 
        #             # Shell script
        #             # subprocess.call(['sh', os.path.join(os.getcwd(), "changeScale.sh"), str(numOfButtonAction), moveDirection])
        #             print('Nothing implemented yet ... need to be discussed!!')
        #         elif platform == "win32" or platform == "win64":
        #             # bat Script ...
        #             subprocess.call([os.path.join(os.getcwd(), "changeScale.bat"), str(numOfButtonAction), moveDirection])
                
        #         # stop the While loop...
        #         break
        #     elif key == ' ':  # Check for the spacebar key       
        #         print("You pressed the spacebar!... Restart Programm again")
        #         break
        
            
        # Call the Bash script and pass the variables as arguments
        if platform == "linux" or platform == "linux2":                   # TODO: need to be discussed later!!! 
            # Shell script
            # subprocess.call(['sh', os.path.join(os.getcwd(), "changeScale.sh"), str(numOfButtonAction), moveDirection])
            print('Nothing implemented yet ... need to be discussed!!')
        elif platform == "win32" or platform == "win64":
            # bat Script ...
            subprocess.call([os.path.join(self.batScriptDir, "changeScale.bat"), str(numOfButtonAction), moveDirection])     
                
    def calculateStepsAndmoveDirection(self, currentScalePercent, targetScale, stepSize) -> [str, int] :
        # Calculate the difference between the currentScalePercent and targetScale and detect the moveDirection..
        diff = abs(currentScalePercent - targetScale)
        
        # Determine the moveDirection → Please Note that the moveDirection has to 
        if currentScalePercent > targetScale:
            moveDirection = "UP"
            diff *= -1
        elif currentScalePercent < targetScale:
            moveDirection = "DOWN"
        else:
            moveDirection = "STAY"
        
        # Calculate the number of steps needed
        numOfButtonActions = abs(diff) / stepSize
        
        return moveDirection, int(numOfButtonActions)

    def checkCurrentResolution(self) -> bool:
        screen_info = pyautogui.size()  # get current monitor resolution
        print("The current resolution is:", screen_info[0], "*", screen_info[1])
                
        # check for the standard Resolution
        if screen_info[0] == self.dicOfResolution[self.numOfStandardResolutionEntrie][0]:
            if screen_info[1] == self.dicOfResolution[self.numOfStandardResolutionEntrie][1]:
                print("The current resolution is alright, no need to change...")
                return True
            else:
                print("The current resolution is Wrong,has to be changed...")
                return False
        else:
            print("The current resolution is Wrong,has to be changed...")
            return False

    def changeResolution(self, width: int, height: int) -> int:
        # cmd = ["QRes.exe", f"/x:{width}", f"/y:{height}"]
        cmd = f"QRes.exe /x:{width} /y:{height}"
        result = os.system(cmd)
        time.sleep(2)   # for the stability of the program
        return result
                        
    def checkAndChangeMonitorSettings(self):

        rightResolution = self.checkCurrentResolution()
        
        if not rightResolution:
        # the current resolution is not a standard one, change needed
            resolutionSetSuccessed = self.changeResolution(width = self.dicOfResolution[self.numOfStandardResolutionEntrie][0], 
                                  height = self.dicOfResolution[self.numOfStandardResolutionEntrie][1])
            
            # check the Resolution again ...
            self.checkCurrentResolution()
            
            if not resolutionSetSuccessed:
                pass # TODO: do somthing... but later to discuss...
            
            else:
                print("The right resolution is successfully setted :)")
 
        # start checking the current scale of the Monitor....
        [isTheRightScale, currentScalePercentPercent] = self.checkcurrentScalePercent()
        
        if not isTheRightScale:
            # adjiust the scale of the Monitor using a bat Script ("changeScale.bat"), that should be located in the same directory as this Script
            [moveDirection, numOfButtonActions] = self.calculateStepsAndmoveDirection(currentScalePercent = currentScalePercentPercent, 
                                                targetScale = self.defaultScale, 
                                                stepSize = self.stepSize)
            print('Scale move direction: ', moveDirection)
            print('number of Button Actions needed to adjust the Scale', numOfButtonActions)
            self.changeScale(moveDirection=moveDirection, 
                             numOfButtonAction=numOfButtonActions)    

if __name__ == "__main__":
    '''      
    dicOfResolution = {
            0: [1920, 1200],    # WUXGA
            1: [1920, 1080],    # Full HD  → Standard!!
            2: [1680, 1050],
            3: [1600, 1200],
            4: [1600, 1024],
            5: [1600, 900],     # HD+       
            6: [1440, 900],
            7: [1360, 768],     
            8: [1280, 1024],
            9: [1280, 960],
            10: [1280, 800],
            11: [1280, 768],
            12: [1152, 864],     # HD
            13: [1024, 768]

    possibleScaleList = [100, 125, 150, 175]
    
    Workflow:
    1. first select the default resolution "numOfDefaultResolution" and the monitor scale "defaultScale" you wanna set → but note that the values are included in the pre-defined lists above.
        u have also to define the current path where the bat-script "changeScale.bat" is located...
    2. this python script will then check the current resolution and scaling and attempts to change them if they vary from the default/wished values
    
    NOTE: * Changing the resolution is done using QRes.exe → but this can also be changed in the same way as the scaling 
          * Changing the monitor scale is done with the help of a bat-script "changeScale.bat". 
            This bat script is well documented ... basically it opens the settings window and changes the scale automatically by pressing some keys
    '''

    # define ur spec. values
    batScriptDir = os.path.join(os.getcwd(), 'newCode')
    print(batScriptDir)
    numOfDefaultResolution = 1            # → choose the number of the ur wished Resolution in the dictt "dicOfResolution" above
    defaultScale = 100                    # → choose the ur default scale of the monitor → possibleScaleList = [100, 125, 150, 175]

    
    CS = ChangeResolution(numOfStandardResolutionEntrie = numOfDefaultResolution, 
                          defaultScale = defaultScale, 
                          batScriptDir = batScriptDir)
    
    CS.checkAndChangeMonitorSettings()