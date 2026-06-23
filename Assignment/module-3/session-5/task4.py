'''Given the following code, fix the bug so that the object is created with the correct values:
<br><br>class Movie:<br> def __init__(self, title, rating):<br> title = title<br>
rating = rating<br><br>m = Movie('Jawan', 4.5)<br>print(m.title, m.rating)<br><br>
<em><strong>Hint:</strong> Check how instance variables should be assigned inside __init__.</em>'''

class Movie:
    def __init__(self,title,rating):
        self.title=title
        self.rating=rating
        '''title=title
        rating=rating'''

m=Movie('jawan',4.5)
print(m.title,m.rating)