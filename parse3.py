#TODO: Add yet another dictionary to store and report conflicts
#TODO: Get rid of the counter_dict
#TODO: Make the output automatically show whatever fields are specified in fieldsets
#TODO: Write out all the dicts as separate CSVs

import csv
counter_dict = {}
deduped_dict={}
dup_dict={}
master_lines={}
linecounter = 0
fieldsets_to_match = [[5],[0,1,5],[6,7,8,9,10],[12],[0,1,13,14,15,16,17]]
with open("full_set.csv", "rb") as csvfile:
 parser = csv.reader(csvfile)
 for this_row in parser:
  linecounter += 1
  for fieldset in fieldsets_to_match:
   token = ""
   for field in fieldset:
    token = token+this_row[field]
   if len(token) > 1 and counter_dict.get(token):
    counter_dict[token] = counter_dict[token]+1
    original_row = deduped_dict[token]
    merged_row = original_row[1]
    for i in range(0,len(this_row)):
     if len(merged_row[i]) < 1 and len(this_row[i]) > 1:
      merged_row[i] = this_row[i]
    deduped_dict[token] = [linecounter,merged_row]
    master_lines.pop(original_row[0])
    master_lines[linecounter] = merged_row
    if dup_dict.get(token): 
     dup_rows = dup_dict[token]
     dup_rows.append([linecounter,this_row])
     dup_dict[token] = dup_rows
    else:
     dup_dict[token] = [original_row,[linecounter,this_row]]
    break
   else:
    counter_dict[token] = 1
    deduped_dict[token] = [linecounter,this_row]
    break
  if not master_lines.get(linecounter):
   master_lines[linecounter] = this_row
 
final_counter = 0
max_counter = 0
for key, value in counter_dict.iteritems():
 if value > 1:
  print key,value
  print "Final row: ", deduped_dict[key][1][0], deduped_dict[key][1][1], deduped_dict[key][1][5], deduped_dict[key][1][6], deduped_dict[key][1][8], deduped_dict[key][1][9], deduped_dict[key][1][10]
  print "Duplicate rows were: ", len(dup_dict[key])
  for i in range (0, len(dup_dict[key])):
   print "Line Number:", dup_dict[key][i][0],":", dup_dict[key][i][1][0], dup_dict[key][i][1][1], dup_dict[key][i][1][5], dup_dict[key][i][1][6], dup_dict[key][i][1][8], dup_dict[key][i][1][9]
  print "-------------------------------------"
  final_counter += 1
  if value > max_counter:
   max_counter = value

print "Number of duplicate sets: ", final_counter
print "Max number of duplicates in a set: ", max_counter
print "Reached line number", linecounter

#with open("cleaned.csv","wb") as csvfileout:
# writer = csv.writer(csvfileout)
