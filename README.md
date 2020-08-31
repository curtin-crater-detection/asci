# asci

_ref: Lagain, A., Servis, K., Benedix, G.K., Norman, C. and Bland, P. (2020) Model Age Derivation of Large Martian Impact Craters, using automatic crater counting methods. Submitted to Earth and Planetary Science Letters (24/08/2020)_

This repository contains an ArcMap Python Toolbox which removes secondary craters from a crater detection map.

The plugin uses the following process to detect and remove secondary craters:

1. A Voronoi polygons (VPs) tessellation is computed over the crater detection area (with the detected craters simplified as points)
2. The size frequency distribution (SFD) of VPs is then calculated
3. The SFD is compared to those produced by 300 different simulated random impact crater populations
4. The intersection between the VPs SFD and the simulation populations SFD at +1σ is used as a threshold area size
5. Any VPs which have an area below this threshold size are removed from the map.

The plugin outputs new ArcMap layers for primary and secondary craters, and for their corresponding counting areas.

This plugin is tested and working on ESRI ArcMap 10.6. Other ArcMap versions may require minor modifications to the `arcpy` ArcGIS Python library calls.

## Installation

### Additional Python dependencies

In addition to `arcpy`, this toolbox utilises a couple of other external Python libraries:

- `pandas`
- `shapely`
- `scipy`
- `numpy`
- `jinja`

These need to be installed using the ArcGIS Python executable as follows. Note - if your ArcGIS installation is in a different folder, please amend the initial path in the commands accordingly.

The precompiled Python wheel for Shapely must be used instead of building from source. Download the Shapely-1.6.4.post2-cp27-cp27m-win32.whl wheel from [this link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) and save it to your local downloads folder.

```cmd
C:\Python27\ArcGIS10.6\python.exe -m pip install pandas scipy matplotlib numpy Jinja2

# The following command installs the Shapely wheel that you have downloaded as per the above instructions
C:\Python27\ArcGIS10.6\python.exe -m pip install C:\Users\YOUR_USERNAME\Downloads\Shapely-1.6.4.post2-cp27-cp27m-win32.whl
```

### Installing the ArcMap toolbox

Add this repository as a source using the ArcMap file browser. The Python toolbox should now be visible in the ArcMap tools directory. Clicking the Toolbox should then reveal a tool called "Secondary Crater Removal". Double clicking on the tool will open a dialog window through which the process can be launched.

## Dimensions

The counting area must be in square kilometres.
