import ee
import datetime

# Initialize the Earth Engine module.
ee.Initialize()

# Define the time range
start_date = '1998-03-10'
end_date = '2023-12-31'

# Define the area of interest: Colombia
colombia = ee.Geometry.Polygon([
    [[-79.5, 12.6], [-66.9, 12.6], [-66.9, -4.3], [-79.5, -4.3], [-79.5, 12.6]]
])

# Load the CHIRPS dataset
chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
            .filterDate(start_date, end_date) \
            .filterBounds(colombia)

# Function to export an image to Google Drive
def export_to_drive(image, description, folder, scale=5000):
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=description,
        folder=folder,
        fileNamePrefix=description,
        region=colombia,
        scale=scale,
        maxPixels=1e12
    )
    task.start()

# Iterate over each day in the defined time range and export data
start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
current = start

while current <= end:
    day_str = current.strftime('%Y-%m-%d')
    
    # Get daily precipitation
    daily_precip = chirps.filterDate(current.strftime('%Y-%m-%d'), (current + datetime.timedelta(days=1)).strftime('%Y-%m-%d')).first()
    
    # Export the daily data to Google Drive
    export_to_drive(daily_precip, description=f'CHIRPS_{day_str}', folder='Chirps_Colombia_diario')
    
    # Move to the next day
    current += datetime.timedelta(days=1)

print('Export tasks started.')
