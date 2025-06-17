# wfork search_telegram_groups.py
## Автор кода
- Misha из команды wfork_98

### search_telegram_groups
- поиск в google search на основе текста запроса
- до 100 результатов
- записевается в csv файл как таблица

--- 

<details>
  <summary>DEV Log</summary>

### v.0.1.0
- создан скрипт для получения результата в csv файле
- создан .env для разделения ключей от скрипта
- создан settings.yaml для предворительной настройки перед запуском
### v.0.1.1
- заменить txt на csv
- обнавлен README.md

### ПЛАНЫ НА БУДУЩЕЕ
- после записи данных выслать полученные данные в n8n используя POST запрос 


</details>



<details>
  <summary>Github CHEATSHEET</summary>

## Load last updates and replace existing local files
git fetch origin; git reset --hard origin/master; git clean -fd  

## Select a hash from the last 10 commits
git log --oneline -n 10  

## Use the hash to get that exact version locally
git fetch origin; git checkout master; git reset --hard 1eaef8b; git clean -fdx  

## Update repository
git add .  
git commit -m "обнавлен README.md"  
git push

</details>
