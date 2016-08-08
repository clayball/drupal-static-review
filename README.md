# Drupal Static Review

This script is the first step used when performing a security review for a
Drupal modules. 


## How to use drupal-static-review.py

**Usage: python drupal-static-review.py [module-name] <full|good|bad|sql|input>**

Copy the default config file to config.yaml

```
cp config/default-config.yaml config/config.yaml
```


Edit review_dir to match your location.

```
review_dir: /home/<user>/code-reviews/drupal7
```
    

Run the script and provide the module's directory name.

```
python drupal-static-review views
```
    

You can also make the script executable and run it like a binary.

```
chmod u+x drupal-static-review
./drupal-static-review views
```


**View the report**

This script will generate a text file with output from the defined checks.


