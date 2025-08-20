# Import packages

import os

def export_to_excel(filename):

    '''
    Imports pandas dataframe and write csv file into the data directory
    
    Parameters
    ----------
    filename: pd.DataFrame
        Dataframe pulled from BLS API
    '''

    file_path = '../data'
    output_name = 'LaborForceParticipationRate.csv'
    output_path = os.path.join(file_path, output_name)

    # Check if file path exists
    if not os.path.exists(file_path):
        os.mkdirs(file_path)

    filename.to_csv(output_path, index=False)

    print(f'Dataframe saved to {file_path}')



