#TODO: Write out all the dicts as separate CSVs
#TODO: Decompose
#TODO: Conflict dict can only store a single conflict set

import csv

def write_csv(dict_to_write, value_index, filename):
   with open(filename,"wb") as csvfileout:
      writer = csv.writer(csvfileout)
      for key,value in dict_to_write.iteritems():
         writer.writerow(value[value_index])

deduped_dict={}
dup_dict={}
conflict_dict = {}
master_lines={}
linecounter = 0
fieldsets_to_match = [[5],[0,1,5],[6,7,8,9,10],[12],[0,1,13,14,15,16]]
conflict_exclusions=[17]
with open("full_set.csv", "rb") as csvfile:
 parser = csv.reader(csvfile)
 for this_row in parser:
  linecounter += 1
  for fieldset in fieldsets_to_match:
   token = ""
   for field in fieldset:
    token = token+this_row[field].lower().strip().strip(".") #ADD flag to allow this to be toggled on and off (fuzzy vs. non-fuzzy)
   if len(token) > 1 and deduped_dict.get(token):
    original_row = deduped_dict[token]
    merged_row = original_row[1]
    if conflict_dict.get(original_row[0]):
     conflict_dict[linecounter] = conflict_dict[original_row[0]]
    else:
     conflict_dict[linecounter] = {}
    for i in range(0,len(this_row)):
     if len(merged_row[i]) < 1 and len(this_row[i]) > 1:
      merged_row[i] = this_row[i]
     elif len(merged_row[i]) > 0 and len(this_row[i]) > 0 and merged_row[i].lower().strip().strip(".") != this_row[i].lower().strip().strip(".") and i not in conflict_exclusions:
      conflict_dict[linecounter][i] = this_row[i] 
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
    deduped_dict[token] = [linecounter,this_row]
    break
  if not master_lines.get(linecounter):
   master_lines[linecounter] = this_row
 
final_counter = 0
max_counter = 0
master_fieldset = []
for fieldset in fieldsets_to_match:
 for field in fieldset:
  if field not in master_fieldset:
   master_fieldset.append(field)
print master_fieldset

for key, value in dup_dict.iteritems():
 if len(value) > 1:
  print key,len(value)
  field_values = [];
  print "Final row: ", [deduped_dict[key][1][field_value] for field_value in master_fieldset] 
  print "Duplicate rows were: ", len(dup_dict[key])
  for i in range (0, len(dup_dict[key])):
   print "Line Number:", dup_dict[key][i][0],":", [dup_dict[key][i][1][field_value] for field_value in master_fieldset]
   if conflict_dict.get(dup_dict[key][i][0]): 
    print "Conflicts:"
    for key2,value2 in conflict_dict[dup_dict[key][i][0]].iteritems():
     print "Field", key2, ":", value2
  print "-------------------------------------"
  final_counter += 1
  if len(value) > max_counter:
   max_counter = len(value)

print "Number of duplicate sets: ", final_counter
print "Max number of duplicates in a set: ", max_counter
print "Reached line number", linecounter

with open("cleaned.csv","wb") as csvfileout:
 writer = csv.writer(csvfileout)
 conflictcounter = 0
 for key,value in master_lines.iteritems():
  if conflict_dict.get(key):
   if len(conflict_dict[key]) > 0:
    conflictcounter += 1
  writer.writerow(value)
 print conflictcounter,"rows have conflicting values"

#write_csv(dup_dict, 1, "duplicate_rows.csv")
