# Development Guide for SecTool

## Structure

SecTool is seperated into 2 primary structures, a plugin and a parser. A plugin must have a parser
so that results can be displayed/outputted. 

### Plugins

Plugins must include the ```sectool/plugin.py``` file and inherit from the Plugin class defined in there.

The ```run``` method needs to be implemented for the plugin to be called from the main sectool.py
file. There is no need to register the plugin as the plugin loader will automatically discover
plugins in the sectool/plugins directory.

These plugins must then call ```__exec_process__(cmd)``` if they require access to an external
process. They should return data suitable for the relevant parser from the ```run``` method.

### Parsers

Parsers are similar to plugins but instead require that the 3 methods ```parse_to_markdown```, 
```parse_to_html```, and ```parse_to_json``` be implemented. These should all return their 
respective data formats.

## Flow

The Flow of the application typically works like this:

ARGS -> Start Tool -> Gather Output -> Parse Output -> Return results/e-mail results.
