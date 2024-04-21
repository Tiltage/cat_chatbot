import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

keys_to_filter = [
    "adaptability",
    "affection_level",
    "child_friendly",
    "dog_friendly",
    "energy_level",
    "grooming",
    "health_issues",
    "intelligence",
    "shedding_level",
    "social_needs",
    "stranger_friendly",
    "vocalisation",
    "experimental",
    "hairless",
    "natural",
    "rare",
    "rex",
    "suppressed_tail",
    "short_legs"
]

# data = [
#     {'categories': ['Category1', 'Category2', 'Category3'], 'values': [3, 4, 5]},
#     {'categories': ['Category4', 'Category5', 'Category6'], 'values': [2, 3, 4]}
# ]

# images = generate_spiderweb(data[0]['categories'],data[0]['values'])

def generate_radar_charts(json_list):

    images = []
    for obj in json_list:
        filtered = filter_json_obj(obj)
        images.append(generate_spiderweb(list(filtered.keys()), list(filtered.values())))

    return images

def filter_json_obj(json_obj):
    filtered_obj = {}
    info = json_obj['breeds'][0]
    for key, value in info.items():
        if key in keys_to_filter:
            filtered_obj[key] = value
    # print(filtered_obj)
    return filtered_obj

#Function to generate spiderweb diagram
def generate_spiderweb(categories, values):
    #Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Compute angle for each category
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

    #Wrap around to close the circle
    values += values[:1]
    angles += angles[:1]

    #Plot data
    ax.fill(angles, values, color='skyblue', alpha=0.6)
    ax.plot(angles, values, color='blue', linewidth=2)

    #Add labels
    ax.set_yticklabels([])
    plt.xticks(angles[:-1], categories, color='grey', size=10)

    #Save plot as image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    #Encode image as base64 string
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_data