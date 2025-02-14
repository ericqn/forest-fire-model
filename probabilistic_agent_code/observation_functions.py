import pandas as pd
import numpy as np

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
def get_observations_given_queries(
        data: pd.DataFrame,
        query_list: list[str],
        index_list: list[list[int]],
        print_output: bool = False
    ) -> dict[str, np.array]:

    assert(len(query_list) == len(index_list)), "The length of the query list and index list must be equal"

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

"""
    Given a dataframe, this function returns a dict representing the probabilities of observations 
    given a range in the `indices` list for each query variable given from the query_list.

    Notable parameters:
    query_list : list[str]
        A list of strings from the column(s) in the DataFrame that we want to query from
        
    indices : list[int]
        List of list of indices defining the specified ranges of the `query_variable`. 
"""
def get_probabilities_given_queries(
        data: pd.DataFrame,
        query_list: list[str],
        index_list: list[list[int]],
        print_output: bool = False
    ) -> dict[str, list[int]]:

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