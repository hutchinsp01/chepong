# ChePong

```
          ,;;;!!!!!;;.
        :!!!!!!!!!!!!!!;    Uptick Chepong Leaderboard
      :!!!!!!!!!!!!!!!!!;       By Paul Hutchins
     ;!!!!!!!!!!!!!!!!!!!; 
    ;!!!!!!!!!!!!!!!!!!!!!
    ;!!!!!!!!!!!!!!!!!!!!'
    ;!!!!!!!!!!!!!!!!!!!'       o      .   _______ _______
     :!!!!!!!!!!!!!!!!'         \_ 0     /______//______/|   @_o
      ,!!!!!!!!!!!!!‘’            /\_,  /______//______/     /\\
   ,;!!!‘’'‘’'‘’''               | \    |      ||      |     / |
 .!!!!'
!!!!
```


## Setup instructions

```
poetry install
docker compose build
docker compose run --rm worker python manage.py migrate
docker compose up
```

## Hidden Urls

- Sport creation is hidden behind a url, mostly to stop accidently sport creation.
  - Goto `/sports/sport/create/`
- Season ending is again hidden behind a url, to stop accidental season ending.
  - Goto `/sports/season/<int:pk>/update`
