import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
plt.style.use('ggplot')
import joypy

name_key = {'birth_vel_max': 'Maximum Velocity',
            'birth_acc_max': 'Maximum Acceleration',
            'birth_jerk': 'Jerk',
            'max_size': 'Maximum Size',
            'birth_width': 'Birth Size',
            'searcher': 'Herbivore',
            'predator': 'Predator',
            'attack': 'Attack',
            'defense': 'Defense',
            'search_distance': 'Search Distance',
            'num_offspring_divisor': 'Number of Offspring Divisor'
            }
aggregations = ['min', 'max', 'mean']
#%%
def plot_traits(dt, traits, type):
    df=dt[dt.type == type][['generation'] + traits]
    # Aggregate by generation
    agg = df.groupby('generation').agg(['min', 'max', 'mean'])
    cols = []
    for col in traits:
        for agg_names in aggregations:
            cols.append(col + "_" + agg_names)
    agg.columns = cols
    plt.figure(figsize=(10,6))
    for trait in traits:
        sns.lineplot(agg.index, agg[trait + '_mean'], label=name_key[trait])
    plt.xlabel('Generation')
    plt.ylabel('Value')
    plt.title('Mean Traits Over Time for the ' + name_key[type])
    plt.show()
#%% 
# Plotting population at the start of the round
def plot_population(dt):
    # Num creatures over time
    grouped = dt.groupby('generation')
    out = []
    for generation, group_dt in grouped:
        out.append({'generation': generation,
                   'num_herbivores': len(group_dt[group_dt.type == 'searcher']),
                   'num_predators': len(group_dt[group_dt.type == 'predator'])})
    res = pd.DataFrame(out)
    
    plt.figure(figsize=(10,6))
    sns.lineplot(res.generation, res.num_herbivores, label='Number of Herbivores')
    sns.lineplot(res.generation, res.num_predators, label='Number of Predators')
    plt.xlabel('Generation')
    plt.ylabel('Number of Creatures')
    plt.title('Population over Time')
    plt.show()
#%%
# Todo: make sure eaten are represented here
def plot_survival(dt):
    grouped = dt.groupby('generation')
    out = []
    for generation, group_dt in grouped:
        out.append({'generation': generation,
                   'num_survived': len(group_dt[group_dt.status == 'alive']),
                   'num_died_of_hunger': len(group_dt[group_dt.status == 'dead']),
                   'num_died_from_being_eaten': len(group_dt[group_dt.status == 'eaten'])
                   })
    res = pd.DataFrame(out)
    
    plt.figure(figsize=(10,6))
    sns.lineplot(res.generation, res.num_survived, label='Number of Surviving Creatures')
    sns.lineplot(res.generation, res.num_died_of_hunger, label='Number of Creatures Who Died From Hunger')
    sns.lineplot(res.generation, res.num_died_from_being_eaten, label='Number of Creatures Who Were Eaten')
    plt.xlabel('Generation')
    plt.ylabel('Number of Creatures')
    plt.title('Surival Statistics over Time')
    plt.show()
#%%
def get_dist_plot(dt, trait, generation, xlim=None, ylim=None, type=None):
    if type is not None:
        df = dt[(dt.type == type) & (dt.generation == generation)]
    else:
        df = dt[dt.generation == generation]
    sns.distplot(df[trait])
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.xlabel('Value')
    plt.title('Distribution of ' + name_key[trait] + ' over time: Generation ' + str(generation))
    plt.show()
#%%
def get_joyplot(dt, trait, type=None, status=None):
    if type is not None:
        df = dt[dt.type == type]
    else:
        df = dt
    if status is not None:
        df = df[df.status == status]
    
    # Do a safety check on the data
    grouped = df.groupby('generation')
    for generation, group_dt in grouped:
        if len(group_dt) <= 1:
            df = df[df.generation != generation]
    
    labels=list(set(df.generation))
    fig, axes = joypy.joyplot(df, by='generation', column=trait, labels=labels,
                              range_style='own', grid='y', linewidth=1, legend=False, figsize=(8,8),
                              title=name_key[trait] + ' Distribution Over Time for ' + name_key[type] + str(status), 
                              colormap=cm.OrRd, fade=False)
    axes[-1].set_xlabel(name_key[trait])
    axes[int(len(axes)/2)].set_ylabel('Generation')
    plt.show()