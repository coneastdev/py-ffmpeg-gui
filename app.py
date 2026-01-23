import os
import pathlib
from datetime import datetime

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox, QDialog
from PySide6.QtGui import QIntValidator
    
# replace output format with the inputs format
def replaceOutputFormatWithInput(inputPath: str, outputFormat: str):
    """
    set output video format to the sa,e as the input videos format
    
    Returns:
        str: Output format i.e. .mp4
    """
    if outputFormat == "Same As Input":
        inputFormat = []
        splitInput: list = list(inputPath)
        index: int = -1
        
        # reverse for loop to find last occurrence of "."
        while True:
            inputFormat.insert(0, splitInput[index])
            if splitInput[index] == ".":
                break
            else:
                index -= 1
        outputFormat: str = "".join(inputFormat)
        
    return outputFormat

# set output to local users desktop
def setOutputToDesktop():
    """
    Set the output path to the user's desktop directory.

    Returns:
        str: The path to the desktop directory.
    """
    return f"{str(pathlib.Path.home())}/Desktop"
    
# set file name to current date
def genOutputName():
    """
    set the output name to the date and time
    
    Returns:
        str: Date time in format of year-month-day_hour:minutes.seconds.
    """
    outputName = str(datetime.now()).replace(" ", "_")
    return outputName
    
# stops spaces in path from creating an error
def replaceSpacesWithBackSlash(path: str):
    """
    replace spaces with backslash's
        
    Returns:
        str: Fixed path.
    """
    return path.replace(" ", "\\ ")

# function to run the command
def execute(inputPath: str, outputCompression: str, outputFormat: str, outputName: str, output: str):
    """
    execute ffmpeg command with given arguments
    
    Returns:
        list: Completion status and dialog messages in the format of [completion status, dialog message]
    """
    # try so it outputs the error in the gui and not terminal
    try:
        os.system(f"ffmpeg -i {inputPath} {"-crf " + str(outputCompression) + " " if not (outputCompression == "") else ""}{output + "/" + outputName + outputFormat}")
        return ["completed", output]
    
    except Exception as e:
        return [e]
    
# gathers, cleans and executes commands    
def generateButtonClicked(window: QWidget, inputPathInput: QLineEdit, compressionInput: QLineEdit, outputFormatComboBox: QComboBox, fileNameInput: QLineEdit, outputPathInput: QLineEdit):
    # collect the inputs for execute function
    inputPath: str = inputPathInput.text()
    outputCompression: str = compressionInput.text()
    outputFormat: str = outputFormatComboBox.currentText()
    outputName: str = fileNameInput.text()
    output: str = outputPathInput.text()
            
    # process events to keep the dialog responsive
    QApplication.processEvents()
    
    # if blank warn else clean and execute
    if inputPath == "":
        notice = ["blank input"]
    else:
        # make output format same as input format
        if outputFormat == "Same As Input":
            outputFormat: str = replaceOutputFormatWithInput(inputPath, outputFormat)
            
        # set output to desktop if empty
        if output == "":
            output: str = setOutputToDesktop()
            
        # set output name to date if empty
        if outputName == "":
            outputName: str = genOutputName()
            
        # stop space in inputs and outputs from breaking 
        inputPath: str = replaceSpacesWithBackSlash(inputPath)
        output: str = replaceSpacesWithBackSlash(output)
        
        notice: list = execute(inputPath, outputCompression, outputFormat, outputName, output)
    
    # create a popup dialog box
    dialog = QDialog(window)
    dialog.setWindowTitle("py-ffmpeg-gui notification")
    dLayout = QVBoxLayout()
    dialog.setMinimumSize(300,150)
        
    dLabel = QLabel()
    dLayout.addWidget(dLabel)
    dialog.setLayout(dLayout)
    
    if notice[0] == "completed":
        dLabel.setText((f"Completed, exported to <a href='{notice[1]}'>{notice[1]}</a>"))
        
        dLabel.setOpenExternalLinks(True)
    elif notice[0] == "blank input":
        dLabel.setText("ERROR: No input video selected.")
    else:
        dLabel.setText(str(notice[0]))
            
    dBtn = QPushButton()
    dBtn.setText("Close")
    dLayout.addWidget(dBtn)
    dBtn.clicked.connect(dialog.close)
        
    dialog.setLayout(dLayout)
    dialog.show()
    QApplication.processEvents()
    
# the main qt window

def app():
    qt_app = QApplication([])
    window = QWidget()
    window.setWindowTitle("py ffempg gui")
    window.resize(350, 450)
    
    layout = QVBoxLayout()
    
    # input file
    inputPathLabel = QLabel("File Path For Input video")
    layout.addWidget(inputPathLabel)
    
    inputPathInput = QLineEdit()
    layout.addWidget(inputPathInput)
    
    inputPathButton = QPushButton("Open In File Explorer")
    layout.addWidget(inputPathButton)
    
    def onInputPathClicked():
        file_url, _ = QFileDialog.getOpenFileUrl(window, "Select Input File")
        if file_url.isValid():
            inputPathInput.setText(file_url.toLocalFile())
    inputPathButton.clicked.connect(onInputPathClicked)
    
    # output format
    outputFormatLabel = QLabel("Output File Format")
    layout.addWidget(outputFormatLabel)
    
    outputFormatComboBox = QComboBox()
    outputFormatComboBox.addItems(["Same As Input", ".mp4", ".avi", ".mov", 
                                   ".wmv", ".mkv", ".webm", ".mpeg", ".flv", 
                                   ".mts", ".gif", ".mp3", ".wav", ".ogg"])
    
    layout.addWidget(outputFormatComboBox)
    
    # output compression
    compressionLabel = QLabel("Compression Factor 0-51")
    layout.addWidget(compressionLabel)
    
    compressionInput = QLineEdit()
    compressionInput.setValidator(QIntValidator(0, 51))
    layout.addWidget(compressionInput)
    
    # stop leading zeros
    def removeLeadingZeros():
        text = compressionInput.text()
        if text.startswith("0") and len(text) > 1:
            compressionInput.setText(text.lstrip("0"))
    compressionInput.textChanged.connect(removeLeadingZeros)
    
    # file name
    fileNameLabel = QLabel("Output File Name")
    layout.addWidget(fileNameLabel)
    
    fileNameInput = QLineEdit()
    layout.addWidget(fileNameInput)
    
    # output folder
    outputPathLabel = QLabel("File Path For Output Folder")
    layout.addWidget(outputPathLabel)
    
    outputPathInput = QLineEdit()
    layout.addWidget(outputPathInput)
    
    outputPathButton = QPushButton("Open In File Explorer")
    layout.addWidget(outputPathButton)
    
    def onOutputPathClicked():
        directory = QFileDialog.getExistingDirectory(window, "Select Output Folder")
        if directory:
            outputPathInput.setText(directory)
    outputPathButton.clicked.connect(onOutputPathClicked)
    
    def generateButtonClick():
        generateButtonClicked(window, inputPathInput, compressionInput, outputFormatComboBox, fileNameInput, outputPathInput)
    
    # generate button
    generateButton = QPushButton("generate")
    layout.addWidget(generateButton)
    generateButton.clicked.connect(generateButtonClick)
    
    window.setLayout(layout)
    window.show()
    qt_app.exec()
    
if __name__ == "__main__":
    app()