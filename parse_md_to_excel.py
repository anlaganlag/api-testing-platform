import pandas as pd
import re
import os
from openpyxl.styles import Font, Alignment, Border, Side

def parse_markdown_to_excel(markdown_file, excel_file):
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize lists for each column
    modules = []  # 课程模块
    topics = []   # 课程主题
    outlines = [] # 课程大纲
    descriptions = [] # 内容说明
    
    # Split content by lines for processing
    lines = content.split('\n')
    
    current_module = ""
    current_topic = ""
    current_outline = ""
    current_description = ""
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        # Skip empty lines
        if not line:
            continue
        
        # Check if first line is the title and skip it
        if i == 1 and "财富管理系列课程" in line:
            continue
            
        # Identify module (卷一, 卷二, etc.)
        if line.startswith('卷') and ('：' in line or ':' in line):
            if current_outline and current_description:
                # Save previous entry
                modules.append(current_module)
                topics.append(current_topic)
                outlines.append(current_outline)
                descriptions.append(current_description)
                current_description = ""
            
            current_module = line
            continue
        
        # Identify topic (第1章, 第2章, etc.)
        if line.startswith('第') and '章' in line:
            if current_outline and current_description:
                # Save previous entry
                modules.append(current_module)
                topics.append(current_topic)
                outlines.append(current_outline)
                descriptions.append(current_description)
                current_description = ""
            
            current_topic = line
            continue
        
        # Identify outline (1.1, 1.2, etc.)
        outline_pattern = r'^\s*\d+\.\d+.*'
        if re.match(outline_pattern, line):
            if current_outline and current_description:
                # Save previous entry
                modules.append(current_module)
                topics.append(current_topic)
                outlines.append(current_outline)
                descriptions.append(current_description)
                current_description = ""
            
            current_outline = line
            continue
        
        # Everything else is considered description
        if current_outline:
            if current_description:
                current_description += " " + line
            else:
                current_description = line
    
    # Add the last entry if exists
    if current_outline and current_description:
        modules.append(current_module)
        topics.append(current_topic)
        outlines.append(current_outline)
        descriptions.append(current_description)
    
    # Create a DataFrame with Chinese headers
    df = pd.DataFrame({
        '课程模块': modules,
        '课程主题': topics,
        '课程大纲': outlines,
        '内容说明': descriptions
    })
    
    # Clean up the outline entries - remove leading spaces
    df['课程大纲'] = df['课程大纲'].str.strip()
    
    # Fill forward the module and topic values
    df['课程模块'] = df['课程模块'].ffill()
    df['课程主题'] = df['课程主题'].ffill()
    
    # Save to Excel with formatting
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        
        # Set column widths
        worksheet.column_dimensions['A'].width = 25  # 课程模块
        worksheet.column_dimensions['B'].width = 35  # 课程主题
        worksheet.column_dimensions['C'].width = 45  # 课程大纲
        worksheet.column_dimensions['D'].width = 80  # 内容说明
        
        # Define border style
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Apply formatting to header row
        header_font = Font(name='宋体', size=11, bold=True)
        header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = thin_border
        
        # Apply formatting to data cells
        data_font = Font(name='宋体', size=11)
        data_alignment = Alignment(vertical='center', wrap_text=True)
        
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
            for cell in row:
                cell.font = data_font
                cell.alignment = data_alignment
                cell.border = thin_border
    
    print(f"Successfully converted {markdown_file} to {excel_file}")
    print(f"Total entries: {len(df)}")

if __name__ == "__main__":
    markdown_file = "data/book_outline.md"
    excel_file = "data/book_outline.xlsx"
    parse_markdown_to_excel(markdown_file, excel_file) 