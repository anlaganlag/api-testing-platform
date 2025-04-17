import pandas as pd

# Create sample data
data = {
    'chapter_number': [1, 2, 3],
    'chapter_title': [
        'Introduction to the Topic',
        'Core Concepts and Fundamentals',
        'Advanced Applications'
    ],
    'chapter_outline': [
        'Overview of the field\nKey historical developments\nWhy this topic matters today',
        'Basic principles and theories\nFundamental concepts\nPractical examples',
        'Real-world applications\nCase studies\nFuture directions'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('data/book_outline_template.xlsx', index=False)
print("Template created at data/book_outline_template.xlsx") 