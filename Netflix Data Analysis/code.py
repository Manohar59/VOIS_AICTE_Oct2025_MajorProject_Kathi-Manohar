# Netflix Data Analysis - Final Version (with 1 Extra Plot)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ 1. Load Dataset ------------------
print("📥 Loading dataset...")
df = pd.read_csv("Netflix_Dataset.csv")
print("✅ Dataset loaded successfully!")
print("Shape:", df.shape)
print("\n--- First 5 Rows ---")
print(df.head())

# ------------------ 2. Check Missing Values ------------------
print("\n🔍 Checking for missing values...")
print(df.isnull().sum())

# ------------------ 3. Fill Missing Values ------------------
fill_columns = ['Director', 'Cast', 'Country', 'Rating']
for col in fill_columns:
    if col in df.columns:
        df[col] = df[col].fillna('Unknown')

if 'Release_Date' in df.columns:
    df['Release_Date'] = df['Release_Date'].fillna('Unknown')

# ------------------ 4. Convert Column Names to Lowercase ------------------
df.columns = df.columns.str.lower()

# ------------------ 5. Drop Duplicates BEFORE creating list columns ------------------
df = df.drop_duplicates()

# ------------------ 6. Clean Text Columns ------------------
df['category'] = df['category'].str.strip()
df['type'] = df['type'].str.strip()

# ------------------ 7. Basic Insights ------------------
print("\n🎬 Category Counts:")
print(df['category'].value_counts())

print("\n⭐ Top 10 Countries with Most Titles:")
if 'country' in df.columns:
    print(df['country'].value_counts().head(10))

# ------------------ 8. Create Genre List (AFTER cleaning duplicates) ------------------
genre_col = 'type'
if genre_col in df.columns:
    df['genre_list'] = df[genre_col].apply(lambda x: [i.strip() for i in str(x).split(',')])
else:
    print(f"⚠️ Column '{genre_col}' not found!")

# ------------------ 9. Visualizations ------------------

## (1) Count of Movies vs TV Shows
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='category', palette='viridis')
plt.title("Distribution of Movies and TV Shows on Netflix")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

## (2) Top 10 Countries by Content Count
if 'country' in df.columns:
    top_countries = df['country'].value_counts().head(10)
    plt.figure(figsize=(8, 4))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette='mako')
    plt.title("Top 10 Countries by Netflix Titles")
    plt.xlabel("Number of Titles")
    plt.ylabel("Country")
    plt.show()

## (3) 📈 NEW PLOT: Trend of Movies vs TV Shows Over Years
if 'release_date' in df.columns:
    df['year'] = df['release_date'].apply(lambda x: str(x)[-4:] if str(x)[-4:].isdigit() else None)
    trend = df.groupby(['year', 'category']).size().reset_index(name='count')
    trend = trend.dropna(subset=['year'])

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=trend, x='year', y='count', hue='category', marker='o')
    plt.title("Trend of Movies vs TV Shows Added to Netflix Over the Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Titles Added")
    plt.grid(True)
    plt.show()

# ------------------ 10. Save Cleaned Data ------------------
df.to_csv("cleaned_netflix_data.csv", index=False)
print("\n💾 Cleaned data saved as 'cleaned_netflix_data.csv'.")
print("✅ Analysis completed successfully!")
