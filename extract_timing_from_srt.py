"""
Extracts timing of the question from an SRT file
"""
import re, sys
from fuzzywuzzy import fuzz

def is_time_stamp(l):
  if l[:2].isnumeric() and l[2] == ':':
    return True
  return False

def has_letters(line):
  if re.search('[a-zA-Z]', line):
    return True
  return False

def has_no_text(line):
  l = line.strip()
  if not len(l):
    return True
  if l.isnumeric():
    return True
  if is_time_stamp(l):
    return True
  if l[0] == '(' and l[-1] == ')':
    return True
  if not has_letters(line):
    return True
  return False

def is_lowercase_letter_or_comma(letter):
  if letter.isalpha() and letter.lower() == letter:
    return True
  if letter == ',':
    return True
  return False

def clean_up(lines,host):
  """
  Get rid of all non-text lines and
  try to combine text broken into multiple lines
  """
  new_lines = []
  for pos in range(1,len(lines)-1):
    if has_no_text(lines[pos]) and host not in lines[pos+1]:
      continue
    elif len(new_lines) and is_lowercase_letter_or_comma(lines[pos][0]):
      #combine with previous line
      new_lines[-1] = new_lines[-1].strip() + ' ' + lines[pos]
    else:
      #append line
      new_lines.append(lines[pos])
  return new_lines

def main(args):
  """
    args[1]: srt file name
    args[2]: encoding. Default: utf-8.
      - If you get a lot of [?]s replacing characters,
      - you probably need to change file_encoding to 'cp1252'
    args[3]: host name
    args[4]: questions file name
    
  """
  file_name = args[1]
  file_encoding = 'utf-8' if len(args) < 3 else args[2]
  host = args[3]
  questions = args[4]
  with open(file_name, encoding=file_encoding, errors='replace') as f:
    lines = f.readlines()
    new_lines = clean_up(lines,host)
  new_file_name = file_name[:-4] + '.txt'
  with open(new_file_name, 'w') as f:
    for line in new_lines:
      f.write(line)

  with open(questions,encoding = file_encoding,errors='replace') as qs:
      lines = qs.readlines()
  final_pos=0
  for line in lines:
      print(line)
      ratio=0
      final_ratio=0
      for pos in range(final_pos,len(new_lines)):
          ratio = fuzz.ratio(line.lower(),new_lines[pos].lower())
          if ratio > final_ratio:
              final_ratio = ratio
              final_pos = pos
          #if fuzz.ratio(line.lower(),new_lines[pos].lower()) > 50:
          #    break
      for indx in range(final_pos,-1,-1):
          if is_time_stamp(new_lines[indx].strip()):
              print(new_lines[indx].split(',')[0])
              break

if __name__ == '__main__':
  main(sys.argv)
