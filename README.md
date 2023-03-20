# dragracer-dash

This dashboard is hosted on `Render`, and can be found [here](https://dragracer-dash.onrender.com/).

## Motivation
This app was created for fans of RuPaul's Drag Race who may wish to compare the performance of queens across different seasons of the main series of the show. Through the dashboard, fans can see the unofficial [Dusted or Busted score](https://rupaulsdragrace.fandom.com/wiki/User_blog:DylanIsAMuffin/RuPaul%27s_Drag_Race_But_I_Am_Ru_%22Dusted_or_Busted%22_Scoring_System#RuPaul's_Drag_Race) (DOB) for each queen, which gives a numeric summary score to their performance across the episodes of their respective season.

For more information, see [here](https://github.com/UBC-MDS/dragracerviz/blob/main/reports/proposal.md).

## App Description
The main panel of the dashboard contains a bar graph with the DOB for each selected queen, as well as a summary table of each selected queen's number of times they finished an episode with a win, high, safe, low, or in the bottom. Queens can be selected using the filters to the left of the bar graph, and users can filter by season or by the names of the queens. Above the filters, there is an expandable info card that explains how the DOB is calculated for each queen.

## Usage
The dashboard can be accessed through the [Render link](https://dragracer-dash.onrender.com/).

By default, when the page is first opened, the dashboard shows the winner of every season. This is also the default when no seasons are chosen to avoid information overload. For more details about the DOB and how it is calculated, users can click the "Show Info" button above the filters. 

Users can also hover over each bar in the bar graph to get information about that particular queen's performance on their season. By default, the table is sorted in order of DOB and season, and should match the order of bars in the table.

## Reference
The data used in this dashboard was originally scraped from the [RuPaul's Drag Race Wiki](https://rupaulsdragrace.fandom.com/wiki/RuPaul%27s_Drag_Race_Wiki) by Steve Miller, the creator of the [dragracer] (https://cran.r-project.org/package=dragracer) R package.
