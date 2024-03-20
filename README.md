### RGB Image to Arduino CPP

This is some simple code to get RGB images into PROGMEM to be displayed by a Adafruits GFX library. I am using it for a SSD1351 driver display and aside from color encoding issues (which I will fix), it is read and displayed perfectly by my ESP32-WROOM

#### Usage
Install required library "Pillow"
`pip install pillow`
Make a directory called "Img" in the project directory
Place images you want to convert in that folder (only .pngs supported)