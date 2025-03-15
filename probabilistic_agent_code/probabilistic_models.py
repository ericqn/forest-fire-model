import pandas as pd
import numpy as np


def calculate_conditional_prob(data, x, area, x_range, boolean,target_var_count):
    """
    Given a dataframe, this function aims to calculate the conditional probability 
    of a given variable, x. 

    Args:
        data (pd.DataFrame): A pd.dataframe that contains data such as the FFMC, DMC, DC, ISI and a boolean int 
            representing if a fire is burning
        x (str): The name of the variable that is having the conditional variable found for.
        area (str): The name of the column that contains boolean ints representing if a fire is burning or not.
        x_range (int): The number of bins used by the variable.
        boolean (bool): Determines if attempting to find P(x|area = 1) or P(x | area = 0). When set to 1, the 
            P(x|area = 1) is calculated for each x. Else, P(x|area = 0) is calculated for each x.
        target_var_count (int): The number of times the target variable has occured.
    Returns:
        dict: Each key in the dict corresponds to a bin in data. The corresponding value for a given key is the 
        probability of P(x = key|area = boolean).
    """
    count_dictionary = {}
    probability_dictionary = {}
    conditional_prob_dictionary = {}
    for j in range(x_range):
        count_dictionary[j] = [0,0]
        conditional_prob_dictionary[j] = 0
    area_counter = 0
    for i in range(len(data)): 
        if data.iloc[i][area] == boolean:
            ##Occurences where area = 1
            count_dictionary[data.iloc[i][x]][0] += 1
            area_counter += 1
        else:
            ##Occurences where area = 0
            count_dictionary[data.iloc[i][x]][1] += 1

    for j in range(x_range):
        if (count_dictionary[j][0] != 0 and count_dictionary[j][1] != 0):
            conditional_prob_dictionary[j] = count_dictionary[j][0]/target_var_count
    return conditional_prob_dictionary


def calculate_lookup_table(conditional_variable, conditional_probabilty_list,target_variable,target_variable_prob):
    temp_dict = {}
    final_prob = float(target_variable_prob)
    for i in conditional_probabilty_list:
        key = f"P({target_variable}|{conditional_variable} = {i})"
        temp_dict[key] = conditional_probabilty_list[i]
        if conditional_probabilty_list[i] > 0:
            final_prob = final_prob * conditional_probabilty_list[i]
    targetKey = f"P({target_variable}|{conditional_variable} = 1, {conditional_variable} = 2, {conditional_variable} = 3,{conditional_variable} = 4, {conditional_variable} = 5)"
    temp_dict[targetKey] = final_prob
    return temp_dict


def calculate_naive_bayes(
        conditional_variables: list[int],
        FFMC_condlist: dict,
        DMC_condlist: dict,
        DC_condlist: dict,
        ISI_condlist: dict,
        target_variable_prob: float
    ):
    """
    This uses the Naive Bayes Assumption to estimate the parameters of a Bayes net.

    Args:
        conditional_variables (list[int]): A list of int from 1-5, where each int represents the severity of a corresponding weather index.
            Index [0] corresponds to FFMC, Index [1] to DMC, Index [2] to DC, and Index [3] to ISI.
        FFMC_condlist (dict): A dictionary corresponding to FFMC, containing the conditional probability for a given severity.
        DMC_condlist (dict): A dictionary corresponding to DMC, containing the conditional probability for a given severity.
        DC_condlist (dict): A dictionary corresponding to DC, containing the conditional probability for a given severity.
        ISI_condlist (dict): A dictionary corresponding to ISI, containing the conditional probability for a given severity.
        target_variable_prob (float): The probability that the target variable (a fire) has occurred.

    Returns:
        float: The estimated conditional probability of the target variable (fire) given the conditional variables.
    """
    FFMC = conditional_variables[0]
    DMC = conditional_variables[1]
    DC = conditional_variables[2]
    ISI = conditional_variables[3]
    
    conditional_FFMC = FFMC_condlist[FFMC]
    conditional_DMC = DMC_condlist[DMC]
    conditional_DC = DC_condlist[DC]
    conditional_ISI = ISI_condlist[ISI]
    conditional_target_var = target_variable_prob * conditional_FFMC *conditional_DMC * conditional_DC * conditional_ISI

    return conditional_target_var

def max_log_likelihood(
        fire: bool,
        indices: dict[str: list],
        data_array: np.array
):
    """
    This function aims to calculate the probability of a fire based on the indices using the maximum log likelihood algorithm

    Args:
        fire (bool): Represents whether or not a fire has occurred or not
        indices (dict): A dict where the keys the specified fire indices and the values are the severity values (from 0-5)
        data_array (np.array): Obtained from utils.fire_dataloader()
    
    Returns:
        probability (float): The estimated conditional probability of the target variable (fire) given the indices

    Example Usage:
        indices = {'FFMC': [3, 4], 'DMC': [4, 5], 'DC': [3, 4, 5], 'ISI': [3, 4]}
        fire_array = fire_dataloader('data/forestfires.csv', to_array=True)
        
        result = max_log_likelihood(True, indices, fire_array)
        --> result = 0.5356
    """
    count_parents_and_fire = 0
    count_parents = 0

    # Compute P(fire | FFMC, DMC, DC, ISI) by counting data
    for item in data_array:
        item_FFMC = item[0]
        item_DMC = item[1]
        item_DC = item[2]
        item_ISI = item[3]
        item_fire = item[4]

        if item_FFMC in indices['FFMC'] and item_DMC in indices['DMC'] and \
            item_DC in indices['DC'] and item_ISI in indices['ISI']:
            count_parents += 1
            if item_fire == fire:
                count_parents_and_fire += 1

    if count_parents == 0:
        print('Not enough data')
        return 0
    else:
        return count_parents_and_fire / count_parents