import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Function to generate spiderweb diagram
def generate_spiderweb(categories, values):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Compute angle for each category
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

    # Wrap around to close the circle
    values += values[:1]
    angles += angles[:1]

    # Plot data
    ax.fill(angles, values, color='skyblue', alpha=0.6)
    ax.plot(angles, values, color='blue', linewidth=2)

    # Add labels
    ax.set_yticklabels([])
    plt.xticks(angles[:-1], categories, color='grey', size=10)

    # Save plot as image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.show()
    # Encode image as base64 string
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_data

# Sample data for multiple spiderweb diagrams
data = [
    {'categories': ['Category1', 'Category2', 'Category3'], 'values': [3, 4, 5]},
    {'categories': ['Category4', 'Category5', 'Category6'], 'values': [2, 3, 4]}
]

generate_spiderweb(data[0]['categories'],data[0]['values'])