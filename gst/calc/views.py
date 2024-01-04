# calc/views.py
from django.shortcuts import render
import pandas as pd
from consolemenu import ConsoleMenu, SelectionMenu
import matplotlib.pyplot as plt
import seaborn as sns

def index(request):
    # Assuming you have the path to your CSV file
    csv_file_path = 'GST\gst\calc\annexure1divisionwisesummary_csv.csv'

    try:
        # Read the CSV file into a DataFrame
        df_time = pd.read_csv(csv_file_path, delimiter='~#~', engine='python')

        # Convert 'filingmonth' column to datetime format
        df_time['filingmonth'] = pd.to_datetime(df_time['filingmonth'], format='%b-%y', errors='coerce')

        # Create a DataFrame for the X-axis
        df_timeaxis = df_time[['filingmonth']]

        # Create a DataFrame for the Y-axis (excluding 'filingmonth')
        df_cost = df_time.drop(['filingmonth'], axis=1)

        # Display available columns for the user to choose from
        print("Available columns in df_time:")
        x_axis_column = select_column("Select X-axis column from df_time", df_timeaxis.columns)

        print("\nAvailable columns in df_cost:")
        y_axis_column = select_column("Select Y-axis column from df_cost", df_cost.columns)

        # Check if the user-input columns exist in the respective DataFrames
        if x_axis_column and y_axis_column:
            # Ask the user to choose the chart type
            chart_types = ['Bar Graph', 'Bubble Graph', 'Pie Chart', 'Scatter Plot', 'Heat Map']
            chart_type_menu = SelectionMenu(chart_types, "Select Chart Type")
            chart_type_menu.show()
            selected_chart_index = chart_type_menu.selected_option
            selected_chart_type = chart_types[selected_chart_index]

            if selected_chart_type == 'Bar Graph':
                plt.bar(df_time[x_axis_column], df_cost[y_axis_column])
                plt.xlabel(x_axis_column)
                plt.ylabel(y_axis_column)
                plt.title(f'Bar Graph: {y_axis_column} vs {x_axis_column}')
                chart_image_path = 'path_to_save_chart.png'  # Provide the path to save the chart
                plt.savefig(chart_image_path)  # Save the chart to a file
                plt.close()

                # Render the HTML template with the chart or other visualizations
                context = {
                    'chart_image': chart_image_path,
                    # Add other data you want to pass to the template
                }

                return render(request, 'calc/index.html', context)
            elif selected_chart_type == 'Bubble Graph':
                # Ask the user to choose the size column for the bubble graph
                size_column = select_column("Select Size Column for Bubble Graph", df_cost.columns)
                plt.scatter(df_time[x_axis_column], df_cost[y_axis_column], s=df_cost[size_column])
                plt.xlabel(x_axis_column)
                plt.ylabel(y_axis_column)
                plt.title(f'Bubble Graph: {y_axis_column} vs {x_axis_column}')
                plt.show()
            elif selected_chart_type == 'Pie Chart':
                plt.pie(df_cost[y_axis_column], labels=df_time[x_axis_column], autopct='%1.1f%%')
                plt.title(f'Pie Chart: {y_axis_column} by {x_axis_column}')
                plt.show()
            elif selected_chart_type == 'Scatter Plot':
                plt.scatter(df_time[x_axis_column], df_cost[y_axis_column])
                plt.xlabel(x_axis_column)
                plt.ylabel(y_axis_column)
                plt.title(f'Scatter Plot: {y_axis_column} vs {x_axis_column}')
                plt.show()
            elif selected_chart_type == 'Heat Map':
                # Assuming you want a heatmap for correlation
                sns.heatmap(df_cost.corr(), annot=True, cmap='coolwarm')
                plt.title('Heat Map: Correlation Matrix')
                plt.show()
            else:
                print("Invalid chart type. Please check your input.")
        else:
            print("Invalid column names. Please check your input.")
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")

    return render(request, 'calc/index.html')  # Render the HTML template without a chart

# Function to create a scrollable menu for column selection
def select_column(menu_title, column_names):
    menu = SelectionMenu(column_names, menu_title)
    menu.show()
    selected_index = menu.selected_option
    return column_names[selected_index]
