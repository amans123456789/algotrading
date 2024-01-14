Process
1. Create annual fundamental analysis csv of each stock (quarterly analysis capabilities to be added)
2. Create call put ratio data of upcoming closing data 
3. Create daily lagging indicator csv (one day prior data for training)
4. Calculate market daily indicators
5. Calculate news daily data
6. Combine all above created datas (3,4,5 to be run daily) in this service :
   a. This service should check that fundamental analysis year is relevant, call put data is upcoming and lag, market and news data should be latest
7. Run service data to calculate today's max, closing, opening , mid-day values of each stock
8. Concatenate above data and create classification sheet
9. Run above process again and again to create multiple classification sheets

Other ideas to explore:
1. Collect Knowledge graph data from marker news
2. Train LLM on news 
3. Deploy in GCP
4. Automate process in GCP
5. Create graphs to link what factor effect each of the stock