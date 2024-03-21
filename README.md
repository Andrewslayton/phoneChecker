# phoneChecker


Requirements:
  Must have Dlib shape_predictor_68_face_landmarks.dat.bz2
  See requirments.txt for packages  
  once installed run detection.py
  create .env file with aws region and keys


Proper use:
  Create account
  Set face in normal gaming position including eyes focused on middle/ bottom 2/3 of screen.
  Change sensitivity, the higher the number out of 10 the more difficult it triggers that you are on your phone
  Capture face with S(only stored locally)
  Game like normal and visit (https://phoneleaderboard.andrewslayton.dev/) to see how often you are on your phone compared to others while gaming/using your computer


How phoneChecker works:
  phone checker uses dlib in combination with the dataset mentioned above to predict the users pupils, forehead, and chin.
  I run a simple calculation determined by thousands of instances of data I acquired by testing on my own and multiple volunteer testers.
  if you are determined to be on your phone for 30 or more seconds, your phone tally count is incremented by one.
  The data is then sent to the website to be displayed 



DISCLAIMER:
  Facial data is not saved, this is honor system based please do not track under non created usernames.
  
