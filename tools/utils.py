# This module implements some additional functional for comfortable handling
# api responces. It is assumed that some getters from getters module will be 
# parametrized from corresponding yaml configuration files. Some functions 
# from this module helps user to write that files and to read from them.


from os.path import expanduser
import yaml


def write_yaml(
        df,
        column,
        name,
        path = expanduser('~')
        ):
    """
    A function used to dump some data in form of dictionaries
    to a yaml config file.
    
    Parameters
    ----------
    df : Pandas DataFrame() instance
        dataframe from which config will be constructed
    column : str
        name of certain dataframe column 
    name : str
        string for specialize a certain file
    path : str
        path to the directory in which will be saved 
        <name>.csv file (default os.path.expanduser('~') - user HOME dir)
    """
    
    # extract values for saving in config
    values = list(df[column].values)
    # prepare structure of the ouptut file
    to_yaml = {column: values}
    # prepare full name of the output file
    full_name = path + name + '.yaml'
    # dump structure to the yaml file
    with open(full_name, 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style = False)

def read_yaml(
        file_name,
        key = 'id'
        ):
    """
    A function used to get the information from yaml configure file. The assumed 
    way of using is for example - extracting list of ID's from config to 
    pass it in one of the getters
    
    
    Parameters
    ----------
    file_name : str
        full name of the file, containing it's path.
    key : str
        A key for extracting certain data from the yaml file.
        The default is 'id'.

    Returns
    -------
    templates[key] : list of str
        The list containing specified information fro yaml file

    """
    
    # read from file into templates structure
    with open(file_name) as f:
        templates = yaml.safe_load(f)
    
    # get from structure data specified by key
    return templates[key] 
