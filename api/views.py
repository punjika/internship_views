
import pandas as pd
import matplotlib.pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from io import BytesIO

# Load Excel File
EXCEL_FILE = '2024 Internship Report updated on 17-8-2024 (1).xlsx'


@api_view(['GET'])
def generate_graph(request):
    try:
        # Load the Excel file
        df = pd.read_excel(EXCEL_FILE)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces in column names
        print("Excel file loaded successfully.")
    except FileNotFoundError:
        print("Error: Excel file not found.")
        return Response({"error": "Excel file not found."}, status=404)
    
    # Log column names for reference
    print("Columns in the DataFrame:", df.columns)

    # Get filters from request
    batch = request.GET.get('Year')
    branch = request.GET.get('Branch')
    domain = request.GET.get('Internship Title/Domain')
    mode = request.GET.get('Mode (Online / Offline)')
    paid_status = request.GET.get('Paid / Unpaid*')
    graph_type = request.GET.get('type')

    # Apply filters
    if batch:
        df = df[df['Year'] == batch]
    if branch:
        df = df[df['Branch'] == branch]
    if domain:
        df = df[df['Internship Title/Domain'] == domain]
    if mode:
        df = df[df['Mode (Online / Offline)'] == mode]
    if paid_status:
        df = df[df['Paid / Unpaid*'] == paid_status]

    # Check if data exists after filtering
    if df.empty:
        return Response({"error": "No data found for the given filters."}, status=404)

    # Generate graphs based on type
    plt.figure(figsize=(10, 6))
    if graph_type == 'bar':
        # Bar chart: Branch-wise internship count
        branch_counts = df['Branch'].value_counts()
        branch_counts.plot(kind='bar', color='skyblue')
        plt.title('Internship Distribution by Branch')
        plt.xlabel('Branch')
        plt.ylabel('Number of Internships')
        print("Branch-wise internship counts:\n", branch_counts)
    elif graph_type == 'pie':
        # Pie chart: Internship mode distribution
        mode_counts = df['Mode (Online / Offline)'].value_counts()
        mode_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Internship Mode Distribution')
        print("Internship mode percentages:\n", mode_counts / mode_counts.sum() * 100)
    elif graph_type == 'line':
        # Line chart: Year-wise internship trend
        year_counts = df.groupby('Year')['Internship Title/Domain'].count()
        year_counts.plot(kind='line', marker='o', color='green')
        plt.title('Year-wise Internship Trend')
        plt.xlabel('Year')
        plt.ylabel('Number of Internships')
        print("Year-wise internship counts:\n", year_counts)
    elif graph_type == 'scatter':
        # Scatter plot: Internship hours vs Credits earned
        plt.scatter(df['Total Number of Hours (A+B)'], df['Credits earned'], color='purple')
        plt.title('Internship Hours vs Credits Earned')
        plt.xlabel('Total Number of Hours (A+B)')
        plt.ylabel('Credits Earned')
        print("Scatter plot: Internship hours vs Credits earned")
    elif graph_type == 'hist':
        # Histogram: Distribution of Total Hours
        df['Total Number of Hours (A+B)'].plot(kind='hist', bins=10, color='orange')
        plt.title('Distribution of Total Internship Hours')
        plt.xlabel('Total Number of Hours')
        plt.ylabel('Frequency')
        print("Histogram: Distribution of Total Internship Hours")
    else:
        return Response({"error": "Invalid graph type."}, status=400)

    # Save the graph to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    # Return the graph as a response
    return HttpResponse(buffer, content_type='image/png')



# import pandas as pd
# import matplotlib.pyplot as plt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import HttpResponse
# from io import BytesIO

# # Load Excel File
# EXCEL_FILE = '2024 Internship Report updated on 17-8-2024 (1).xlsx'

# @api_view(['GET'])
# def generate_graph(request):
#     # Load data from Excel
#     try:
#         df = pd.read_excel(EXCEL_FILE)
#     except FileNotFoundError:
#         return Response({"error": "Excel file not found."}, status=404)
    
#     # Get filters from request
#     batch = request.GET.get('batch')
#     department = request.GET.get('Branch')
#     domain = request.GET.get('Internship Title/Domain')
#     mode = request.GET.get('Mode (Online / Offline)')  # Online/Offline
#     graph_type = request.GET.get('type')  # Type of graph
    
#     # Apply filters
#     if batch:
#         df = df[df['Batch'] == batch]
#     if department:
#         df = df[df['Department'] == department]
#     if domain:
#         df = df[df['Domain'] == domain]
#     if mode:
#         df = df[df['Mode'] == mode]

#     # Check if data is available
#     if df.empty:
#         return Response({"error": "No data found for the given filters."}, status=404)

#     # Generate graph
#     plt.figure(figsize=(8, 6))
#     if graph_type == 'bar':
#         df['Domain'].value_counts().plot(kind='bar', color='skyblue')
#         plt.title('Domain Distribution')
#         plt.xlabel('Domain')
#         plt.ylabel('Count')
#     elif graph_type == 'pie':
#         df['Department'].value_counts().plot(kind='pie', autopct='%1.1f%%')
#         plt.title('Department Distribution')
#     elif graph_type == 'line':
#         df.groupby('Batch')['Domain'].count().plot(kind='line', marker='o', color='green')
#         plt.title('Batch-wise Domain Trend')
#         plt.xlabel('Batch')
#         plt.ylabel('Count')
#     else:
#         return Response({"error": "Invalid graph type."}, status=400)

#     # Save graph to a BytesIO object
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close()
#     buffer.seek(0)

#     # Return the graph as a response
#     return HttpResponse(buffer, content_type='image/png')
