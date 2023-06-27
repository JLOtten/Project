# Coder's Boost
*Now deployed on:* https://codersboost.com/

*Learn more about the developer:* www.linkedin.com/in/jlotten

Coder's Boost is a fullstack application that encourages aspiring software engineers from underrepresented backgrounds in tech to meet their goals and persevere through adversity. 

Users can login with Github's OAuth to receive a unique encouraging statement in English or Spanish. Encouragements can be saved on their profile page to view at any time, with the option provide an email address to receive daily motivation using One Signal’s API. Users can develop and support others in their network by sharing encouragements with other coders via facebook, email or copying a link. Customized AI generated art and a resources page further support the user experience.

Coder's Boost is designed to fill an exsisting gap in web applications that encourages aspiring coders and to augment the many exsisting technical resources to develop coding abilities. 



<img width="1355" alt="Screen Shot 2022-11-29 at 12 06 16 PM" src="https://user-images.githubusercontent.com/108947258/204636971-c69912d7-0e24-4b00-a9ce-e7837a1c6dbd.png">
<img width="1344" alt="Screen Shot 2022-11-29 at 12 09 20 PM" src="https://user-images.githubusercontent.com/108947258/204637477-69a71be9-c70f-416b-9db7-9d010ef30ffd.png">
<img width="1343" alt="Screen Shot 2022-11-29 at 12 07 10 PM" src="https://user-images.githubusercontent.com/108947258/204637124-f477a084-61fe-4722-b30a-cdf6d7ef0050.png">
<img width="1357" alt="Screen Shot 2022-11-29 at 12 08 18 PM" src="https://user-images.githubusercontent.com/108947258/204637306-a470b218-c9d5-464c-84b3-779e9064ee15.png">


 

# Technologies Used
Python (Flask 7 Jinja), Javascript (AJAX, JSON), CSS, HTML, SQLAlchemy, PostgreSQL, Flask Babel, Bootstrap 5.0

### API's Used
Github OAuth, Open AI, Open AI DALLE-2, One Signal

# Future Improvements
Future improvements to Coder's Boost could be adding more languages, automate a process to get more encouragements in each language, allow users to upload encouraging photos to thier page and add more or update the resources page. 

# Resources
### Open AI API
* https://www.creativebloq.com/news/how-to-use-dall-e
* https://openai.com/dall-e-2/
* https://beta.openai.com/playground
* https://openai.com/dall-e-2/#demos 

### Internationalization
* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n
* https://medium.com/@nicolas_84494/flask-create-a-multilingual-web-application-with-language-specific-urls-5d994344f5fd
* https://github.com/schmidni/multilingualFlask/blob/2de451e89c79c37dc7cfb9b673259b912925f562/app/blueprints/multilingual/templates/multilingual/cake.html
* https://medium.datadriveninvestor.com/translating-your-web-app-via-flask-babel-a1561376256c

### Flask Babel
* https://python-babel.github.io/flask-babel/ 
* https://github.com/python-babel/babel 
* https://jinja.palletsprojects.com/en/3.0.x/integration/ 

### Other Inspiration Resoures
* https://www.theverge.com/2017/8/16/16153740/tech-diversity-problem-science-history-explainer-inequality
* https://hbr.org/2020/12/to-increase-diversity-u-s-tech-companies-need-to-follow-the-talent

# Developing
### Run
```
pip install -r requirements.txt
flask run
```

### Updating Translations with Flask Babel
```
# extract
pybabel extract -F babel.cfg -o messages.pot --ignore-dirs=env .
# update
pybabel update -i messages.pot -l es -d translations
pybabel update -i messages.pot -l en -d translations
# now translate files
# compile
pybabel compile -d translations
```

### Testing
```
python -m pytest .
```
