# -*- coding: utf-8 -*-

#
# AudioCurve example Python plugin for Natron.
#
# Based on work done by rcspam (https://github.com/rcspam/audio2ascii).
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import NatronEngine

# extra lib added
import os, time, tempfile
from os import path

def getPluginID():
    return "AudioCurve"

def getLabel():
    return "AudioCurve"

def getVersion():
    return 1

def getIconPath():
    return "AudioCurve.png"

def getGrouping():
    return "Read"

def getDescription():
    return "Audio curve generator for Natron.\n\nWritten by @olear and @rcspam.\nPowered by SoX."
    
# extra defs added

def audioCurve(audioFileATA, asciiFileATA, dimATA, fpsATA, durationATA, xHeightATA, yHeightATA):
    ret_a2a = os.system(str(os.path.dirname(os.path.realpath(__file__)))+"/AudioCurve -input \""+str(audioFileATA)+"\" -output \""+str(asciiFileATA)+"\" -"+str(dimATA)+" -fps "+str(fpsATA)+" -frames "+str(durationATA)+" -cX "+str(xHeightATA)+" -cY "+str(yHeightATA));
    return ret_a2a

def animCurves(thisParam, fileAC, dimAC, durationAC ,frameStartAC):
    # ascii file
    asciiAC = open(fileAC, "r")
    # end frame
    lineAC = int(durationAC) + int(frameStartAC)
    # anim x
    if dimAC == 0:
        # reset x before recalculate
        thisParam.removeAnimation(0)
        for frameC in range(int(frameStartAC),lineAC + int(frameStartAC)):
            x = asciiAC.readline()
            thisParam.setValueAtTime(float(x), frameC, 0)
    # anim y
    elif dimAC == 1:
        # reset y before recalculate
        thisParam.removeAnimation(1)
        for frameC in range(int(frameStartAC),lineAC):
            y = asciiAC.readline()
            thisParam.setValueAtTime(float(y), frameC, 1)
    # anim yx
    else:
        # reset x and y before recalculate
        thisParam.removeAnimation(0)
        thisParam.removeAnimation(1)
        for frameC in range(int(frameStartAC),lineAC):
            x, y = asciiAC.readline().split ("_")
            thisParam.setValueAtTime(float(x), frameC, 0)
            thisParam.setValueAtTime(float(y), frameC, 1)

def paramHasChanged(thisParam, thisNode, thisGroup, app, userEdited):
    # audio input file
    audio_file = thisNode.inputFile.get()
    # ascii output file
    ascii_file = thisNode.curveFile.get()
    
    # convert dimension in comprehensive thing for audio2ascii script 
    dim = thisNode.dimEnsion.get()
    if dim == 0:
        dimension = "x"
    elif dim == 1:
        dimension = "y"
    elif dim == 2:
        dimension = "xy" 

    # Import Curve
    if ascii_file is not None and audio_file is not None and thisParam == thisNode.importCurve:
        ret_exec = audioCurve(audio_file, ascii_file, dimension, thisNode.framesPerSec.get(), thisNode.duraTion.get(), thisNode.xHeight.get(), thisNode.yHeight.get())
        # test and wait end of audio2ascii 
        if ret_exec == 0:
            # calculate animation 
            animCurves(thisNode.curveIn, ascii_file, thisNode.dimEnsion.get(), thisNode.duraTion.get(), thisNode.atFrameNum.get())
            

## / extra defs

def createInstance(app,group):

    #Create all nodes in the group
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setScriptName("Output1")
    lastNode.setLabel("Output1")
    lastNode.setPosition(758.75, 325.125)
    lastNode.setSize(104, 44)
    lastNode.setColor(0.699992, 0.699992, 0.699992)
    groupOutput1 = lastNode

    param = lastNode.getParam("Output_layer_name")
    if param is not None:
        param.setValue("RGBA")
        param.setVisible(False)
        del param

    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    del lastNode



    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(758.75, 161.125)
    lastNode.setSize(104, 44)
    lastNode.setColor(0.300008, 0.500008, 0.2)
    groupInput1 = lastNode

    param = lastNode.getParam("Output_layer_name")
    if param is not None:
        param.setValue("RGBA")
        param.setVisible(False)
        del param

    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    del lastNode

    #Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("AudioCurve.paramHasChanged")
        del param


    #Create the user-parameters
    lastNode.userNatron = lastNode.createPageParam("userNatron", "Settings")
    param = lastNode.createFileParam("inputFile", "Audio")
    param.setSequenceEnabled(False)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    lastNode.inputFile = param
    del param

    param = lastNode.createFileParam("curveFile", "CurveFile")
    param.setSequenceEnabled(False)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setVisible(False)
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    param.setDefaultValue(os.path.join(tempfile.gettempdir(),"audiocurve"))
    param.setValue(os.path.join(tempfile.gettempdir(),"audiocurve"))
    lastNode.curveFile = param
    del param

    param = lastNode.createChoiceParam("dimEnsion", "Dimension")
    entries = [ ("x", ""),
    ("y", ""),
    ("xy", "")]
    param.setOptions(entries)
    del entries

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Dimension curve X/Y (left/right)")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    options = param.getOptions()
    foundOption = False
    for i in range(len(options)):
        if options[i] == "x":
            param.setValue(i)
            foundOption = True
            break
    if not foundOption:
        app.writeToScriptEditor("Could not set option for parameter dimension on node AudioCurve")
    lastNode.dimEnsion = param
    del param

    param = lastNode.createDoubleParam("framesPerSec", "FPS")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(24, 0)
    param.setValue(24, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Calculate curve with this frame rate")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.framesPerSec = param
    del param

    param = lastNode.createIntParam("duraTion", "Frames")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(10000, 0)
    param.setDefaultValue(250, 0)
    param.setValue(250, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Duration in frames")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.duraTion = param
    del param

    param = lastNode.createIntParam("xHeight", "Height X")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(100, 0)
    param.setValue(100, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Height of X deviation in pixels")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.xHeight = param
    del param

    param = lastNode.createIntParam("yHeight", "Height Y")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(100, 0)
    param.setValue(100, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Height of Y deviation in pixels")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.yHeight = param
    del param

    param = lastNode.createIntParam("atFrameNum", "Start at frame")
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(1, 0)
    param.setValue(1, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Start the curve at this frame")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.atFrameNum = param
    del param

    param = lastNode.createButtonParam("importCurve", "Generate curve(s)")

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Generate curve from parameters")
    param.setAddNewLine(True)
    param.setPersistent(False)
    param.setEvaluateOnChange(False)
    lastNode.importCurve = param
    del param
    
    param = lastNode.createDouble2DParam("curveIn", "Curve ")
    param.setMinimum(-2.14748e+09, 0)
    param.setMaximum(2.14748e+09, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setMinimum(-2.14748e+09, 1)
    param.setMaximum(2.14748e+09, 1)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(500, 1)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Curve X/Y result")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.curveIn = param
    del param

    # extra callback added
    app.AudioCurve1.onParamChanged.set("AudioCurve.paramHasChanged")    

    #Refresh the GUI with the newly created parameters
    lastNode.refreshUserParamsGUI()
    del lastNode

    #Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupInput1)

