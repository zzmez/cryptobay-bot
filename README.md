# REQUIREMENTS
pip3 install conda  
conda create -n py39 anaconda  
conda activate py39

Create a new ipynb (notebook and initilize it like this)

```
from include.global_functions import *

if __name__ == "__main__":
    my_driver = init_driver()
    switch_account(my_driver, 4)
```