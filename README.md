# Drupal Static Review

This script is the first step used when performing a security review for a
Drupal module. A report will be saved to the reports/ directory identifying
the file and line number where a string of interest is found. For example,

```
/home/XXXX/drupal/drupal7/contrib/ctools/ctools.install query at line: 196
$result = db_query('SELECT status FROM {system} WHERE name = :name', array(':name' => 'panels_views'))->fetchField();


[*] End report for /home/XXXX/drupal/drupal7/contrib/ctools/ctools.install 
```

Other features will include:

- identify menu_path URLs
- locate input forms

The goal of these results is to import them into a soon-to-be-developed tool
for further processing.

Note: this project currently target Drupal 7.


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


