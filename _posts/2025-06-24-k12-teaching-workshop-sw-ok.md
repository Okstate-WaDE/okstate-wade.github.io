---
date: 2025-06-24
title: K-12 Teaching Workshop - Water Data Analysis
categories:
toc: true
author_staff_member: Jeff Sadler
---

# Goals of this workshop session
- Introduce teachers to relevant and interesting water data in the SW OK region
- Show where to download the data
- Provide preprocessed data
- Provide examples of graphs/plots that illustrate relevant water resource principles and data visualization and analysis principles. The plots will include:
    - Line plots (time series)
    - Bar plots
    - Scatter plots
    - Combined line/bar plots

# Lake Lugert-Altus

The data that I am using for the lecture is from the Lake Lugert-Altus reservoir.

Purposes of the reservoir include:
- Flood control (e.g., spring 2015)
- Irrigation
- Recreation 

For more information about the reservoir, please see the [wikipedia page](https://en.wikipedia.org/wiki/Lake_Altus-Lugert).

<figure>
    <img src="{{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/960px-Altuslake-1.jpg" alt="Image of Lugert Altus Reservoir">
    <figcaption>Photo of Lake Altus-Lugert by James Powers <a href="https://commons.wikimedia.org/wiki/File:Altuslake-1.jpg">https://commons.wikimedia.org/wiki/File:Altuslake-1.jpg</a></figcaption>
</figure>

<figure>
    <img src="{{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/lugert_altus_watershed.jpeg" alt="Lugert Altus Watershed">
    <figcaption>Watershed of Lugert-Altus, by Ochsner et. al (2014) <a href="https://water.okstate.edu/site-files/documents/our-work/funded-projects/threats-to-the-lugert-altus-irrigation-district-2015.pdf">https://water.okstate.edu/site-files/documents/our-work/funded-projects/threats-to-the-lugert-altus-irrigation-district-2015.pdf</a></figcaption>
</figure>

# Data from the reservoir
## Data Source: The US Army Corps of Engineers
The US Army Corps of Engineers (USACE) monitors the reservoir and publishes the data on [their web page](https://www.swt-wc.usace.army.mil/ALTU.lakepage.html).
They collect data on an hourly and daily basis.
You can access the hourly data via [this webpage](https://www.swt-wc.usace.army.mil/webdata/gagedata/ALTO2.current.html) and the daily data via [this webpage](https://www.swt-wc.usace.army.mil/charts/?monthly&proj=ALTU).
They have data starting in 1994.

## Data Gathering using a For Loop in a Python Program
The USACE only makes their daily data available in monthly reports, publishing one month per report. 
To see long-term data (or even just one year of data), we needed a way to get all of the monthly reports and stitch them together into a single dataset.
To do this, we wrote a small computer program in Python. 
This program manipulated the URL (i.e., the website address) to get the data for each month of each year.

The URL for April 2025 is `https://www.swt-wc.usace.army.mil/charts/bins/ALTUAPR25.txt`.
The URL for May 2013 is `https://www.swt-wc.usace.army.mil/charts/bins/ALTUMAY13.txt`.
There is a pattern here. 
Can you see it?
To make it more general, we can substitute a placeholder (a "variable" in programming) in the months and year places: `https://www.swt-wc.usace.army.mil/charts/bins/ALTU{MONTH}{YEAR}.txt`

Then we can write a `for` loop to get the data from each month of each year and stitch them all together.
Here is some pseudocode for what that looked like

```
for MONTH in months from JAN to FEB
    for YEAR in years from 1994 to 2024
        update the generic URL ->  `https://www.swt-wc.usace.army.mil/charts/bins/ALTU{MONTH}{YEAR}.txt`
        retrieve the data at that URL
        add the data to the combined collection
```



## Data Structure
The data columns in the daily summaries include information on pool elevation, storage, releases, evaporation, inflow and rainfall. Below is a table describing the different columns. This information is considered _metadata_ or information about the data.

Column label | Description | Unit | Dimension
:-- | :-- | :-- | :--
pool_0800 | pool elevation at 0800 | feet above National Geodetic Vertical Datum of 1929 (NGVD) | length 
pool_2400 | pool elevation at 2400 | feet above National Geodetic Vertical Datum of 1929 (NGVD) | length 
storage | reservoir storage volume at 2400 | acre-feet | volume
releases_power | power releases | daily average cubic feet per second (CFS) | flow rate (volume per time)
releases_total | total releases | daily average cubic feet per second (CFS) | flow rate (volume per time)
evaporation | total evaporation from reservoir from 0800 to 0800 | inches | length 
inflow | inflow into the reservoir  | daily average cubic feet per second (CFS) | flow rate (volume per time)
rain_dam | rainfall recorded at dam 0700 to 0700 | inches | length 
rain_bsn | rainfall recorded across basin 0700 to 0700 | inches | length 

## Data Files

File Num | Description | Link
:-- | :-- | :--
1 | raw data 1994-2024 | [lugert_altus_data_1994_2024.csv]({{ site.baseurl }}/assets/data/250624_k12_wkshp/lugert_altus_data_1994_2024.csv)
2 | cleaned data 1994-2024 (removed outliers)| [lugert_altus_data_1994_2024_CLN.csv]({{ site.baseurl }}/assets/data/250624_k12_wkshp/lugert_altus_data_1994_2024_CLN.csv)
3 | cleaned data 1995 (removed outliers)| [lugert_altus_data_1995_CLN.csv]({{ site.baseurl }}/assets/data/250624_k12_wkshp/lugert_altus_data_1995_CLN.csv)
4 | cleaned data August 1995 (removed outliers)| [lugert_altus_data_Aug_1995_CLN.csv]({{ site.baseurl }}/assets/data/250624_k12_wkshp/lugert_altus_data_Aug_1995_CLN.csv)


# Data Analysis and Visualization
## Reservoir Storage 1994-2024 (line plot)
![Reservoir storage 94-24]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/storage_time_series.png)
## Rainfall at reservoir 1994-2024 (bar plot)
![Reservoir rainfall 94-24]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/annual_average_rainfall.png)
## Reservoir storage, rainfall, and releases 1995 (line plots and barplots)
![Reservoir storage 95]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/1995_storage.png)
![Reservoir storage 95 with rain]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/storage_rain_1995.png)
![Reservoir storage 95 with rain and releases]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/storage_rain_releases_1995.png)
## Rain - inflow relationship (line and barplot)
![Reservoir inflow 95 with rain]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/rainfall_inflow.png)
## Storage - Elevation relationship (scatter plot)
![storage elevation raw]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/storage_elevation_raw.png)
![storage elevation clean]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/storage_elevation.png)
![storage elevation colored by year]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/storage_elevation_color.png)
## Rainfall - Inflow Model (scatter plot)
![predicting inflow with rainfall]({{ site.baseurl }}/assets/images/blog/250624_k12_wkshp/rainfall_inflow_model.png)



