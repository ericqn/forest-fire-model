import pandas as pd
import numpy as np
import scipy.stats as scipy

def get_observations_given_queries(
        data: pd.DataFrame,
        query_list: list[str],
        index_list: list[list[int]],
        print_output: bool = False
    ) -> dict[str, np.array]:

    """
    Given a dataframe, this function returns a dict representing the counts of observations 
    that fall within each specified range in the `indices` list for each query variable given 
    from the query_list.

    Notable parameters:
    query_list : list[str]
        A list of strings from the column(s) in the DataFrame that we want to query from
        
    indices : list[int]
        List of list of indices defining the specified ranges of the `query_variable`. 
    """

    assert len(query_list) == len(index_list), "The length of the query list and index list must be equal"

    observation_counts = {query: [] for query in query_list}

    for indices, query in zip(index_list, query_list):
        for i in range(0, len(indices)):
            count = 0
            lower_bound = indices[i]

            if i != len(indices) - 1:
                upper_bound = indices[i+1]
                count = data[(lower_bound <= data[query]) & (data[query] < upper_bound)].shape[0]
                if print_output:
                    print(f'Counts in {data.title} where {lower_bound} ≤ {query} < {upper_bound}]: {count}')
            else:
                count = data[(lower_bound <= data[query])].shape[0]
                if print_output:
                    print(f'Counts in {data.title} where {lower_bound} ≤ {query}: {count}')

            observation_counts[query].append(count)
        
        # For readability:
        print('')

    # convert counts to np array to work with data easier:
    for query in observation_counts.keys():
        observation_counts[query] = np.array(observation_counts[query])

    return observation_counts

def get_probabilities_given_queries(
        data: pd.DataFrame,
        query_list: list[str],
        index_list: list[list[int]],
        print_output: bool = False
    ) -> dict[str, list[int]]:
    """
    Given a dataframe, this function returns a dict representing the probabilities of observations 
    given a range in the `indices` list for each query variable given from the query_list.

    Notable parameters:
    query_list : list[str]
        A list of strings from the column(s) in the DataFrame that we want to query from
        
    indices : list[int]
        List of list of indices defining the specified ranges of the `query_variable`. 
    """

    assert(len(query_list) == len(index_list)), "The length of the query list and index list must be equal"

    total_count_data = data.shape[0]
    conditional_probabilities = get_observations_given_queries(data, query_list, index_list, print_output=False)
    
    for key in conditional_probabilities.keys():
        conditional_probabilities[key] = conditional_probabilities[key] / total_count_data

    if print_output:
        for indices, query in zip(index_list, query_list):
            for i in range(0, len(indices)):
                lower_bound = indices[i]
                if i != len(indices) - 1:
                    upper_bound = indices[i+1]
                    print(f'P({data.title} | {lower_bound} ≤ {query} < {upper_bound}]) = {np.round(conditional_probabilities[query][i], 5)}')
                else:
                    print(f'P({data.title} | {lower_bound} ≤ {query}]) = {np.round(conditional_probabilities[query][i], 5)}')
            
            # For readability:
            print('')

    return conditional_probabilities

def get_quartiles(
        data: pd.DataFrame,
        column: str
    ):
    """
    Given a dataframe, retrieves the values indicating the 25th, 50th, and 75th percentiles
    """

    # Calculate the quartiles (Q1, Q2, Q3)
    quartile25 = data[column].quantile(0.25)
    quartile50 = data[column].quantile(0.50)
    quartile75 = data[column].quantile(0.75)

    # Return the quartiles as a 3-tuple
    return (quartile25, quartile50, quartile75)

def fire_dataloader(
        data_path: str,
        to_array: bool
    ):
    """
    Loads a T x 5 dataframe (or numpy array), where T is the number of observations

    We convert the raw index values into a severity value. For example, For example, if a row has an 
    FFMC of 57, it would be replaced with a 1 as it falls in the bin with index 1 (50 to 80).

    Each observation contains the severity values of the specified key variables: FFMC, DMC, DC, ISI
    and a boolean indicating whether or not a fire occurred (1 if 'area' > 0 and 0 otherwise).
    """

    raw_data_frame = pd.read_csv(data_path)
    key_variables = ['FFMC', 'DMC', 'DC', 'ISI', 'area']

    bin_FFMC = [0,50,80,91,95,float('inf')]
    bin_DMC = [0,1,10,60,200,float ('inf')]
    bin_DC = [0,20,50,425,750, float('inf')]
    bin_ISI = [0,1,5,15,50,float('inf')]

    modified_data_frame = raw_data_frame[key_variables].copy()

    modified_data_frame['FFMC'] = np.digitize(modified_data_frame['FFMC'], bins=bin_FFMC, right=True)
    modified_data_frame['DMC'] = np.digitize(modified_data_frame['DMC'], bins=bin_DMC, right=True)
    modified_data_frame['DC'] = np.digitize(modified_data_frame['DC'], bins=bin_DC, right=True)
    modified_data_frame['ISI'] = np.digitize(modified_data_frame['ISI'], bins=bin_ISI, right=True)
    modified_data_frame['area'] = np.where(modified_data_frame['area'] > 0, 1, 0)

    modified_data_frame = modified_data_frame.rename(columns={'area': 'Fire?'})
    
    if to_array:
        return modified_data_frame.to_numpy()
    else:
        return modified_data_frame