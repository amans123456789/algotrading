Indicators :

1. RSI
2. Bollinger Band
3. MACD 
4. ATR 
5. ADX
6. Stochastic Trend

How to use Indicators?

1. RSI : source - https://www.investopedia.com/terms/r/rsi.asp
         Technical indicator, used in momentum trading,that measures the speed and magnitude of a
         security's recent price changes to evaluate overvalued or undervalued conditions.
         Traditionally, an RSI above 70 indicates overbought situation and a reading below 30 indicates oversold 
         condition.
         RSI line crossing below the overbought line or above oversold line is often seen as a signal to buy or sell.
         However, RSI works best in trading ranges rather than trending markets. RSI is particularly useful in 
         identifying potential reversals or shifts in market sentiment when prices are moving within a trading range. 
         During trending markets, the RSI may provide less accurate signals, as it could indicate overbought or oversold
         conditions that persist for an extended period during strong trends.
         Reversal indication using RSI: For example, if the RSI can’t reach 70 on a number of consecutive price swings 
         during an uptrend, but then drops below 30, the trend has weakened and could be reversing lower. 
         The opposite is true for a downtrend. If the downtrend is unable to reach 30 or below and then rallies above 
         70, that downtrend has weakened and could be reversing to the upside. Trend lines and moving averages are 
         helpful technical tools to include when using the RSI in this way.
         
         Not written code on this : A bullish divergence occurs when the RSI displays an oversold reading followed by a 
         higher low that appears with lower lows in the price. This may indicate rising bullish momentum, and a break 
         above oversold territory could be used to trigger a new long position.

         A bearish divergence occurs when the RSI creates an overbought reading followed by a lower high that appears 
         with higher highs on the price.
         Example of Positive-Negative RSI Reversals :
         An additional price-RSI relationship that traders look for is positive and negative RSI reversals. A positive 
         RSI reversal may take place once the RSI reaches a low that is lower than its previous low at the same time 
         that a security's price reaches a low that is higher than its previous low price. Traders would consider this
         formation a bullish sign and a buy signal.
         Conversely, a negative RSI reversal may take place once the RSI reaches a high that is higher that its previous
         high at the same time that a security's price reaches a lower high. This formation would be a bearish sign and 
         a sell signal.

2. Bollinger Band: source - https://www.investopedia.com/terms/b/bollingerbands.asp, 
                            https://www.investopedia.com/articles/technical/102201.asp
         A Bollinger Band® is a technical analysis tool defined by a set of trendlines. They are plotted as two standard
         deviations, both positively and negatively, away from a simple moving average (SMA) of a security's price and 
         can be adjusted to user preferences.
         It is a technical analysis tool to generate oversold or overbought signals.
         When the price continually touches the upper Bollinger Band, it can indicate an overbought signal.
         If the price continually touches the lower band it can indicate an oversold signal.
         It should be used in conjugation with other indicators.
         The "squeeze" is the central concept of Bollinger Bands. When the bands come close together, constricting the 
         moving average, it is called a squeeze. A squeeze signals a period of low volatility and is considered by 
         traders to be a potential sign of future increased volatility and possible trading opportunities.
         Conversely, the wider apart the bands move, the more likely the chance of a decrease in volatility and the 
         greater the possibility of exiting a trade. These conditions are not trading signals. The bands do not indicate
         when the change may take place or in which direction the price could move.
What I did ?

RSI: (trend_functions.py) -  if RSI is above upper_limit, it is termed as Overbought else if it is below a lower limit, 
it is termed as Oversold.
Bollinger Band: if Open price is above Upper Bollinger, it is termed as Overbought else if it is below Lower Bollinger, 
it is termed as Oversold.

Additional Ideas:
RSI: Write Bullish and Bearish reversal indicator using RSI as explained in description of RSI above
     Write Bullish and Bearish momentum indicator using RSI as explained in description of RSI above
     Note: More functions on RSI written in "TimeSeries_features_on_clustered_stock_data" notebook for future use
Bollinger Band: Add the concept of squeeze with bollinger bands

Shortcomings of current iteration:
1. RSI looks only for overbought and oversold
2. Bollinger Band's squeeze concept can be added, however, squeeze is not a direct trading signal