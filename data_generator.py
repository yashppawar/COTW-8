import pandas as pd
import numpy as np
import random

def are_limits_valid(*limits) -> bool:
    """
    Takes individual limits as arguments and return if all the limits are valid or not
    @params
    limits:* --> unlimited number of limits which are to be tested
    """
    for limit in limits:
        if not (limit is int or limit is float):
            return False
    
    return True


def validate_limits(limits:tuple) -> bool:
    if len(limits) != 2:
        raise ValueError('The limits are not the reuired shape')
    if are_limits_valid(*limits):
        raise ValueError('Invalid limit types')


def get_random_data(nrows:int, limits:tuple = (0, 100)) -> np.ndarray:
    """
    generate_random_data(nrows:int, limits:tuple) will retun an np.ndarray of size (nrows,) and will contain the values between limits[0] and limits[1];
    @params
    nrows:int --> the length of the data expected
    limits: tuple --> the tuple containing the min and max value which should be in the expected array

    Example:
    >>> get_random_data(10, (1, 10)) 
    array([4, 8, 3, 2, 2, 2, 2, 4, 6, 6])
    """
    validate_limits(limits)

    return np.random.randint(*limits, size=(nrows))


def get_unique_random_numbers(n:int, limits:tuple) -> list:
    """
    returns a list of unique random numbers of length n which have numbers between the given limits
    """
    numbers = set()
    validate_limits(limits)
    if limits[1] - limits[0] < n:
        raise ValueError('invalid set of limits, this will cause this function to run infinately!')

    while len(numbers) < abs(n):
        numbers.add(random.randrange(*limits))

    return list(numbers)


def add_noise(data:np.ndarray, ambiguous_values:list or tuple = (0, -100, -1), noise:float=0.3) -> np.ndarray:
    """
    Adds noise to the given data, adds some ambiguous values and NaN values to the data.
    @params
    data:np.ndarray --> The data to which noise is to be added
    ambigous_values:list or tuple --> the values to which the data is to be replaced
    noise:float --> between 0 and 1, size to which noise is to be added 
    """
    # if (noise is not float) or (not (0 >= noise <= 1)):
    #     raise ValueError('Invalid noise percentage')

    data = data.copy().astype('float')
    size = len(data)
    noise = int(size * noise)
    indices_to_add_noise = get_unique_random_numbers(noise, (0, size))

    iter_no = 0
    for index in indices_to_add_noise:
        iter_no+=1
        if iter_no % 4 == 0:  # 20% of the noise is NaN values
            data[index] = (np.nan)
            continue

        data[index] = random.randrange(*ambiguous_values)
        

    return data


if __name__ == "__main__":
    # print(len(get_random_data(200, (1, 10))))
    # print(len(get_unique_random_numbers(10, (0, 17))))
    # print(add_noise(get_random_data(20, (1, 10)), (0, -10, -1))) # cannot convert to integer type
    studying_hours = get_random_data(200, (0, 10))
    studying_hours = add_noise(studying_hours, (0, -5, -1), noise=0.15)  # add 20% noise of negative ambigious values
    studying_hours = add_noise(studying_hours, (11, 25, 1), noise=0.15)  # add 20% noise of positive ambigious values

    average_marks = get_random_data(200, (0, 100))
    average_marks = add_noise(average_marks, (0, -50, -1), noise=0.15)  # add 20% noise of negative ambigious values
    average_marks = add_noise(average_marks, (100, 150, 1), noise=0.15)  # add 15% noise of positivee ambigious values

    dataframe = pd.DataFrame({"Hours": studying_hours, "marks": average_marks})
    dataframe.to_csv('./study_data.csv', index=False)
    print(dataframe)
