def boolcheck(string):
#     print(string)
    if string == 'True' or string == 'true' or string == '1':
         return True
    elif string == 'False' or string == 'false' or string == '0':
         return False
    else:
         raise ValueError("Input value is not convertible to bool.")
     
# Built upon: https://stackoverflow.com/questions/21732123/convert-true-false-value-read-from-file-to-boolean?lq=1