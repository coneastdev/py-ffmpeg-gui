# py ffmpeg gui

A simple python QT app for compressing and converting videos via [ffmpeg](https://github.com/FFmpeg/FFmpeg)

## install

You can download it from releases, however, you need to install ```PySide6``` via pip or your systems package manager [arch linux package](https://archlinux.org/packages/extra/x86_64/pyside6/)

Self explanatory, but you will also need [ffmpeg](https://ffmpeg.org/download.html) installed.

## how to use

### select file

Click the "Open In File Explorer" and select your file, do **not** leave this blank.

### format conversion

The drop down box allows you to chose the output file format, if left on "Same As Input" it won't convert it to a different file format.

### compression

This number will change the CRF compression rate to transfer quality for file size, the lower the number the higher quality and vise versa. Leave blank for no compression.

### output name

This will determine the name of the file, do **not** include the file format in the name. If left blank it will set the name as the current date and time.

### output folder

Click the "Open In File Explorer" and select your folder, if left blank it will export to your desktop. Also note when complete a link to the output folder will be in the conformation popup.
