import pandas as pd

def merge_photos(file1_path, file2_path):
    # Load the data from both CSV files
    data_df1 = pd.read_csv(file1_path)
    data_df2 = pd.read_csv(file2_path)

    # Ensure the columns 'HudHud_Media', 'Store_Front', and 'Google_Link' exist in data_df2
    if 'HudHud_Media' not in data_df2.columns:
        data_df2['HudHud_Media'] = None
    if 'Store_Front' not in data_df2.columns:
        data_df2['Store_Front'] = None
    if 'Google_Link' not in data_df2.columns:
        data_df2['Google_Link'] = None

    for index, row in data_df1.iterrows():
        longitude = row['Longitude']
        latitude = row['Latitude']
        photos_interior = row['قم بإرفاق الصور والفيديوهات للمحل من الداخل']
        photos_front = row['صورة واجهة المحل']
        place_name = row['(نسخ من قوقل ماب اذا وجد) اسم المكان']
        location = row['رابط الموقع في قوقل مابس']

        # Skip rows with NaN values in Longitude or Latitude
        if pd.isna(longitude) or pd.isna(latitude):
            print(f"Skipping row {index} due to missing Longitude or Latitude")
            continue

        # Convert photo lists to string format
        photos_interior_str = str(photos_interior.split(', ')) if pd.notnull(photos_interior) else None
        photos_front_str = str(photos_front.split(', ')) if pd.notnull(photos_front) else None

        # Check if the longitude and latitude exist in the second file
        existing_rows = data_df2[
            (data_df2['Longitude'] == longitude) & (data_df2['Latitude'] == latitude)
        ]

        if existing_rows.empty:
            # Add a new row if the coordinates do not exist
            new_row = pd.DataFrame({
                'Name': [place_name],
                'Longitude': [longitude],
                'Latitude': [latitude],
                'HudHud_Media': [photos_interior_str],
                'Store_Front': [photos_front_str],
                'Google_Link': [location]
            })
            data_df2 = pd.concat([data_df2, new_row], ignore_index=True)
            print(f"Added new row: {new_row}")
        else:
            # Update the existing row if the coordinates exist
            if photos_interior_str:
                data_df2.loc[
                    (data_df2['Longitude'] == longitude) & (data_df2['Latitude'] == latitude),
                    'HudHud_Media'
                ] = photos_interior_str
            if photos_front_str:
                data_df2.loc[
                    (data_df2['Longitude'] == longitude) & (data_df2['Latitude'] == latitude),
                    'Store_Front'
                ] = photos_front_str
            print(f"Updated row with Longitude: {longitude}, Latitude: {latitude}")

    return data_df2

# Paths to the CSV files
file1_path = '/Users/rahafmasmali/Desktop/l/Photos_24Jul_final (1).csv'  # الملف الناتج من الكود الأول
file2_path = 'POI DB - Photos - Copy of POI DB - POI_Data_ (1).csv'  # الملف الثاني

# دمج البيانات وتحديث الملف الثاني مباشرةً
merged_df = merge_photos(file1_path, file2_path)

# حفظ الملف الثاني المحدث
merged_df.to_csv(file2_path, index=False)

# طباعة DataFrame المحدث للتحقق
print("The updated DataFrame:")
print(merged_df.head())  # Print the first few rows for verification