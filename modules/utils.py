def boolcheck(string):
    if string == 'True' or string == 'true' or '1':
         return True
    elif s == 'False' or s == 'false' or '0':
         return False
    else:
         raise ValueError("Input value is not convertible to bool.")
     
# Built upon: https://stackoverflow.com/questions/21732123/convert-true-false-value-read-from-file-to-boolean?lq=1