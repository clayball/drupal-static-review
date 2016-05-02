# Drupal7 Module Check

This script is the first step used when performing a security review for a
Drupal 7 contrib module. 


## How to use drupal-module-check.py

- Copy the default config file to config.yaml

    cp config/default-config.yaml config/config.yaml


- Edit review_dir to match your location.

    review_dir: /home/<user>/code-reviews/drupal7
    

- Run the script and provide the module's directory name.

    python drupal-module-check views
    
    You can also make the script executable and run it like a binary.
    
    chmod u+x drupal-module-check
    ./drupal-module-check views


- View the report

    This script will generate a text file with output from the defined checks.
