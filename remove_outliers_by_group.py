# removes outliers based on number of standard deviations from the mean for a given variable with the specified group
def remove_outliers(dataset, var, group_var, num_std):
    # mean of var
    mean = dataset[[var,group_var]].groupby(by=group_var, as_index=False).mean()
    mean = mean.rename(columns = {var: 'mean'})
   
    #std of var
    std = dataset[[var,group_var]].groupby(by=group_var).std().reset_index(level=0)
    std = std.rename(columns = {var: 'std'})
   
    # calculate upper and lower bounds
    bounds = pd.merge(mean, std, on=group_var)
    bounds['upper'] = bounds['mean'] + (num_std * bounds['std'])
    bounds['lower'] = bounds['mean'] - (num_std * bounds['std'])
   
    # merge with dataset
    dataset = pd.merge(dataset, bounds[[group_var,'upper','lower']], on=group_var)
   
    # filter outlier records
    print('Previous record count: {}'.format(dataset.shape[0]))
    dataset = dataset[(dataset['lower'] < dataset[var]) & \
           (dataset[var] < dataset['upper'])]
    dataset.drop(columns=['upper','lower'])
    print('New record count: {}'.format(dataset.shape[0]))
    return dataset