#!/usr/local/bin/python3


import os, sys, datetime
import json
from PIL import Image


strPathMainJSON = "/Users/quark2930/Work/apps/sshAppFrame/var/main.json"
dicMain = {}
with open(strPathMainJSON, "rb") as fMain: dicMain = json.load(fMain)

strPathApp  = "/Users/quark2930/Work/apps"
strAddrMain = "http://localhost"

strPathCurr = os.getenv("PWD")
strPathHome = os.getenv("HOME")

strPathDir = os.path.dirname(strPathMainJSON)
strPrefixQ = "tmpQueue_"

strNameWin = "" if len(dicMain[ "#display" ]) <= 0 else dicMain[ "#display" ][ 0 ] 

if sys.argv[ 1 ] == "manage": 
  while True:
    try: 
      listQueue = [ s for s in os.listdir(strPathDir) if s.startswith(strPrefixQ) ]
      if len(listQueue) <= 0: continue
      
      listQueue.sort()
      os.system("mv " + os.path.join(strPathDir, listQueue[ 0 ]) + " " + strPathMainJSON)
    finally:
      os.system("sleep 0.05")
  
  sys.exit(0)
elif sys.argv[ 1 ] == "enter": 
  dicMain[ "#display" ] = [ sys.argv[ 2 ] ]
elif sys.argv[ 1 ] == "leave": 
  dicMain[ "#display" ] = []
elif sys.argv[ 1 ] == "clear": 
  if strNameWin == "": sys.exit(1) # Something is totally wrong!
  for strKey in [ s for s in dicMain.keys() if s[ 0 ] != "#" ]: 
    if dicMain[ strKey ].get("group", "") == strNameWin: dicMain.pop(strKey)
elif sys.argv[ 1 ] == "img":
  if sys.argv[ 2 ] == "add": 
    if strNameWin == "": sys.exit(1) # Something is totally wrong!
    
    strPathImg = sys.argv[ 3 ]
    if not os.path.exists(strPathImg): 
      sys.stderr.write("FATAL ERROR: Cannot find %s"%strPathImg)
      sys.exit(1)
    
    listRatioPre = [ s for s in sys.argv if s.startswith("-r") ]
    nRatio = 100 if len(listRatioPre) == 0 else int(listRatioPre[ -1 ])
    
    if strPathImg.startswith("~"): strPathImg = os.path.join(strPathHome, strPathImg[ 1 : ])
    elif strPathImg.startswith("/"): pass # Oh, absolute path
    else: strPathImg = os.path.join(strPathCurr, strPathImg)
    
    if not strPathImg.startswith(os.path.join(strPathHome, "Work")): # I cannot treat such files 
      print("FATAL ERROR: Not in the area of web server")
      sys.exit(1)
    
    strAddrImg = strAddrMain + strPathImg[ len(os.path.join(strPathHome, "Work")) : ]
    
    (nW, nH) = Image.open(strPathImg).size
    nW = int(nW * 0.01 * nRatio)
    nH = int(nH * 0.01 * nRatio)
    
    # Making a new window from infos gathered above
    
    strContent  = "<table border = 0 style = \"border-spacing: 0; border-collapse: collapse; margin: 0; padding:0;\">"
    strContent += "<tr><td bgcolor = \"#A8C6FF\" style = \"margin: 0; padding: 0; "
    strContent += "font-size: 15px; font-family: Helvetica, sans-serif\">"
    strContent += "<center>%(name)s</center></td></tr>"
    strContent += "<tr><td style = \"margin: 0; padding: 0; font-size: 0;\">"
    strContent += "<<img src = \"%(src)s\" width = %(width)i height = %(height)i "
    strContent += "style = \"border-color: red; margin: 0; padding: 0;\" border = 0>/td></tr></table>"
    
    dicNewImg = {
      "left": 0.51, "top": 0.1, "width": 0.001, "height": 0.001, 
      "group": strNameWin, 
      "src": strPathImg, 
      "content": strContent%{"name": os.path.basename(strPathImg), "src": strAddrImg, "width": nW, "height": nH}
    }
    
    nIdxNew = 0
    
    while True: 
      if strNameWin + "_%02i"%nIdxNew not in dicMain: break
      nIdxNew += 1
    
    dicMain[ strNameWin + "_%02i"%nIdxNew ] = dicNewImg

strOrder = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
strNameNew = strPrefixQ + strOrder + os.path.basename(strPathMainJSON)
with open(os.path.join(strPathDir, strNameNew), "w") as fMain: fMain.write(json.dumps(dicMain))


