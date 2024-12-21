import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

def count_plot(df, feature, title, ordered=True, ax=None):  
    plt.figure(figsize=(10,5))
    # Set the axis for the plot
    if ax is None:
        ax = plt.gca()  # If no axis is provided, use the current axis
    
    # Order the categories based on value counts if 'ordered' is True
    order = df[feature].value_counts().sort_values(ascending=False).index if ordered else None
    
    # Create the countplot
    sns.countplot(data=df, y=feature, palette='Dark2', order=order, ax=ax)
    
    # Total number of entries
    total = len(df)
    
    # Set plot labels and title
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Add percentage annotations to each bar
    for p in ax.patches:
        width = p.get_width()  # Count of each category
        percentage = (width / total) * 100  # Calculate percentage
        ax.annotate(f'{percentage:.1f}%',
                    (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2), 
                    ha='left', va='center', fontsize=12, color='black')

    plt.tight_layout()

def cross_tab_features(df,feature1,feature2):
    cross_tab= pd.crosstab(index=df[feature1], columns=df[feature2], margins=True)
    pd.crosstab(index=df[feature1], columns=df[feature2], margins=True)
    return cross_tab
def plot_crosstab(cross_tab):
    cross_tab=cross_tab.drop(columns=['All']) # drop the all column
    cross_tab=cross_tab[cross_tab.index!="All"] #drop the all index
    sns.heatmap(cross_tab, annot=True, cmap='coolwarm', fmt=".0f")
    plt.title('Crosstab Heatmap')
    plt.show()
