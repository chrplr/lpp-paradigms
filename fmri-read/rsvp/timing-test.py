import bbtkv2

bb = bbtkv2.BlackBoxToolKit()

bb.adjust_thresholds()  # adjust the thresholds manually
bb.clear_timing_data()  # clear the internal memory of the BBTKv2
text = bb.capture(30)   # start capturing events for 30sec

# convert the results into human readable formats:
df1 = bbtkv2.capture_output_to_dataframe(text)
processed_events = bbtkv2.capture_dataframe_to_events(df1)
print(processed_events)