# akeneo-test

### Requirements
Backend
- pip (24.2)
- pipenv (2024.0.3)
- pyenv (2.4.13), to install python 3.12.x
- sqlite3

Frontend
- pmpm (9.7.1)
- node

### Run the application

API
```
cd api
pipenv shell
pipenv install --deploy --dev
python runserver.py
```

Run the tests
```
cd api
pipenv run pytest .
```


Frontend
```
cd secret-santa
pnpm install
pnpm run dev
```

### Assumptions
- The number of participants is within the expectation of a secret santa (in dozens, always less than a hundred)
- Draws are done with the participants registered at the time of draw. So if new participants are added, it has no effects on previous draws
- Draws are done purely on randomness which can sometimes lead to impossible draw, eventhough when condition for a valid draw are meet, hence the retry mechanism to ensure a draw. This is particularly usefull for some cases:
  - When the number of participant is very small: if there are 3 participants A, B and C (no blacklist), if the draw makes A gifts B and then B gifts A, then no valid draw can be made as participant C is by themself.
  - The propbability of making a valid draw decreasing the bigger the blacklist is

The retry mechanism ensures a draw is returned when conditions are meet (even on tricky situation) but it would still fail for impossible draws (e.g. one participant being blacklisted by all other participants or one participant having blacklisted all other participants).

Another approach would have been a more "deterministic" approach: if we see one participant with only one remaining pick, make this combination as a draw. But even with this situation, we could end up with dead lock draw so a retry mechanism would have been necessary regardless.


### Technical decisions
- The API follows an light hexagonal architecture, where the usecases hold the business logic, with ports as buffer to external actors. Since ports are interfaces, usecases are totally unaware of the technical implementations, which is done in the adapters. To the usecases, it does not matter which databases is used under the hood as it solely focus on the domain logic.
- The configuration is done via environment variables and the `.env` file. In normal case, this file should not be committed as it may contain sensitive information (like here with the connection string to the database). But for the sake of simplicity, it has been committed here.

### Backend Improvements
Project:
- Dockerize the application for easier setup and development
- Setup CI/CD. All code checks are done manually (tests, formatter, linter, static typing checks) and could be included in the PR flow to ensure code quality
- Split the frontend and backend applications into dedicated repos.

Business logic:
- Improvement on the blacklisting: at the moment the blacklist can only handle one blacklist direction: to ensure one participant is not gifting a particular participant but we could add the possibility for one participant to ensure they will receive a gift from a particular participant
- Better handling of email addresses (lowercase them for a stronger validation)
- Add the possibility to delete a participant, but that would require some extra work / reflection: how to handle participant to be deleted that have been drawn already ...
- Users authentification so each user can register themself rather tham being added by an admin (like it is kind of the case here)
- Permission / Authorisation so only a set of people can generate a draw or participant can only alter their own blacklist and not see others blacklist

Application / API:
- Add versioning on the API
- Improvement of the draw history endpoint: pagination (with proper HTTP status code), maximum page size ...
- Better error management and logging: the error messages are fairly generic at the moment and could be improved, while ensuring no sensitive information is leaked

Tests:
- Fixtures scope: all fixtures were scoped at the function level so for every test, we are sure to have a clean state flask application with empty database. The downside of that is that tests take a little bit longer to run. For an application of this size, it's fine but in the event this application would grow, tests run would take longer.
- Freeze date so there is no potential side effect because of the date

Database:
- Set up a database migration (Alembic) to create tables instead of relying on the models
- Use UUID instead of autoincrement for identifying resources
