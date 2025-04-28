import pandas as pd
import matplotlib.pyplot as plt

plot_number = 0
df = pd.read_csv('linkedin_education_data_batched.csv')
schools_series = df['Schools'].dropna()

if plot_number == 0:
    school_counts = schools_series.value_counts()

    top_n = 10  # Change this number if you want Top 5, Top 20, etc.


    school_counts.head(top_n).plot(kind='barh', figsize=(10,6), color='skyblue')
    plt.title(f'Top {top_n} Universities Among My LinkedIn Connections')
    plt.xlabel('Number of Connections')
    plt.ylabel('University Name')
    plt.gca().invert_yaxis()  # Put highest at the top
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if plot_number == 1:
    from wordcloud import WordCloud

    text = ' '.join(schools_series)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()