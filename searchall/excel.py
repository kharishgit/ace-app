import openpyxl

# Create a new workbook
workbook = openpyxl.Workbook()

# Select the active worksheet
worksheet = workbook.active

# Set the column headers
headers = ['Material ID', 'Previous Materials Allocation', 'Course', 'batch', 'Subject', 'select topic', 'File Type', 'Type', 'Instruction', 'Question', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'addOption', 'Answer']
worksheet.append(headers)

# Set the data rows
data = [
    [1001, 'Add Materials for a batch', 'gpsc', 'GPSC Regular a', 'indian History', 'Delhi dynasti', 'Question', 'Practice test', '', 'republic day ?', '1978', 'Option 2', 'Option 3', 'Option 4', 'Option 5', 'A'],
    ['', '', '', '', '', '', 'Question paper', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', 'Document', 'Presentation Slide', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Materials', '']
]

for row in data:
    worksheet.append(row)

# Save the workbook
workbook.save('example.xlsx')
