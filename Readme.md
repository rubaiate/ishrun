### Interactive Shell Runner

### Commands

#### Docker
|Command | Description |  
|--------|-------------|
|dcs| docker start |
|dck| docker stop |

#### kubernet
|Command | Description |  
|--------|-------------|
|kcs| kubectl scale 1 |
|kck| kubectl scale 0 |
|kcl| kubectl logs |

#### Command
|Command | Description |  
|--------|-------------|
|isl| run last command |

### Register alias

#### Temporary
    export ISH_RUN_SCRIPTS=<Script folder>
    
    alias dcs="$ISH_RUN_SCRIPTS/shlrunner.py dci start"
    alias dck="$ISH_RUN_SCRIPTS/shlrunner.py dci stop"
    alias kcs="$ISH_RUN_SCRIPTS/shlrunner.py kci 1"
    alias kck="$ISH_RUN_SCRIPTS/shlrunner.py kci 0"
    alias kcl="$ISH_RUN_SCRIPTS/shlrunner.py kclogs"
    alias isl="$ISH_RUN_SCRIPTS/islast.py"
    
    
Save them in bashrc for permanent links