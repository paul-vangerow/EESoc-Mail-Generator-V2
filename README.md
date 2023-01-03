# EESoc-Mail-Generator-V2
Second Version of the EESoc mail generator

Goals:
- Make the generator more usable
  - Web Interface with easier formatting options
  - Real time viewing options (DONE)
  - Easy one command running. (Set up environments, executable?) (DONE)
  - Buttons and so on. (Drag and drop? and more UI elements)
- Make the templates look better
  - General formatting things, make section options better
  - Prevent things from getting too close
- Make sending out emails easier (Overall)
  - File that contains all the emails to send to.
  - We're not on the mailing lists so we gotta make do.
  - Button to send (With confirmtion)


Will reuse the email sending component + events generation from previous mail generator.
Will add a new frontend using flask.
-> UI for adding elements, modifies a .YAML file which will be used to generate the appropriate HTML.
-> Can also directly modify the YAML file. 
-> Always show what the output looks like. 
-> A bit like an Overleaf editor? Switching between a text editor for the .YAML / a UI based one.
-> the YAML editor will be more of a in case type situation.

