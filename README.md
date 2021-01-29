# TagSpaces CLI
TagSpaces is great, but how about the terminal users? now there's the new tool to you! the Tagspaces CLI.
which compatible with the offical sidecar format.

## How to use?
Adding tags script into your $PATH, then that it! currently support python, I'll build more version for that. or you are lazy to type command, here you go:
```bash
# bash
echo export "PATH=\$PATH":"$(pwd)/bin" > ~/.bashrc

# zsh
echo export "PATH=\$PATH":"$(pwd)/bin" > ~/.zshrc
```

## QnA

### Why only using **sidecar** ?
Because sidecar dose not effect the origin file name, while the file name become your relativity of everything, like README.md or some file links. sidecar by the other hand, that using json file to manage tags, which dose not effect the origin relativity. If you dont want to use sidecar method, then you may not need this tool for tagSpaces.

### Why using python3?
Becuase every morden computer have python3 preinstalled, so Python3 become the better options to build this tools. About the "Windows" side, I'm not consider to build it, becuase no much people are using termianl in windows (and terminal in windows is sucks, that's a common sens for sure :D )
