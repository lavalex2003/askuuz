# Инструкция по публикации компонента

Готовим компонент `askuuz` к публикации на GitHub и HACS.

## ✅ Предварительные проверки (уже готово)

- [x] README.md - полная документация
- [x] CHANGELOG.md - история версий  
- [x] FAQ.md - часто задаваемые вопросы
- [x] CONTRIBUTING.md - гайд для контрибьюторов
- [x] SECURITY.md - политика безопасности
- [x] LICENSE - MIT лицензия
- [x] .gitignore - исключить чувствительные файлы
- [x] manifest.json - версия 1.0.0
- [x] .github/ISSUE_TEMPLATE/ - шаблоны для issues
- [x] .github/workflows/ - CI/CD pipeline

## 🚀 Шаг 1: Создание GitHub репозитория

### 1.1 На GitHub

1. Откройте https://github.com/new
2. Создайте репозиторий:
   - **Repository name**: `askuuz`
   - **Description**: `Home Assistant integration for Uzbekistan utilities (electricity, water, waste, property management)`
   - **Public**: ✅ Выберите
   - **Initialize with**: None (у вас уже есть файлы)
   - **License**: MIT (уже есть)

3. Нажмите "Create repository"

### 1.2 На локальной машине

Откройте терминал в `/root/config/custom_components/askuuz`:

```bash
# Инициализируйте git репозиторий
git init

# Добавьте origin (замените USERNAME на ваш GitHub юзер)
git remote add origin https://github.com/USERNAME/askuuz.git

# Или используйте SSH (если он настроен)
git remote add origin git@github.com:USERNAME/askuuz.git

# Проверьте статус
git status

# Добавьте все файлы
git add .

# Первый коммит
git commit -m "initial: Initialize askuuz Home Assistant integration

- Add complete ASKU portal integration
- Support 4 services: electricity, water, waste, management
- Implement DataUpdateCoordinator pattern
- Add validation and duplicate checking
- Include comprehensive documentation
- Add 3 languages: Russian, English, Uzbek"

# Отправьте на GitHub
git branch -M main
git push -u origin main
```

## 📝 Шаг 2: Создание GitHub Releases

### 2.1 Подготовка

Убедитесь, что версия в `manifest.json` совпадает с версией релиза:

```json
{
  "version": "1.0.0",
  ...
}
```

### 2.2 Создание релиза

1. Откройте https://github.com/USERNAME/askuuz/releases
2. Нажмите "Create a new release"
3. Заполните:

```
Tag version: v1.0.0
Release title: Version 1.0.0 - Initial Release
Release notes:

## Features

- ✨ Integration with ASKU portal for Uzbekistan utilities
- 📊 Support 4 services:
  - Electricity (o'lektro.uz)
  - Water (suv.uz)
  - Waste (taxminot.uz)
  - Property Management (boshqarish.uz)
- 🔐 Secure credential validation with API testing
- ✅ Duplicate configuration prevention
- 🔄 Refresh data buttons for each service
- 🌍 Multi-language support (Russian, English, Uzbek)
- ⚙️ 12-hour automatic update cycle
- 🎯 Full Home Assistant integration

## Installation

### Via HACS
1. Go to HACS > Integrations > Custom repositories
2. Add: https://github.com/USERNAME/askuuz
3. Search for "askuuz" and install

### Manual
1. Clone to: `~/.homeassistant/custom_components/askuuz`
2. Restart Home Assistant
3. Add via Settings > Devices & Services

## Documentation

- 📚 [README.md](README.md) - Complete guide
- ❓ [FAQ.md](FAQ.md) - Common questions
- 📋 [CHANGELOG.md](CHANGELOG.md) - Version history
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

## Known Issues

None at this time.

## What's Next

- [ ] Multi-account support
- [ ] Custom update intervals
- [ ] Battery indicator for sensors
- [ ] Notification alerts
```

4. Выберите "Set as the latest release"
5. Нажмите "Publish release"

## 🏠 Шаг 3: Регистрация в HACS

### 3.1 Подготовка

Убедитесь что у вас есть:

- [x] README.md в корне
- [x] LICENSE (MIT)
- [x] manifest.json с правильной версией
- [x] GitHub репозиторий публичный
- [x] Минимум один релиз (release) с тегом версии

### 3.2 Добавление в HACS

1. Откройте https://github.com/hacs/default
2. Нажмите "Fork" чтобы создать fork
3. Добавьте в файл `repositories.json`:

```json
{
  "askuuz": {
    "authors": ["lavalex2003"],
    "category": "integration",
    "description": "Home Assistant integration for Uzbekistan utilities (ASKU portal)",
    "documentation": "https://github.com/USERNAME/askuuz",
    "downloads": "https://github.com/USERNAME/askuuz/releases/latest",
    "homeassistant": "2023.6.0",
    "issues": "https://github.com/USERNAME/askuuz/issues",
    "requirements": [],
    "state": "active",
    "updated_at": "2026-01-30",
    "version": "1.0.0"
  }
}
```

4. Создайте Pull Request в `hacs/default`
5. Дождитесь одобрения

### 3.3 После регистрации

После одобрения в HACS, пользователи смогут установить через:

```
HACS → Integrations → Custom repositories → askuuz
```

## 📊 Шаг 4: Оптимизация репозитория

### 4.1 GitHub Topics

Добавьте topics (Settings > About):

- `home-assistant`
- `integration`
- `uzbekistan`
- `utilities`
- `electricity`
- `water`

### 4.2 GitHub Actions

Проверьте что workflow выполняется:

1. Перейдите на Actions
2. Убедитесь что Code Quality workflow запущен
3. Проверьте что все проверки проходят ✅

### 4.3 Branch Protection Rules

1. Перейдите Settings > Branches
2. Добавьте правило для `main`:
   - ✅ Require pull request reviews before merging (1 review)
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

## 🔍 Шаг 5: Финальная проверка

Убедитесь в наличии всех файлов:

```bash
# В корне askuuz/:
ls -la

# Должны быть:
# .github/              ← GitHub templates и workflows
# .gitignore            ← Исключить файлы
# LICENSE               ← MIT лицензия
# README.md             ← Основная документация
# CHANGELOG.md          ← История версий
# FAQ.md                ← Часто задаваемые вопросы
# CONTRIBUTING.md       ← Гайд для разработчиков
# SECURITY.md           ← Политика безопасности
# manifest.json         ← Версия 1.0.0
# __init__.py
# config_flow.py
# const.py
# button.py
# electricity/          ← Сервис электричество
# water/                ← Сервис вода
# tbo/                  ← Сервис ТБО
# management/           ← Сервис управление
# translations/         ← Переводы (ru, en, uz)
```

## 📢 Шаг 6: Продвижение

### 6.1 Объявления

- [ ] Reddit: /r/homeassistant, /r/HA_UZ (если существует)
- [ ] GitHub Discussions: https://github.com/home-assistant/home-assistant/discussions
- [ ] Home Assistant Forum: https://community.home-assistant.io
- [ ] Uzbekistan tech communities

### 6.2 Социальные сети

- [ ] Telegram каналы HA Uzbekistan
- [ ] GitHub страница (Profile)

## 🆘 Troubleshooting

### Проблема: "Repository not found" при push

```bash
# Проверьте remote
git remote -v

# Используйте HTTPS или SSH в зависимости от настройки
# HTTPS (требует token)
git remote set-url origin https://github.com/USERNAME/askuuz.git

# SSH (требует ключи)
git remote set-url origin git@github.com:USERNAME/askuuz.git
```

### Проблема: Файлы не исключены

Если секретные файлы были добавлены:

```bash
# Удалите из истории
git filter-branch --tree-filter 'rm -f secrets.yaml home-assistant.log' HEAD

# Force push (опасно! только если репо новый)
git push --force-with-lease origin main
```

### Проблема: GitHub Actions не запускается

1. Проверьте наличие файла `.github/workflows/code-quality.yml`
2. Убедитесь что репо публичный
3. Нажмите Actions и включите workflows

## ✅ Чек-лист готовности

- [ ] README.md создан и полный
- [ ] CHANGELOG.md с версией 1.0.0
- [ ] FAQ.md с частыми вопросами
- [ ] LICENSE (MIT) добавлена
- [ ] CONTRIBUTING.md для разработчиков
- [ ] SECURITY.md с политикой
- [ ] .gitignore исключает чувствительные файлы
- [ ] .github/ISSUE_TEMPLATE/ с шаблонами
- [ ] .github/workflows/ с CI/CD
- [ ] manifest.json версия 1.0.0
- [ ] GitHub репозиторий создан
- [ ] GitHub Release v1.0.0 создан
- [ ] GitHub Actions запущены и прошли
- [ ] Branch protection rules установлены
- [ ] Регистрация в HACS (Pull Request создан)

---

После выполнения всех шагов ваш компонент будет опубликован и доступен для установки через HACS! 🎉

**Примерный timeline:**
- Шаги 1-2: 5 минут
- Шаг 3 (HACS PR): 1-5 дней на одобрение
- Шаги 4-6: По мере необходимости

Удачи с публикацией! 🚀
