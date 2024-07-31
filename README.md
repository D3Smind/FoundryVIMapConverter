# FoundryViMapConverter

A script that converts the walls from exported FoundryVTT maps to simple high contrast shapes that might help people with vision problems.

Currently only supports exports from Foundry v11. I might have a look into changes to Foundry v12. If you like to contribute, feel welcome :)

## Dependencies
- matplotlib
- version_parser

## Usage
For the simple use there is a sample program in main.py, that loads a default configuration and saves the result.

Configuring your custom changes to the style can be a bit difficult. 
You will need to call "set_wall_style" with a list of "VIMapConverterWallConfig" objects that describe the walltype the style should be applied to
and a "VIMapConverterWallStyle" object that describes the style of wall the program should draw.
You might need to look into the Source Code of "VIMapConverter.py" to figure out the parameters.

I know this is not easy especially for beginners, but I could not find a easy way to make this more approachable.
If you need any help open a issue and we can figure it out.
