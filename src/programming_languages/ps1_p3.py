# Singly-Hyphenated Words

# We examined hyphenated words in a quiz in class. In this problem you
# will get a chance to handle them correctly.
#
# Assign to the variable regexp a Python regular expression that matches
# both words (with letters a-z) and also singly-hyphenated words. If you
# use grouping, you must use (?: and ) as your regular expression
# parentheses.
#
# Examples:
#
# regexp exactly matches "astronomy"
# regexp exactly matches "near-infrared"
# regexp exactly matches "x-ray"
# regexp does not exactly match "-tricky"
# regexp does not exactly match "tricky-"
# regexp does not exactly match "large - scale"
# regexp does not exactly match "gamma-ray-burst"
# regexp does not exactly match ""

# Your regular expression only needs to handle lowercase strings.

# In Python regular expressions, r"A|B" checks A first and then B - it
# does not follow the maximal munch rule. Thus, you may want to check
# for doubly-hyphenated words first and then non-hyphenated words.

import re

regexp = r"[a-z]+(?:-[a-z]+)?" # you should replace this with your regular expression

# This problem includes an example test case to help you tell if you are on
# the right track. You may want to make your own additional tests as well.

test_case_input = """the wide-field infrared survey explorer is a nasa
infrared-wavelength space telescope in an earth-orbiting satellite which
performed an all-sky astronomical survey. be careful of -tricky tricky-
hyphens --- be precise."""

test_case_output = ['the', 'wide-field', 'infrared', 'survey', 'explorer',
'is', 'a', 'nasa', 'infrared-wavelength', 'space', 'telescope', 'in', 'an',
'earth-orbiting', 'satellite', 'which', 'performed', 'an', 'all-sky',
'astronomical', 'survey', 'be', 'careful', 'of', 'tricky', 'tricky',
'hyphens', 'be', 'precise']

if re.findall(regexp, test_case_input) == test_case_output:
    print "Test case 1 passed."
else:
    print "Test case 1 failed:"
    print re.findall(regexp, test_case_input)

for successful_match in ["astronomy", "near-infrared", "x-ray"]:
    print "%s - %s" % (successful_match, re.findall(regexp, successful_match) == [successful_match])

for unsuccessful_match in ["-tricky-", "tricky-", "large - scale", "gamme-ray-burst"]:
    print "%s - %s" % (unsuccessful_match, re.findall(regexp, unsuccessful_match) != [unsuccessful_match])

