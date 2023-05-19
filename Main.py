from Driver import Driver
from Cocos import Cocos
import os
from dotenv import load_dotenv
import os 

load_dotenv()


driver_1=Driver()
cocos=Cocos(driver_1,os.getenv('USERNAME_KEY'),os.getenv('PASSWORD_KEY'))

cocos.obtenerBalance()