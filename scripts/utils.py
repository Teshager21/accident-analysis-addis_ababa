import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime

import sys

def is_colab():
  """Checks if the code is running in Google Colab.

  Returns:
      bool: True if running in Colab, False otherwise.
  """
  try:
    # Colab specific package
    from google.colab import drive 
    print("Running on Google Colab")
    return True
  except ImportError:
    print("Running on local machine")
    return False
         



def count_plot(df, feature, title, ordered=True, ax=None, hue=None, figsize=(10, 5)):
    # If no Axes object is provided, create a new figure and axis with the specified size
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        own_fig = True
    else:
        own_fig = False

    # Determine the order of categories based on value counts if 'ordered' is True
    order = df[feature].value_counts().sort_values(ascending=False).index if ordered else None

    # Create the countplot
    sns.countplot(data=df, y=feature, palette='Dark2', order=order, ax=ax, hue=hue)

    # Total number of entries
    total = len(df)

    # Set plot labels and title
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
    ax.set_title(prettifyTitle(title), fontsize=16)
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Add percentage annotations to each bar
    for p in ax.patches:
        width = p.get_width()  # Count of each category
        percentage = (width / total) * 100  # Calculate percentage
        ax.annotate(f'{percentage:.1f}%',
                    (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', fontsize=12, color='black')

    # Adjust layout and display the plot if it's a standalone figure
    if own_fig:
        plt.tight_layout()
        plt.savefig(f"images/{ax.get_title()}.png", dpi=300, bbox_inches='tight')  # High-resolution save
        plt.show()


def cross_tab_features(df,feature1,feature2):
    cross_tab= pd.crosstab(index=df[feature1], columns=df[feature2], margins=True)
    pd.crosstab(index=df[feature1], columns=df[feature2], margins=True)
    return cross_tab

def plot_crosstab(cross_tab, ax=None):
  """
  Plots a crosstab heatmap with annotations.

  Args:
      cross_tab (pandas.crosstab): The crosstabulation table to visualize.
      ax (matplotlib.axes.Axes, optional): The axes object to plot on.
          If not provided, a new figure will be created.
  """

  # Drop 'All' columns and rows if they exist
  cross_tab = cross_tab.drop(columns=['All'], errors='ignore')  # Handle potential 'All' absence
  cross_tab = cross_tab[cross_tab.index != "All"]  # Handle potential 'All' absence

  # Create a new figure and axes if not provided
  if ax is None:
    fig, ax = plt.subplots()

  # Generate the heatmap
  sns.heatmap(cross_tab, annot=True, cmap='coolwarm', fmt=".0f", ax=ax)
  ax.set_title('Crosstab Heatmap')

  # Display the plot (only if not using an external subplot)
  if ax is None:
    plt.savefig(f"images/{ax.get_title()}.png", dpi=300, bbox_inches='tight')  # High-resolution save
    plt.show()


def histogram_plot(df, feature, hue, ax=None):
    """
    Plots a stacked bar chart with percentages on top of each bar, allowing for subplot integration.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        feature (str): The feature to group by on the x-axis.
        hue (str): The feature to group by on the color of the bars.
        ax (matplotlib.axes.Axes, optional): The axis to plot on. If None, creates a new plot.
    """
    # Create a pivot table to calculate counts
    pivot_table = df.groupby([feature, hue]).size().unstack(fill_value=0)

    # Get total counts for each group in the feature
    total_counts = pivot_table.sum(axis=1)

    # Normalize counts to proportions
    proportions = pivot_table.div(total_counts, axis=0)

    # a vibrant colormap
    colors = sns.color_palette("Dark2", n_colors=proportions.shape[1])

    # If no axis is provided, create a new one
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 7))

    # Plot the stacked bar chart
    proportions.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        color=colors,
        edgecolor='black',
        linewidth=0.5,
        width=0.8
    )

    # Add percentage labels to each section of the bars
    for container in ax.containers:
        for bar in container:
            if bar.get_height() > 0:  # Avoid adding labels to empty bars
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height +0.02,
                    f"{height:.1%}",  # Display percentage
                    ha='center',
                    va='center',
                    fontsize=12,
                    color='white',
                    weight='bold'
                )

    # Customize the plot appearance
    ax.set_title(f'{prettifyTitle(hue)} Distribution by {prettifyTitle(feature)}', fontsize=16, weight='bold')
    ax.set_xlabel({prettifyTitle(feature)}, fontsize=12)
    plt.savefig(f"images/{ax.get_title()}.png", dpi=300, bbox_inches='tight')  # High-resolution save

def print_uniques(df):
    """
    Displays the unique values of each column in a Pandas DataFrame.

    Args:
        df: The Pandas DataFrame.

    Returns:
        A styled Pandas DataFrame showing the unique values.
        Returns None if the input is not a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        print("Input must be a Pandas DataFrame.")
        return None

    uniques=[]
    for i in df.columns:
        uniques.append(df[i].unique())
    uniques_df=pd.Series(data=uniques,index=df.columns,name='Values')
    pd.set_option('display.max_colwidth', None) 
    styled_df = uniques_df.to_frame().style.set_properties(**{'text-align': 'left'})
    return styled_df

def prettifyTitle(str):
    """Capitalizes the first letter of every word in a string and strip underscores
Args:
    text: The input string.

Returns:
    The string with the first letter of each word capitalized, or the
    original string if it's None or empty with the underscoes stripped.
"""
    str=str.replace('_',' ')
    if not str:  # Check for None or empty string
        return str

    words = str.split()  # Split the string into a list of words
    capitalized_words = [word.capitalize() for word in words] #Capitalize every word
    return " ".join(capitalized_words)  # Join the words back into a string


# print(modifyTitle('accident_severity Distribution by accident_cause'))
   
    
