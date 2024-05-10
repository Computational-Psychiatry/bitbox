import os
import json
import glob

from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_retention_period(period_str):
    """_summary_

    :param period_str: time period written as a string. ie. '6 months'
    :type period_str: str
    :return: The retention period
    :rtype: datatime.timedelta object?
    """
    parts = period_str.split()
    kwargs = {parts[i + 1]: int(parts[i]) for i in range(0, len(parts), 2)}
    
    retention_period_timedelta = datetime.min + relativedelta(**kwargs) - datetime.min
    
    return retention_period_timedelta


class FileCache:
    """
        A running history of file events.

        :param json_required: If True, a JSON file is required for each file. If False, a JSON file is not required.
        :type json_required: bool
        :param retention_period: The retention period for the files. The default is '6 months'.
        :type retention_period: str
    """
    def __init__(self, json_required=True, retention_period='6 months'):
        self.json_required = json_required
        self.retention_period = parse_retention_period(retention_period)
    
    
    def check_file(self, file_path, current_metadata=None, verbose=False, json_required=None, retention_period=None):
        """_summary_

        :param file_path: _description_
        :type file_path: _type_
        :param current_metadata: _description_, defaults to None
        :type current_metadata: _type_, optional
        :param verbose: _description_, defaults to False
        :type verbose: bool, optional
        :param json_required: _description_, defaults to None
        :type json_required: _type_, optional
        :param retention_period: _description_, defaults to None
        :type retention_period: _type_, optional
        :return: _description_
        :rtype: _type_
        """
        
        # Return codes:
        # 0: file exists no need to create a new file
        # 1: file does not exist, create a new file
        # 2: file does not exist, create a new file with a new name
        
        # @TODO: check if the file is a valid file
        
        if json_required is None:
            json_required = self.json_required
        if retention_period is None:
            retention_period = self.retention_period
        else:
            retention_period = parse_retention_period(retention_period)
        
        file_name = os.path.basename(file_path)
        status = -1
        
        # check if the file exists
        if os.path.exists(file_path): # file exists
            # check if the associated JSON file exists
            json_file = '.'.join(file_path.split('.')[:-1]) + '.json'
            if os.path.exists(json_file): # JSON exits
                with open(json_file, "r") as json_file:
                    old_metadata = json.load(json_file)
                    
                # compare metadata
                same = True
                for key, value in current_metadata.items():
                    if key in old_metadata:
                        if not old_metadata[key] == value:
                            same = False
                            break           
                        
                # check if the metadata is the same        
                if same: # same metadata
                    # check the retention period
                    if 'time' in old_metadata:
                        time_created = datetime.strptime(old_metadata['time'], "%Y-%m-%d %H:%M:%S")
                        time_current = datetime.now()
                        time_difference = time_current - time_created
                        
                        if time_difference > retention_period:
                            if verbose:
                                print("An older file, %s, is found with the same metadata; however, it is older than the retention period. A new file will be generated." % file_name)
                            status = 2
                        else:
                            if verbose:
                                print("A recent file, %s, is found with the same metadata. Old file will be used." % file_name)
                            status = 0
                    else: # there is no time information in the old metadata
                        if verbose:
                            print("An older file, %s, is found with the same metadata, but missing time information. A new file will be generated." % file_name)
                        status = 2
                else: # different metadata
                    if verbose:
                        print("An older file, %s, is found with different metadata. A new file will be generated." % file_name)
                    status = 2
            else: # JSON does not exist
                if json_required: # JSON is required
                    if verbose:
                        print("An older file, %s, is found but associated JSON file is missing. You selected to require a JSON file. A new file will be generated." % file_name)
                    status = 2
                else: # JSON is not required
                    # check the retention period
                    time_created = datetime.fromtimestamp(os.path.getctime(file_path))
                    time_current = datetime.now()
                    time_difference = time_current - time_created
                    
                    if time_difference > retention_period:
                        if verbose:
                            print("An older file, %s, is found with missing JSON file; however, it is older than the retention period. A new file will be generated." % file_name)
                        status = 2
                    else:
                        if verbose:
                            print("A recent file, %s, is found with missing JSON file. Old file will be used." % file_name)
                        status = 0
        else: # file does not exist
            status = 1
                
        return status
    
    
    def store_metadata(self, file_path, base_metadata):
        """_summary_

        :param file_path: _description_
        :type file_path: _type_
        :param base_metadata: _description_
        :type base_metadata: _type_
        :raises ValueError: _description_
        """
        additonial_metadata = {'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        metadata = {**base_metadata, **additonial_metadata}
        
        json_path = '.'.join(file_path.split('.')[:-1]) + '.json'
        with open(json_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        if not os.path.exists(json_path):
            raise ValueError("Metadata file for %s could not be created." % file_path)
    
    
    def get_new_file_name(self, file_path):
        """_summary_

        :param file_path: _description_
        :type file_path: _type_
        :return: _description_
        :rtype: _type_
        """
        directory, filename = os.path.split(file_path)
        base_filename, file_extension = os.path.splitext(filename)

        # search for files with similar names in the specified directory
        matching_files = glob.glob(os.path.join(directory, f"{base_filename}*{file_extension}"))

        # count the number of matching files
        num_files = len(matching_files)
        
        # add a number to the file name
        new_file_name = os.path.join(directory, f"{base_filename}{num_files}{file_extension}")
        
        return new_file_name
    
    
    def delete_old_metadata(self, file_path):
        """_summary_

        :param file_path: _description_
        :type file_path: _type_
        :raises ValueError: _description_
        """
        json_file = '.'.join(file_path.split('.')[:-1]) + '.json'
        if os.path.exists(json_file):
            os.remove(json_file)
            
        if os.path.exists(json_file):
            raise ValueError("Old metadata file could not be deleted.")
        
    
    def delete_old_file(self, file_path):
        """_summary_

        :param file_path: _description_
        :type file_path: _type_
        :raises ValueError: _description_
        """
        # delete the old file
        if os.path.exists(file_path):
            os.remove(file_path)
            
        if os.path.exists(file_path):
            raise ValueError("Old file could not be deleted.")
        
        # delete the old metadata file
        self.delete_old_metadata(file_path)