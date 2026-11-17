from bs4 import BeautifulSoup

data = []

file_name = "python_class_question.html"

with open(file_name) as html_file:
    soup = BeautifulSoup(html_file,'lxml')
    
    
table_rows = soup.find_all("tr")

for row in table_rows:
    day_data = {}
    day = row.find_all("td")[0]
    row_colours = row.find_all("td")[1]
    day_data[day.text] = row_colours.text.split(", ")
    
    data.append(day_data)
    


def set_colors(data:list) -> None:
    """
     . Takes in a list of formatted data .Ex [
         {
             "day" : [...colours]
         },
     ]
     iterates over this data extracts the colors for each day then returns a set of unique colors and all colors
    """
    colors = []
    for day in data:
        colors += list(day.values())[0]
     
    return list(set(colors)), colors


def get_frequency(unique_colors ,universal_colors):
    data = {}
    
    for unique in unique_colors:
        frequency = 0
        
        for universal in universal_colors:
            if unique == universal:
                frequency+=1
        
        data[unique] = frequency
        
    return data

def get_number_of_workers(data):
    
    workers_per_day = map(lambda day: len(day.values()),data)
    print(workers_per_day)







if __name__ == '__main__':
    unique_colors, all_colours = set_colors(data)
    colors_frequency = get_frequency(unique_colors,universal_colors=all_colours)
    mode_color = max(colors_frequency, key=colors_frequency.get)
    print(mode_color)