# Config

## about

The app is configurable via the json file. A web-based GUI for configuration can be found [here](https://github.com/maxupravitelev/picam-config).

## handling false positives

Some weather and lightning conditions might trigger false positives. To deal with this you can try out tweaking different settings:

- Set minimum detection area to avoid detecting small particles like small leaves (set value between 0 and 100). 
- Set maximum area to avoid large shadows moving during sun light hours or moving clouds (set value between 0 and 100).
- Set contour limit to limit detected objects. For example, if your camera points at a tree, leaves moving in the wind would trigger false positives detecting a lot of objects. If you want to detect only a specified amount of objects (let's say one squirrel), you can set it here.

If you do not want to use any of those parameters, just set them to zero.