# Simple terraria map sticher

### **Most of this was written by chatgpt.** I fixed it enough to work for me but there might still be bugs and stuff.

This tool takes images generated with terraria snapshot tool and generates a tile set to be used with leaflet. 
## Setup
* Get python3
* `pip install -r requirements.txt`
* Get `libvips` which is the core dependancy doing all the transforming
## Usage
* Take a terraria snapshot with **image packing turned off**
* Put all the images you got into `tiles` folder
* Run the script
* Copy `output_tiles` folder and `index.html` into a webserver of your choice. You will probably need to adjust the `home`, `minZoom` and `maxZoom` inside of `index.html` based on your map size.