# Blender Rig Assistant

![](https://i1.wp.com/paladinstudios.com/wp-content/uploads/2020/03/logo-1.png)

 * [Description](#description)
 * [Best Practices](#bestpractices)
 * [Requirements](#requirements)
 * [Developing & Testing](#develop)
 * [Creating a release](#release)

<a name="description"/>

# Description

The Blender Rig Assistant helps speed up the rigging process of game assets by supporting an older but very stable workflow. This workflow uses 3 main types of bones:

* Deform bones: Used in by blender and in the game engine to deform the character
  
* Cnstr_ bones: Used as constraints for the deform bones. They have the same orientation as the deform bones so you don't have to worry about local/pose/world space in your constraints
  
* Ctrl_ bones: Used to control the rig. These bones are what the animator will use to make their poses.

When done correctly 2 hierarchies of bones are created linked by constraints, a "Deform Hierarchy" that will be exported to the game engine and a "Control Hierarchy" that will be used by the animator to create animations 

There are also a lot of smaller tools that will increase productivity and help speed up your rigging workflow

<a name="bestpractices"/>

# Best Practices

The tool bar has been setup to work from top to bottom. So to start create an armature and end with adding control shapes for the animator to easily select controls.

Armature
* Create An Armature: creates an armature to start your rig 
* Dissconnect Bones: Bones are linked together can't use translation. This is a blender thing and no game engine supports these connected bones. Always disconnect!
* Remove Roll: Removes Roll from bones. Recommended when you want to control your rotations better.
* Chain Parent: Special mode where you are able to quickly create a linear hierarchy. Each bone you select after the first one will be parented to the previous one

Constraints  
* Type: Selects the type of constraints you will get when using the constraint buttons
* Create Constraint Bone: Creates a duplicate of your selected deform bones with the prefix CNSTR_ and constraints it using the type that was set above
* Append Constraint To Bone: Creates another constraint on the selected deform bone with the same CNSTR_ bone as a target
* Constraint Between Selected Bones: Creates a constraint between the selected bones. The last selected bone will get the constraint and the first selected bone will be the target

Removing Bones and Constraints
* Remove All Constraints: Removes all constraints from a selected bone
* Remove Constraint Bone: When a deform bone is selected the CNSTR_ bone is deleted and the constraints together with the constraint on the deform bone
* Remove Selected Bone: Removes a selected bone

Controls and Offsets
* Space: Will create control bones in either world or local space
* Create Control Bones: Creates bones prefixed with CTRL_ for the selected deform bones. Looks if there are CNSTR_ bones and parents them under the CTRL_ bones
* Create Local Offset Bones: Creates a duplicate of the selected bone and parents the original bone under it. When 2 bones are selected it duplicates the first selected bone and parents it under the second selected bone

*Suffix.l/Suffix.r: adds a suffix to the name of the bone making it easier to mirror or symmetrize

Control Shapes
* Add Control Shapes: Will set the selected shape to the selected bones. In edit or pose mode select the bones you want to give the shape to then using the outliner select the shape then hit the button
* Remove Control Shapes: Removes the shapes from selected bones

* Shape names (Circle, Sphere, Piramid, Cube, Square): Will create basic shapes to use as custom objects for control bones


# Requirements

Has been tested on Blender version 3.0 up to version 4.1. 
Basic rigging knowledge required

<a name="develop"/>

# Developing & Testing
To test during development, add the path to the addons folder in this repo to the Scripts path in Blender Preferences. Preferences -> File Paths -> Data -> Scripts

After adding the path, make sure to reload the python scripts within Blender. Click the top left Blender icon -> System -> Reload Scripts.

![reload](https://github.com/PaladinStudiosBVs/Blender-RigAssistant/assets/29857793/17c82162-f423-4926-bfa2-42fc20ddae34)

Now the addon scripts should be in Blender and the add-on can be enabled in the preferences menu. Search for `Paladin` with the `Community` tab enabled to find it.

![image](https://github.com/PaladinStudiosBVs/Blender-RigAssistant/assets/29857793/c09867f2-4efc-481a-8d37-3674db0b0ff0)


Click the checkbox to enable the add on.

<b> Note: </b> When the addon has been enabled once, this step can be skipped. Reloading scripts is only required.

The addon is now available in the main viewport on the 'N' panel. If it isn't visible, press `N` to reveal the panel and click on `Paladin Studios`. 

<a name="release"/>

# Creating a new release
Checkout the repository and switch to the branch you need a release from.

Zip the `Blender-RigAssistant` folder to a `Blender-RigAssistant`x.x.x.zip`, where x.x.x should be the relevant version number.

The zip file can now be distributed and installed using the add on preferences menu, by clicking `Install` and selecting the .zip file.
