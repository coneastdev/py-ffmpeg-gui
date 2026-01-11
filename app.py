from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox
from PySide6.QtGui import QIntValidator  # Import QIntValidator
import os

def execute(input: str, output: str, outputCompression: int, outputFormat: str):
    return ""
    
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
    outputFormatComboBox.addItems(["Same As Input", ".mp4", ".avi", ".mov", ".wmv", ".mkv", ".webm", ".mpeg", ".flv", ".mts", ".gif", ".mp3", ".wav", ".ogg"])
    layout.addWidget(outputFormatComboBox)
    
    # output compression
    compressionLabel = QLabel("Compression Factor 0-51")
    layout.addWidget(compressionLabel)
    
    compressionInput = QLineEdit()
    compressionInput.setValidator(QIntValidator(0, 51))  # Set validator for range 0-51
    compressionInput.setText("0")  # Set default value to 0
    layout.addWidget(compressionInput)
    
    # remove leading zeros
    def removeLeadingZeros():
        text = compressionInput.text()
        if text.startswith("0") and len(text) > 1:
            compressionInput.setText(text.lstrip("0"))

    compressionInput.textChanged.connect(removeLeadingZeros)  # Connect signal to function
    
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
        output: str = outputPathInput.text()
        input: str = inputPathInput.text()
        outputCompression: int = int(compressionInput.text())
        outputFormat: str = outputFormatComboBox.currentText()
        
        execute(output, input, outputCompression, outputFormat)
    generateButton.clicked.connect(generateButtonClicked)
    
    window.setLayout(layout)
    window.show()
    qt_app.exec()
    
if __name__ == "__main__":
    app()