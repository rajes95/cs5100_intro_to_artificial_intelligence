def findDecision(obj): #obj[0]: age, obj[1]: spectacle-prescription, obj[2]: astigmatism, obj[3]: tear-prod-rate
   if obj[3] == 'reduced':
      return 'none'
   elif obj[3] == 'normal':
      if obj[2] == 'no':
         if obj[0] == 'presbyopic':
            if obj[1] == 'hypermetrope':
               return 'soft'
            elif obj[1] == 'myope':
               return 'none'
         elif obj[0] == 'young':
            return 'soft'
         elif obj[0] == 'pre-presbyopic':
            return 'soft'
      elif obj[2] == 'yes':
         return 'none'
