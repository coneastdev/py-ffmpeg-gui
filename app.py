import os
import platform
from datetime import datetime

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox, QDialog
from PySide6.QtGui import QIntValidator

sys = platform.system()

def execute(inputPath: str, outputCompression: str, outputFormat: str, outputName: str, output: str):
    # notify user their is no input and terminate function
    if inputPath == "":
        return ["blank input"]
    
    # if same as input will replace output format with the inputs format
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
        
    # set output to desktop if blank
    if output == "":
        desktop = ""
        if sys == "Linux":
            desktop = f"/home/{os.getlogin()}/Desktop"
        elif sys == "Windows":
            desktop = "C:\\Users\\" + os.environ.get("USERNAME") + "\\Desktop"
        
        output = desktop
    
    # set file name to current date if empty
    if outputName == "":
        outputName = str(datetime.now()).replace(" ", "_")

    if sys == "Linux":
        output: str = output + "/" + outputName + outputFormat
        os.chdir("/")
    elif sys == "Windows":
        output: str = "\\" + output + "\\" + outputName + outputFormat
        os.chdir("C:\\")

    # stops spaces in path from creating an error
    inputPath = inputPath.replace(" ", "\\ ")

    # try so it outputs the error in the gui and not terminal
    try:
        os.system(f"ffmpeg -i {inputPath} {"-crf " + str(outputCompression) + " " if not (outputCompression == "") else ""}{output}")
        
        # remove file from output path so when you click the link it opens the folder instead of the video
        splitOutput: list = list(output)
  
        while True:
            splitInput.pop(-1)
            if splitInput[-1] == "/":
                break
            
        cleanedOutput: str = "".join(splitInput)
        
        return ["completed", cleanedOutput]
    
    except Exception as e:
        return [e]
    
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
    
    # generate button
    generateButton = QPushButton("generate")
    layout.addWidget(generateButton)
    
    def generateButtonClicked():
        # collect the inputs for execute function
        inputPath: str = inputPathInput.text()
        outputCompression: str = compressionInput.text()
        outputFormat: str = outputFormatComboBox.currentText()
        outputName: str = fileNameInput.text()
        output: str = outputPathInput.text()
                
        # process events to keep the dialog responsive
        QApplication.processEvents()
        
        notice = execute(inputPath, outputCompression, outputFormat, 
                         outputName, output)
        
        dialog = QDialog(window)
        dialog.setWindowTitle("py-ffmpeg-gui notification")
        dLayout = QVBoxLayout()
        dialog.setMinimumSize(300,150)
            
        dLabel = QLabel()
        dLayout.addWidget(dLabel)
        dialog.setLayout(dLayout)
        
        if notice[0] == "completed":
            dLabel.setText(("Completed, exported to <a href='{}'>" + 
                            notice[1] + "</a>").format(notice[1]))
            
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
    generateButton.clicked.connect(generateButtonClicked)
    
    window.setLayout(layout)
    window.show()
    qt_app.exec()
    
if __name__ == "__main__":
    app()