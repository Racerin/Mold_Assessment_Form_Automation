<!-- <style type="text/css">
    /* ol { list-style-type: upper-alpha; } */
    .temp {
        text-indent: 100px;
    }
</style> -->
# Welcome

This is documentation for the 'filling-out' of the Mold assessment form.
Follow the instructions below to complete the task.



# Road Map
1. Tree diagram of spreadsheet inputs.
* Headers:  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***Text Inputs***
    * Room Name
    * Floor Name (ID)
    * Room Type (ID)
    * Building Name (ID)
    * Others:  
        <ins>*Sections*</ins>  
        <!-- <div class="temp">***Text Inputs***</div> -->
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***Text Inputs***
        * Observer's Name
        * Date  
        ***Multiple options***
        * Damage or Stains  
            <ins>*Content*</ins>
            * Ceiling
            * ...
            * Pipes  
            *Modifiers*
                * Close to external wall (+)
        * Visible Mold  
            * Ceiling
            * ...
        * Wet or Damp  
        ***Single options***
        * Ceiling Material  
            <ins>*Content*</ins>
            * Ceiling Tile
            * Plaster
            * ...
        * Wall Material
        * ...  
        * HVAC Material  
        ***Multiple options***
        * Supplies and Materials  
        ***Text Inputs***
        * Describe Supplies and Materials
        * Additional Comments

2. Things to look for when assessing the rooms:
    * Is there any water damage (**Damage or Stains**), **Visible Mold**, or is an area **Wet or Damp**.
        * What items/surfaces were affected.
        * How big is the effect on each item.
        * Of the items/surfaces affected, is it within 3 feet of an external wall?
    * For each of these items; Ceiling, Walls, Floor, Windows, Furniture, HVAC;
        * Was it affected?



# Disclaimer

* Be very careful what information is placed in the spreadsheet. Once a form is submitted, it cannot be unsubmitted and the submission cannot be changed.



# Start

## User
1. Open the file 'template.xltx' in Microsoft Excel. If not found, open a new spreadsheet.
2. In this spreadsheet, enter the information for each 'Mold Assessment' Form. Follow the following instructions to complete the task.
    * Each row represents a single form submission.
    * Look at the Heading on top/row 1 (Room Name, Floor Name/ID, Room Type(Name/ID), Building, Name/ID, Others). These are your **headings**. Each heading is assigned its own column except for **'Others'**
    * Each column containing a header that has an 'ID' tag can be filled-out with IDs (Look at [appendix 2](#section_content) for more information).
    * **Others**:
        * The heading **'Others'** is unique. It is used to assign additional details to the form. No entries under 'Others' equates to default values and no additional information entered. The 'Others' column allows for entries **below** and **below right** of its header i.e. the Others header covers multiple columns and the remainder of the spreadsheet going to the right.
        * Each **section** requires its own **column**: 
        * A section and its content is formatted in a single cell as follows: **[section]:[content]**
        * There are 15 sections under Others:
            * Observer (O)
            * Date (D)
            * Mold Odor (MO)
            * Damage or Stain (DS)
            * Visible Mold (VM)
            * Wet or Damp (WD)
            * Materials for; Ceiling (CM), Walls (WaM), Floor (FlM), Windows (WiM), Furnishings (FsM), HVAC System (HM/HVAC)
            * Supplies & Materials (SM)
            * Describe Supplies & Materials (DSM)
            * Additional Comments (EX)
        * The **content** for a given **section** can be filled out using codes shown in 'Appendix 2'.  Look at **Examples** to better understand the syntax for filling out the spreadsheet.
3. Save the file as 'file.tsv'.
4. Pass the file to admin to fill-out form.


## Admin
Follow the instructions ahead to fill-out the Microsoft Forms based on the inofrmation entered in the 'file.tsv' file.
1. Copy the git repository [here](https://github.com/Racerin/Mold_Assessment_Form_Automation).
2. Install Python version 3.8.10 or older.
3. Open the command terminal and change the working directory to the copied repository is step 1.
4. Activate the virtual environment using the following command depending on your Operating ystem:
    * Microsoft: *Scripts/venv/bin/activate*
    * Linux: *source venv/bin/activate*
5. Install the chromedriver compatible with your personal system and chrome version. (Look-up an online tutorial).
6. Install the python dependencies using the command terminal:  
*'python3 -m pip install -r requirements.txt'*
7. Change the values in the file 'config.json' to their appropriate values.
8. Run the script: *'python3 app.py'*



# Examples:
Look at 'example template.xltx' for more information.



# Appendix
Fill-out the spreadsheet according to; **headers** and **section/content** as follows.


## 1. Headers:
1. **Room name** - Enter a room name. A good format for readability is;  
'*Block number, Room number, Room name*'
2. **Floor name** - Select a floor by entering an ID code or unique subset of characters of floor name (e.g. 'base'). **N.B.** The index starts with '0'.
    * 0 : Basement
    * 1 : Ground
    * 2 : Floor 1
    * 3 : Floor 2
    * 4 : Floor 3
    * 5 : Floor 4
    * 6 : Floor 5
3. **Room Type** - Select the room type by entering an ID code or unique subset of characters of room type (e.g. 'work' for 'Workshop').
    * 0 : Office
    * 1 : Classroom
    * 2 : Kitchen
    * 3 : Workshop
    * 4 : Lab
    * 5 : Store Room
    * 6 : Washroom
    * 7 : Conference Room
    * 8 : Meeting Room
    * 9 : Changing/Locker Room
    * 10 : Electrical Room
4. **Building Name** - Select the Building Name/Block of the contained room by entering an ID or unique subset of characters of the building/block's name (e.g. 'System' or 'block 9').
    * 0 : Geomatics Engineering and Land Management
    * 1 : George Moonsammy Building (Block 9)
    * 2 : Systems Lab (Block 11)
    * 3 : Block 13 (Max Richards Building)
    * 4 : Kenneth S. Julien Building (Block 1)
    * 5 : Block 2 Civil Building
    * 6 : Civil/Chemical/Mechanical Labs


## 2. <a name="section_content">*'Others'* > Sections/Content:</a>  
The ID of the *'section'* is in parenthesis. Each content contains one or more *options* with their own ID listed below in bulletin.

* **Observer (O)** - The name of the person that carried-out the evaluation. **N.B.** The default value is found in 'config.json' and will be override when changed on spreadsheet.
* **Date (D)** - The date when the evaluation was carried out. It **must** follow the format: *mm/dd/yyy*. **N.B.** The default value is found in 'config.json' and will be override when changed on spreadsheet.
* **Mold Odor (MO)** - Put in the number/letter corresponding to the Mold Odor smelled. **N.B.** The index starts with '0'.
    * 0 : None
    * 1 : Mild
    * 2 : Moderate
    * 3 : Strong
* **Damage or Stains (DS), Visible Mold (VM), Wet or Damp (WD)** - All these 3 *sections* has the same *content/options* below.  
Each option can be tagged with a number 0-3 corresponding to the size of area affected. If not tagged, a default of **'0'** will be set.  
Any option not selected will be given an automatic **'N/A'**.  
Each option can be tagged with the symbol '+' to state that it is close to an external wall (External Zone). (look at [appendix 3](#advance)).  
Several options can be selected by placing a comma between them.  e.g. Ceiling2, Walls3+, Windows+
    * Ceiling
    * Walls
    * Floor
    * Windows
    * Furnishings
    * HVAC systems
    * Supplies & Materials
    * Pipes
    * All components are more than 3 feet away from Exterior Wall
    * No Exterior Walls
    * No Effect/Zone,
* **Ceiling Material (CM)** - Put in the number/letter corresponding to the ceiling material affected. (One option)
    * 0 : Ceiling Tile
    * 1 : Plaster
    * 2 : Concrete
    * 3 : Sheet rock
    * 4 : Metal
    * 5 : Wood
    * 6 : N/A
* **Wall Materials (WaM)** - Put in the number/letter corresponding to the wall materials affected. (One option)
    * 0 : Sheet rock
    * 1 : Plaster
    * 2 : Concrete
    * 3 : Block
    * 4 : Tile
    * 5 : Wood
    * 6 : N/A
* **Floor Material (FlM)** - Put in the number/letter corresponding to the floor material affected. (One option)
    * 0 : Wood
    * 1 : Carpet
    * 2 : Vinyl
    * 3 : Ceramic
    * 4 : Concrete
    * 5 : N/A
* **Windows Material (WiM)** - Put in the number/letter corresponding to the window type affected. (One option)
    * 0 : Exterior
    * 1 : Interior
    * 2 : skylight
    * 3 : N/A
* **Furnishing (FsM**) - Put in the number/letter corresponding to the furnishing affected. (One option)
    * 0 : Furniture
    * 1 : Mechanical
    * 2 : Sink
    * 3 : Toilet
    * 4 : Copier
    * 5 : N/A
* **HVAC Material (HM/HVAC**) - Does not actually refer to 'HVAC Materials' but naming convention follows Microsoft Form. Put in the number/letter corresponding to the main type of HVAC affected. (One option)
    * 0 : Forced Air
    * 1 : Fan
    * 2 : Unit Ventilator
    * 3 : Window Unit
    * 4 : N/A
* **Supplies and Materials [in room] (SM**) - Put in the number/letter corresponding to the supplies and materials affected.
    * 0 : Books
    * 1 : Boxes
    * 2 : Equipment
    * 3 : N/A
* **Describe Supplies and Materials [in room] (DSM**) - Put in the number/letter corresponding to the floor affected.
    * 0 : Wrinkled pages
    * 1 : Crumpled boxes
    * 2 : Other
* **Additional Comment (EX**) - Enter a string of comments in parenthesis.  
e.g. EX(This is my additional message.)


## 3. <a name="advance">*'Others'* Advance:</a>
* DS, VM, WD Intensity - The numbers below represents the area size of the component.
    * 0 : None
    * 1 : The size of a sheet of paper
    * 2 : More than a sheet of paper to the size of a standard door
    * 3 : More than the size of a standard door
* '+' - Add the tag '+' to the end of the option in DS, VM, WD to state that it is within 3 feet of external wall.


## 4. <a name="config">Config:</a>
View/Edit the 'config.json' config file to change some default values.  
**N.B.** Changing these values especially file names can lead to irregular behavior.  
Also, maintain 'JSON' syntax within file to prevent errors.
* Observer name : Name of person who carried-out the assessments. This value is overridden individually per spreadsheet entry when user inputs 'Obeserver name' under 'Others'.
* tsv_load_file : The file containing user input spreadsheet information.
* tsv_save_file : The file containing completed spreadsheet information.
* website_url : The default url for the Microsoft Form online assessment form.



# Limitations
* Under Header *Others* > VM/DS/WD > Only one option can be selected with respect to its component.