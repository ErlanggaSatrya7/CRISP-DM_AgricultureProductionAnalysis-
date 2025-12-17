import matplotlib.pyplot as plt
import seaborn as sns

def histogram(df, column, title):
    """Generates a histogram for a given column."""
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column], kde=True)
    plt.title(title)
    return plt

def boxplot(df, column, title):
    """Generates a boxplot for a given column."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df[column])
    plt.title(title)
    return plt
