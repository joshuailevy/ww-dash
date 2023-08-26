import yaml
import os
import pickle

### this generates the hierarchy dict/pickle file
# load lineage data
with open(os.path.join('lineages.yml'), 'r') as f:
    try:
        lineage_yml = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ValueError('Error in lineages.yml file: ' + str(exc))

lineage_info = {}
for lineage in lineage_yml:
    lineage_info[lineage['name']] = {'children': lineage['children']}
pickle.dump(lineage_info,open('hierarchy.pkl','wb'))